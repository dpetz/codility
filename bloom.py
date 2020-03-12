
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


def bloom_insertions(m, n):
    """m -- bits, n -- inserts"""
    k = math.ceil(math.log(2) * m / n)
    print(f"bits={m}, inserts={n} --> hashes={k}")
    return BloomFilter(m, k)


def bloom_false_positives(epsilon, n):
    """epsilon -- accepted false positive rate, n -- inserts"""
    m = (math.log(epsilon) * n) / (math.log(2) ** 2)
    print(f"epsilon={epsilon}, inserts={n} --> bits={m}")
    return bloom_insertions(next_power_of_2(m), n)


class Hasher:

    alg = hashlib.sha512
    size = 512  # number of bits

    def __init__(self, k=8, n=64):
        """Will hash string to `n` times `k` bits"""

        assert k * n <= self.size, \
            f"{self.size} bit hash function {self.alg} cannot create {n} times {k} bits"
        self.k, self.n = k, n

    def bits(self, s):
        """ Hashes string to byte array and wraps its bits as integer """

        return int.from_bytes(self.alg(s.encode('utf-8')).digest(), byteorder='big', signed=False)

    def ints(self, s):
        """Hashes string and slices results into bit fields returned as list of integers. """

        hash_bits = self.bits(s)
        return [int((hash_bits >> int(i * self.k)) % (2 ** self.k)) for i in range(self.n)]

class BloomFilter:
    """https://en.wikipedia.org/wiki/Bloom_filter"""

    def __init__(self, m, k):
        """m -- number of bits
           k -- number of hash functions """
        assert is_power_of_2(m)

        self.m, self.k = m, k
        self.hasher = Hasher(int(math.log2(m)), k)
        self.bits_as_int = 0

    def add(self, str):
        # https://wiki.python.org/moin/BitwiseOperators
        hashes = self.hasher.ints(str)
        # print(f"Adding {hashes} to {self .inspect()}")
        for h in hashes:
            self.bits_as_int = self.bits_as_int | (2 ** h)

    def contains(self, str):
        for h in self.hasher.ints(str):
            if self.bits_as_int & (2 ** h) != 2 ** h:
                return False
        return True

    def fill_rate(self):
        return (1.0 * self.bits_filled()) / self.m

    def bits_filled(self):
        return self.bit_mask().count("1")

    def bit_mask(self):
        return bin(self.bits_as_int).lstrip('0b')

    def inspect(self):
        return f"funcs={self.k}, bits={self.m}, fill={self.bits_filled()}, mask={self.bit_mask()}"

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
        assert not bloom.contains(s)
        bloom.add(s)
        assert bloom.contains(s)

    def test_many(self, n=100000):
        strings = [random_string(5) for i in range(n)]
        print(f'Counting unique strings in: {strings} ')
        bloom = bloom_insertions(2 ** 20, n)  # BloomFilter(2 ** 12, 8)

        strings_approx = 0
        for s in strings:
            if not bloom.contains(s):
                strings_approx += 1
                bloom.add(s)

        strings_exact = count_exact(strings)

        print(f'{strings_exact} unique strings in {len(strings)}. Approximated: {strings_approx}')

        assert 0 < strings_approx <= strings_exact


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
