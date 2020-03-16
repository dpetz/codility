def is_power_of_2(n):
    """" https://stackoverflow.com/questions/57025836/check-if-a-given-number-is-power-of-two-in-python """
    return (n & (n-1) == 0) and n != 0


def next_power_of_2(x):
    """ https://stackoverflow.com/questions/14267555/find-the-smallest-power-of-2-greater-than-n-in-python """
    return 1 if x == 0 else 2**(x - 1).bit_length()


def inspect_bytes(btes):
    return {
        'Class': bytes.__class__,
        'Lengths': len(btes),
        'Strings': [bin(b).lstrip('0b')for b in btes],
        'Bits': [bin(b) for b in btes]
    }
