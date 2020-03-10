
import random
import string
import unittest
import hashlib
import numpy as np
import math

def count_exact(strs):
    return len(set(strs))


def random_string(stringLength=10, letters=string.ascii_lowercase):
    """Generate a random string of fixed length """
    return ''.join(random.choice(letters) for i in range(stringLength))

class HashToInts:

    def __init__(self, range=256, variants=64):
        """Hashes strings to `variants` many integers between 0 and `range`-1"""

        assert range == 256
        assert variants <= 64

        self.range = range
        self.variants = variants

    def hash_to_ints(self, s):
        """Hashes string to ints """
        return [int(b) for b in hashlib.sha512(s.encode('utf-8')).digest()[0:self.variants]]



class BloomFilter:
    """https://en.wikipedia.org/wiki/Bloom_filter"""

    def __init__(self, m, k):
        """n -- number of bits
           k -- number of hash functions """
        self.m = m
        self.k = k
        self.hash_algo = HashToInts(m, k)
        self.bit_mask = 0

    def add(self, str):
        # https://wiki.python.org/moin/BitwiseOperators
        hashes = self.hash_algo.hash_to_ints(str)
        for h in hashes:
            self.bit_mask = self.bit_mask | (2 ** h)
        print(f"For '{str}' adding {len(hashes)} hashes (eg. {hashes[:5]}). Updated bit mask: {bin(self.bit_mask)[2:22]}...")

    def contains(self, str):
        for h in self.hash_algo.hash_to_ints(str):
            if self.bit_mask & (2 ** h) != 2 ** h:
                return False
        return True

    def fill_rate(self):
        return (1.0 * bin(self.bit_mask).count("1")) / self.m


class TestBloom(unittest.TestCase):

    def test_hashes(self):
        hashes = HashToInts(256, 64).hash_to_ints(random_string(100))
        assert len(hashes) == 64
        for h in hashes:
            assert isinstance(h, int)
            assert 0 <= h < 256

    def test_filter_many(self):
        strings = [random_string(5) for i in range(100)]
        print(f'Counting unique strings in: {strings} ')
        bloom = BloomFilter(256, 5)

        strings_approx = 0
        for s in strings:
            if not bloom.contains(s):
                strings_approx += 1
                bloom.add(s)
            print(bloom.fill_rate())

        strings_exact = count_exact(strings)

        print(f'{strings_exact} unique strings in {len(strings)}. Approximated: {strings_approx}')

        assert 0 < strings_approx <= strings_exact


    def test_filter_single(self):
        bloom = BloomFilter(256, 64)
        s = random_string(5)
        assert not bloom.contains(s)
        bloom.add(s)
        assert bloom.contains(s)

    def test_unit_random(self):
        rs = random_string(5)
        print("Random string length 5: " + rs)
        assert len(rs) == 5

    def test_random(self):
        strings = [ random_string(5) for i in range(1000000)]
        n = count_exact(strings)
        print(f"Number of unqiue strings: {n}")

    def test_unit_count(self):
        assert count_exact(["a","b","a"]) == 2


def bytes_to_string(_bytes):
    """Expects a https://docs.python.org/3/library/stdtypes.html#bytes """
    _str = ''
    for b in _bytes:
        _str += bin(b).lstrip('0b')
    return _str


def inspect_bytes(bytes):
    print(f'Class: {bytes.__class__}')
    print(f'Lengths: {len(bytes)}')
    print(f'As List: {[b for b in bytes]}')
    print(f'As bits: {[bin(b) for b in bytes]}')


"""
 assert len(bit_string) == self.size

    for i,b in enumerate(bit_string):
        if b == '1':
            filter[i] += 1
        elif b != '0':
            raise ValueError(f'{b} instead 0 or 1 at position {i}: {bit_string}')
"""