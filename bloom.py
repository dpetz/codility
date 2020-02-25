
import random
import string
import unittest
import hashlib
import numpy as np

def count_exact(strs):
    return len(set(strs))


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class Hash:

    def __init__(self, bits, version=0):
        self.bits = bits
        self.version = version
        if bits == 256:
            self.hash_func = hashlib.sha256
        elif bits == 128:
            self.hash_func = hashlib.md5
        else:
            raise ValueError(f'No hash function for {bits} bits. Use 128 or 256 instead.')

    def hash(self,s):
        """Hashes string to int """

        # add single letter to modify for version
        versioned = s + str(self.version)
        return int(self.hash_func(versioned.encode('utf-8')).hexdigest(),16)


class Bloom:
    """https://en.wikipedia.org/wiki/Bloom_filter"""
    def __init__(self,m,k):
        """n -- number of bits
           k -- number of hash functions """
        self.m = m
        self.k = k
        self.hash_funcs = [Hash(m,i) for i in range(k)]
        self.bits = 0

    def add(self, elem):
        # https://wiki.python.org/moin/BitwiseOperators
        for h in self.hash_funcs:
            hashed = h.hash(elem)
            self.bits = self.bits | hashed
        print(f'Added: {hashed}')

    def contains(self,elem):
        for h in self.hash_funcs:
            hashed = h.hash(elem)
            if self.bits & hashed != hashed:
                return False
        return True

    def fill_rate(self):
        return 1.0 * bin(self.bits).count("1") / self.m


class TestBloom(unittest.TestCase):

    def test_add_and_retrieve_many(self):
        strings = [randomString(5) for i in range(10)]
        bloom = Bloom(128, 1)

        strings_approx = 0
        for s in strings:
            strings_approx += not bloom.contains(s)
            bloom.add(s)
            print(bloom.fill_rate())

        strings_exact = count_exact(strings)

        print(f'For {strings_exact} unique strings of {len(strings)} approximated: {strings_approx}')

        assert 0 < strings_approx <= strings_exact


    def test_add_and_retrieve_single(self):
        bloom = Bloom(256, 1)
        hash = Hash(256)
        s = randomString(5)
        hashed = hash.hash(s)
        print(f'{s} hashed into: {hashed}')

        assert not bloom.contains(s)
        bloom.add(s)
        assert bloom.contains(s)

    def test_unit_random(self):
        rs = randomString(5)
        print("Random string length 5: " + rs)
        assert len(rs) == 5

    def test_random(self):
        strings = [ randomString(5) for i in range(1000000)]
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