from testif import testif

DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def strB(n: int, base: int = 10) -> str:
    """Return n as a string in the given base, digits over 9 use A-Z

    Parameters: n - the number to convert; base - the base to convert to
    Precondition: n >= 0 and 2 <= base <= 26
    """
    if n < base:
        return DIGITS[n]
    return strB(n // base, base) + DIGITS[n % base]


def test_strB():
    testif(strB(0) == '0', 'strB zero', 'got 0', 'expected 0')
    testif(strB(1234, base=10) == '1234', 'strB base 10', 'got 1234', 'expected 1234')
    testif(strB(8191, base=16) == '1FFF', 'strB base 16 letters', 'got 1FFF', 'expected 1FFF')
    testif(strB(100, base=2) == '1100100', 'strB base 2', 'got 1100100', 'expected 1100100')


if __name__ == '__main__':
    test_strB()
