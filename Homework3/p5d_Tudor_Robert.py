from testif import testif


def make_pairs(seq1: list, seq2: list, acc: list = []) -> list[tuple]:
    """Return a list of (x, y) tuples pairing up seq1 and seq2 by index, stops at the end of the shorter one

    Parameters: seq1 - the first list; seq2 - the second list; acc - the pairs made so far
    Precondition: seq1 and seq2 are lists
    """
    if seq1 == [] or seq2 == []:
        return acc
    return make_pairs(seq1[1:], seq2[1:], acc + [(seq1[0], seq2[0])])


def test_make_pairs() -> None:
    """Test make_pairs with same length, different length and empty lists"""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)], 'make_pairs same length',
           'got [(1, 4), (2, 5), (3, 6)]', 'expected [(1, 4), (2, 5), (3, 6)]')
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)], 'make_pairs seq2 shorter',
           'got [(1, 4), (2, 5)]', 'expected [(1, 4), (2, 5)]')
    testif(make_pairs([1, 2, 3], [4, 5, 6, 7, 8, 9]) == [(1, 4), (2, 5), (3, 6)], 'make_pairs seq1 shorter',
           'got [(1, 4), (2, 5), (3, 6)]', 'expected [(1, 4), (2, 5), (3, 6)]')
    testif(make_pairs([], [4, 5, 6, 7, 8, 9]) == [], 'make_pairs seq1 empty', 'got []', 'expected []')
    testif(make_pairs([1, 2, 3], []) == [], 'make_pairs seq2 empty', 'got []', 'expected []')


if __name__ == '__main__':
    test_make_pairs()
