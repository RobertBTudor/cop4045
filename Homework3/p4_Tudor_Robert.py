import os
from testif import testif


def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Return the file text from from_ up to to, not including to

    Parameters: filename - the file to read; from_ - start position (from is a python keyword); to - end position, -1 means the end of the file
    Precondition: the file exists and 0 <= from_ <= to <= file length
    Postcondition: the file doesnt change
    Raises IndexError if to is past the end of the file or from_ is out of range, file errors get passed to the caller
    """
    with open(filename) as f:
        text = f.read()
    if to == -1:
        to = len(text)
    if to < 0 or to > len(text):
        raise IndexError('to (' + str(to) + ') is out of range for the file length (' + str(len(text)) + ')')
    if from_ < 0 or from_ > to:
        raise IndexError('from_ (' + str(from_) + ') is out of range')
    return text[from_:to]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Return a list of every position where search_str is found in the file

    Parameters: filename - the file to search; search_str - the string to look for
    Precondition: the file exists and search_str isnt empty
    Postcondition: the file doesnt change, returns [] if search_str isnt found
    Raises ValueError if search_str is empty, file errors get passed to the caller
    """
    if search_str == '':
        raise ValueError('search_str must not be empty')
    with open(filename) as f:
        text = f.read()
    positions = []
    pos = text.find(search_str)
    while pos != -1:
        positions.append(pos)
        pos = text.find(search_str, pos + 1)
    return positions


def ed_replace(filename: str, search_str: str, replace_with: str, occurrence: int = -1) -> int:
    """Replace search_str with replace_with in the file and return how many were replaced

    Parameters: filename - the file to change; search_str - the string to replace; replace_with - the new string; occurrence - which one to replace, -1 means all, 0 the first, 1 the second, etc
    Precondition: the file exists, search_str isnt empty and occurrence >= -1
    Postcondition: the file only changes if something was replaced, if occurrence is too big nothing is replaced and it returns 0
    Raises ValueError if search_str is empty or occurrence < -1, file errors get passed to the caller
    """
    if search_str == '':
        raise ValueError('search_str must not be empty')
    if occurrence < -1:
        raise ValueError('occurrence must be >= -1')
    with open(filename) as f:
        text = f.read()
    if occurrence == -1:
        count = text.count(search_str)
        text = text.replace(search_str, replace_with)
    else:
        positions = ed_find(filename, search_str)
        if occurrence >= len(positions):
            return 0
        pos = positions[occurrence]
        text = text[:pos] + replace_with + text[pos + len(search_str):]
        count = 1
    if count > 0:
        with open(filename, 'w') as f:
            f.write(text)
    return count


def ed_append(filename: str, string: str) -> int:
    """Add string to the end of the file and return how many characters were written

    Parameters: filename - the file to add to, its created if it doesnt exist; string - the text to add
    Precondition: string is a str
    Postcondition: string is at the end of the file
    File errors get passed to the caller
    """
    with open(filename, 'a') as f:
        return f.write(string)


def reset_file(filename: str, text: str) -> None:
    """Overwrite the file with text so each test starts the same

    Parameters: filename - the test file; text - the starting content
    """
    with open(filename, 'w') as f:
        f.write(text)


def test_ed_find() -> None:
    """Test ed_find with testif"""
    fn = 'test_file.txt'
    reset_file(fn, '01234567890123456789')
    testif(ed_find(fn, '345') == [3, 13], 'ed_find found twice', 'got [3, 13]', 'expected [3, 13]')
    testif(ed_find(fn, '356') == [], 'ed_find not found', 'got []', 'expected []')
    testif(ed_find(fn, '0123') == [0, 10], 'ed_find at the start', 'got [0, 10]', 'expected [0, 10]')
    reset_file(fn, 'aaaa')
    testif(ed_find(fn, 'aa') == [0, 1, 2], 'ed_find overlapping', 'got [0, 1, 2]', 'expected [0, 1, 2]')
    try:
        ed_find(fn, '')
        testif(False, 'ed_find empty string', '', 'no ValueError raised')
    except ValueError:
        testif(True, 'ed_find empty string', 'ValueError raised')


def test_ed_replace() -> None:
    """Test ed_replace with testif"""
    fn = 'test_file.txt'
    reset_file(fn, '01234567890123456789')
    count = ed_replace(fn, '345', 'ABCDE', 1)
    testif(count == 1 and ed_read(fn) == '0123456789012ABCDE6789', 'ed_replace one occurrence',
           'replaced the second 345', 'got ' + ed_read(fn))
    reset_file(fn, '01234567890123456789')
    count = ed_replace(fn, '345', 'ABCDE')
    testif(count == 2 and ed_read(fn) == '012ABCDE6789012ABCDE6789', 'ed_replace all',
           'replaced both 345', 'got ' + ed_read(fn))
    reset_file(fn, '01234567890123456789')
    count = ed_replace(fn, '345', 'X', 5)
    testif(count == 0 and ed_read(fn) == '01234567890123456789', 'ed_replace occurrence too big',
           'nothing changed', 'got ' + ed_read(fn))
    count = ed_replace(fn, '356', 'X')
    testif(count == 0 and ed_read(fn) == '01234567890123456789', 'ed_replace not found',
           'nothing changed', 'got ' + ed_read(fn))
    try:
        ed_replace(fn, '345', 'X', -2)
        testif(False, 'ed_replace bad occurrence', '', 'no ValueError raised')
    except ValueError:
        testif(True, 'ed_replace bad occurrence', 'ValueError raised, file still ' + ed_read(fn))


def main() -> None:
    """Show how to use each ed_ function, then run the tests"""
    fn = 'file1.txt'
    if os.path.exists(fn):
        os.remove(fn)

    # ed_append makes the file since it doesnt exist yet
    print(ed_append(fn, '0123456789'))
    print(ed_append(fn, '0123456789'))
    print(ed_read(fn))

    # ed_read
    print(ed_read(fn, 3, 9))
    print(ed_read(fn, 3))
    try:
        ed_read(fn, 5, 25)
    except IndexError as e:
        print('IndexError:', e)

    # ed_find
    print(ed_find(fn, '345'))
    print(ed_find(fn, '356'))

    # ed_replace one occurrence, then reset and replace all
    print(ed_replace(fn, '345', 'ABCDE', 1), ed_read(fn))
    reset_file(fn, '01234567890123456789')
    print(ed_replace(fn, '345', 'ABCDE'), ed_read(fn))

    # file errors get passed to the caller
    try:
        ed_read('no_such_file.txt')
    except FileNotFoundError as e:
        print('FileNotFoundError:', e)

    # unit tests
    test_ed_find()
    test_ed_replace()


if __name__ == '__main__':
    main()
