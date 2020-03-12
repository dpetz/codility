
import random
import string
import unittest
import hashlib
import math


def count_exact(strs):
    return len(set(strs))


def random_string(stringLength=10, letters=string.ascii_lowercase):
    """Generate a random string of fixed length """
    return ''.join(random.choice(letters) for i in range(stringLength))


def is_power_of_2(n):
    # https://stackoverflow.com/questions/57025836/check-if-a-given-number-is-power-of-two-in-python
    return (n & (n-1) == 0) and n != 0


def next_power_of_2(x):
    # https://stackoverflow.com/questions/14267555/find-the-smallest-power-of-2-greater-than-n-in-python
    return 1 if x == 0 else 2**(x - 1).bit_length()


def inspect_bytes(btes):
    print(f'Class: {bytes.__class__}')
    print(f'Lengths: {len(btes)}')
    print(f"Strings: {[bin(b).lstrip('0b')for b in btes]}")
    print(f'Bits: {[bin(b) for b in btes]}')


def bloom_inserts(m, n):
    """ Create BloomFilter with good number of has functions for m bits and n insertions """
    k = math.ceil(math.log(2) * m / n)
    print(f"bits={m}, inserts={n} --> hashes={k}")
    return BloomFilter(m, k)


def bloom_fp(epsilon, n):
    """ Create BloomFilter with false positive rate of epsilon for n inserts """
    m = -int(math.ceil(math.log(epsilon) * n) / (math.log(2) ** 2))
    print(f"epsilon={epsilon}, inserts={n} --> bits={m}")
    return bloom_inserts(next_power_of_2(m), n)


class Hasher:

    alg = hashlib.sha512
    size = 512  # number of bits

    def __init__(self, k=8, n=64):
        """ Will hash string n times to k bits """

        assert k * n <= self.size, \
            f"{self.size} bit hash function {self.alg} cannot create {n} times {k} bits"

        self.k, self.n = k, n

    def bits(self, s):
        """ Hash string to byte array and return as integer """

        return int.from_bytes(self.alg(s.encode('utf-8')).digest(), byteorder='big', signed=False)

    def ints(self, s):
        """Hashes string and slices results into bit fields returned as list of integers. """

        hash_bits = self.bits(s)
        return [int((hash_bits >> int(i * self.k)) & (2 ** (self.k+1)) - 1) for i in range(self.n)]


class BloomFilter:
    """https://en.wikipedia.org/wiki/Bloom_filter"""

    def __init__(self, m, k):
        """New filter with m bits and k hash functions """
        assert is_power_of_2(m)

        self.m, self.k = m, k
        self.hasher = Hasher(int(math.log2(m)), k)
        self.bits_as_int, self.added = 0, 0

    def add(self, str):
        # https://wiki.python.org/moin/BitwiseOperators
        for h in self.hasher.ints(str):
            self.bits_as_int = self.bits_as_int | (2 ** h)
            self.added += 1

    def query(self, str):
        for h in self.hasher.ints(str):
            if self.bits_as_int & (2 ** h) != 2 ** h:
                return False
        return True

    def stats(self):
        ones = self.bit_mask().count("1")
        return {
            '1s' : ones ,
            'fill rate': ones / self.m,
            'added': self.added
        }

    def bit_mask(self):
        return bin(self.bits_as_int).lstrip('0b')

    def inspect(self):
        return f"funcs={self.k}, bits={self.m}, stats={self.stats()}, mask={self.bit_mask()}"

class TestHashes(unittest.TestCase):

    @staticmethod
    def random(k, n):
        return Hasher(k, n).ints(random_string())

    def test_variants(self):
        assert len(self.random(8, 64)) == 64

    def test_variance(self):
        ints = self.random(7, 73)
        assert len(ints) - len(set(ints)) < 2, f"Element appears more than twice: {ints}"

    def test_values(self):
        for i in self.random(3, 100):
            assert isinstance(i, int)
            assert 0 <= i < 8, f"Out of range: {i}"


class TestBloom(unittest.TestCase):

    def test_single(self):
        bloom = BloomFilter(8, 64)
        s = random_string(5)
        assert not bloom.query(s)
        bloom.add(s)
        assert bloom.query(s)

    def test_many(self, n=10000):
        strings = [random_string(5) for i in range(n)]
        print(f'Counting unique strings in: {strings} ')
        bloom = bloom_fp(0.2, n)  # BloomFilter(2 ** 12, 8)

        strings_approx = 0
        for s in strings:
            if not bloom.query(s):
                strings_approx += 1
                bloom.add(s)

        strings_exact = count_exact(strings)

        print(f'{strings_exact} unique strings in {len(strings)}. Approximated: {strings_approx}')

        assert 0 < strings_approx <= strings_exact

        # Process finished with exit code 0
        # Counting unique strings in: ['rkqeg', 'anqzw', ...
        # epsilon=0.2, inserts=10000 --> bits=33497
        # bits=65536, inserts=10000 --> hashes=5
        # 9996 unique strings in 10000. Approximated: 9989
        # Ran 1 test in 13.569s


class TestRandom(unittest.TestCase):

    def test_length(self):
        length = ord(random_string(1)[0])
        rs = random_string(length)
        print(f"Random string of length {length}: {rs}")
        assert len(rs) == length

    def test_diversity(self):
        n = 1000000  # number of strings
        ls = 5  # lengths of strings
        strings = [random_string(ls) for i in range(n)]
        count = count_exact(strings)
        print(f"{count} of {n} strings of length {ls} unique.")
        assert count == len(set(strings))
