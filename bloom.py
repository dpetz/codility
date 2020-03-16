from random import choice
import string
from unittest import TestCase
from dataclasses import dataclass
from hashlib import sha512
from math import log, ceil, log2
from bit_util import next_power_of_2


@dataclass
class Poet:
    """ Generate words by sampling [size] many [letters]. """

    size: int = 10
    letters: str = string.ascii_lowercase

    def word(self):
        """Generate single word. """
        return ''.join(choice(self.letters) for i in range(self.size))

    def words(self, n):
        """Generate n words. """
        return [self.word() for i in range(n)]


class Hasher:

    def __init__(self, k=8, n=64, alg=sha512()):
        """ Will hash string n times to k bits """
        self.k, self.n, self.alg = k, n, alg
        self.size = alg.digest_size * 8  # number of bits, eg. 512
        assert k * n <= self.size, \
            f"{self.size} bit hash function {alg} cannot create {n} times {k} bits"

    def bits(self, word):
        """ Hash string to byte array and return as integer """
        self.alg.update(word.encode('utf-8'))
        return int.from_bytes(self.alg.digest(), byteorder='big', signed=False)

    def ints(self, word):
        """Hashes string and slices results into bit fields returned as list of integers. """
        hash_bits = self.bits(word)
        return [int((hash_bits >> int(i * self.k)) & (2 ** self.k - 1)) for i in range(self.n)]

    def scaled(self, word, ubound):
        """Rescales entries in self.ints to [s,unbound)"""
        return [int((2 ** self.k) * i / ubound) for i in self.ints(word)]


class Filter:
    """https://en.wikipedia.org/wiki/Bloom_filter
       https://wiki.python.org/moin/BitwiseOperators"""

    @staticmethod
    def create_n(m, n):
        """ Create BloomFilter with good number of hash functions for m bits and n insertions """
        k = int(ceil(log(2) * m / n))
        return Filter(m, k)

    @staticmethod
    def create_fp(epsilon, n):
        """ Create BloomFilter with false positive rate of epsilon for n inserts """
        m = -int(ceil(log(epsilon) * n) / (log(2) ** 2))
        return Filter.create_n(m, n)

    def __init__(self, m: int, k: int):
        """New filter with m bits and k hash functions """
        assert isinstance(k, int), k
        assert isinstance(m, int), m
        self.hasher = Hasher(int(log2(next_power_of_2(m))), k)
        self.bits, self.m, self.k = 0, m, k

    def _hashes(self, word):
        return self.hasher.scaled(word, self.m)

    def add(self, word):
        """ Add word to filter. """
        for h in self._hashes(word):
            self.bits = self.bits | (2 ** h)

    def query(self, word):
        """Is word contained? """
        for h in self._hashes(word):
            if self.bits & (2 ** h) != 2 ** h:
                return False
        return True

    def approx(self):
        """Approximate number of items """
        return -int(self.m * log(1 - self.filled() / self.m) / self.k)

    def bit_str(self):
        return bin(self.bits).lstrip('0b')

    def filled(self):
        return self.bit_str().count("1")

    def __repr__(self):
        return {
            'm': self.m,
            'k': self.k,
            '%': round(self.filled() / self.m * 100, 2),
        }

    def __str__(self):
        return f'Bloom({self.__repr__()})'


class TestHashes(TestCase):

    @staticmethod
    def ints(k, n):
        return Hasher(k, n).ints(Poet().word())

    def test_size(self):
        assert len(self.ints(7, 73)) == 73

    def test_variance(self):
        ints = self.ints(8, 64)
        assert len(set(ints)) / len(ints) >= .9, f"Element appears more than twice: {ints}"

    def test_values(self,bits=3):
        for i in self.ints(bits, 100):
            assert isinstance(i, int)
            assert 0 <= i < (2**bits), f"Out of range: {i}"


class TestBloom(TestCase):

    def test_create_n(self, m=958505, n=100000, k=7):
        print(f"bits={m}, inserts={n} --> hashes={k}")
        assert Filter.create_n(m, n).k == k

    def test_create_fp(self, fp=0.01, n=100000, m=958505):
        print(f"epsilon={fp}, inserts={n} --> bits={m}")
        assert Filter.create_fp(fp, n).m == m

    def test_add(self, poet=Poet(5)):
        bloom = Filter(8, 64)
        word = poet.word()
        assert not bloom.query(word)
        bloom.add(word)
        assert bloom.query(word)

    def test_approx(self, n=100000, poet=Poet(5), false_positive_rate=.1):
        """Filter approximation of unique items after n insertions is at most false_positive_rate % off-."""
        words = poet.words(n)
        bloom = Filter.create_fp(false_positive_rate, n)

        for w in words:
            bloom.add(w)

        print(f'Filter:{bloom}')

        words_exact = len(set(words))
        words_approx = bloom.approx()
        error = round(abs(words_exact - words_approx) / words_exact * 100, 2)

        print(f'{bloom} approximates {words_approx} of {len(set(words))} words unique ({error}% error).')

        assert error <= false_positive_rate * 100

        # test_approx(self, n=100000, poet=Poet(5), false_positive_rate=.1)
        # Bloom({'m': 479251, 'k': 4, '%': 58.16}) approximates 104400 of 99574 words unique (4.85% error).


class TestPoet(TestCase):

    def test_char(self, n=100):
        c = Poet(1, string.ascii_lowercase).word()
        assert 97 <= ord(c) <= 122
        return c

    def test_length(self):
        length = ord(self.test_char())  # sample single character and take its Unicode code point as length
        assert len(Poet(length).word()) == length

    def test_diversity(self, n=100000, k=5, pct=.9):
        assert len(set(Poet(k).words(n))) / n > pct, f"Less than {pct} of {n} random words of length {k} are unique."
