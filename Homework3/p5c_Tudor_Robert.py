from testif import testif

memo = {}


def Cnk_m(n: int, k: int) -> int:
    """Return n choose k, saving results in memo so each (n, k) is only computed once

    Parameters: n - the number of items; k - the number of items chosen
    Precondition: 0 <= k <= n
    """
    if k == 0 or k == n:
        return 1
    if (n, k) not in memo:
        memo[(n, k)] = Cnk_m(n - 1, k - 1) + Cnk_m(n - 1, k)
    return memo[(n, k)]


def test_Cnk_m():
    testif(Cnk_m(5, 0) == 1, 'Cnk_m k is 0', 'got 1', 'expected 1')
    testif(Cnk_m(5, 2) == 10, 'Cnk_m small', 'got 10', 'expected 10')
    testif(Cnk_m(20, 10) == 184756, 'Cnk_m middle', 'got 184756', 'expected 184756')
    testif(Cnk_m(100, 50) == 100891344545564193334812497256, 'Cnk_m big',
           'got 100891344545564193334812497256', 'expected 100891344545564193334812497256')


if __name__ == '__main__':
    test_Cnk_m()
