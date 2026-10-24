import testif


def check_number(value: object) -> None:
    """Make sure value is a number

    Parameters: value - the object to check
    Raises: TypeError if value is not an int or float
    """
    if not isinstance(value, (int, float)):
        raise TypeError('vector elements must be numbers, got ' + type(value).__name__)


def check_index(index: object) -> None:
    """Make sure index is an int

    Parameters: index - the object to check
    Raises: TypeError if index is not an int
    """
    if not isinstance(index, int):
        raise TypeError('vector indices must be integers, got ' + type(index).__name__)


class NVector:
    """An N-dimensional vector of real numbers stored in a list"""

    def __init__(self, *args: int | float | list | tuple) -> None:
        """Create a new vector

        Parameters: one sequence of numbers, or two or more numbers
        Precondition: all elements are numbers
        Postcondition: the elements are copied into a new list
        Raises: TypeError if a single argument is not a sequence or an element is not a number
        """
        if len(args) == 1:
            # copy the sequence into a new list so no state is shared with the caller
            elements = list(args[0])
        else:
            elements = list(args)
        for value in elements:
            check_number(value)
        self.elements = elements

    def __len__(self) -> int:
        """Return the length of the vector"""
        return len(self.elements)

    def __getitem__(self, index: int) -> int | float:
        """Return the element at index

        Parameters: index - an int, negative counts from the end
        Precondition: -len(self) <= index < len(self)
        Raises: TypeError if index is not an int, IndexError if out of range
        """
        check_index(index)
        return self.elements[index]

    def __setitem__(self, index: int, value: int | float) -> None:
        """Set the element at index to value

        Parameters: index - an int, negative counts from the end; value - a number
        Precondition: -len(self) <= index < len(self)
        Postcondition: self[index] == value
        Raises: TypeError if index is not an int or value is not a number, IndexError if out of range
        """
        check_index(index)
        check_number(value)
        self.elements[index] = value

    def __str__(self) -> str:
        """Return the vector as a string like NVector([3, 0, 1, -1])"""
        return 'NVector(' + str(self.elements) + ')'

    def __repr__(self) -> str:
        """Return the same string as __str__"""
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Return True if other is an NVector with the same elements"""
        if not isinstance(other, NVector):
            return False
        return self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Return True if other is not equal to self"""
        return not self == other

    def __add__(self, other: 'NVector | int | float') -> 'NVector':
        """Return a new vector of self + other

        Parameters: other - an NVector (added element by element) or a number (added to each element)
        Precondition: if other is an NVector, it has the same length
        Postcondition: self and other are not changed
        Raises: ValueError if the lengths differ, TypeError if other is the wrong type
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError('vectors must have the same length')
            return NVector([a + b for a, b in zip(self.elements, other.elements)])
        if isinstance(other, (int, float)):
            return NVector([a + other for a in self.elements])
        # lets Python raise TypeError: unsupported operand type(s)
        return NotImplemented

    def __radd__(self, other: int | float) -> 'NVector':
        """Return a new vector of other + self when other is a number"""
        return self.__add__(other)

    def __mul__(self, other: 'NVector | int | float') -> int | float:
        """Return the scalar product of self and other

        Parameters: other - an NVector gives sum(A[i] * B[i]), a number B gives sum(A[i] * B)
        Precondition: if other is an NVector, it has the same length
        Postcondition: self and other are not changed
        Raises: ValueError if the lengths differ, TypeError if other is the wrong type
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError('vectors must have the same length')
            return sum(a * b for a, b in zip(self.elements, other.elements))
        if isinstance(other, (int, float)):
            return sum(a * other for a in self.elements)
        # lets Python raise TypeError: unsupported operand type(s)
        return NotImplemented

    def __rmul__(self, other: int | float) -> int | float:
        """Return the scalar product of other * self when other is a number"""
        return self.__mul__(other)

    @classmethod
    def zeros(cls, n: int) -> 'NVector':
        """Return a new vector of length n with all elements 0

        Precondition: n is an int and n >= 0
        Raises: TypeError if n is not an int, ValueError if n is negative
        """
        if not isinstance(n, int):
            raise TypeError('dimension must be an integer, got ' + type(n).__name__)
        if n < 0:
            raise ValueError('dimension must not be negative')
        return cls([0] * n)


def main() -> None:
    """Test parts a) - i) with the testif function"""
    # a) constructor with one sequence argument
    a = NVector([3, 0, 1, -1])
    testif.testif(a.elements == [3, 0, 1, -1], 'constructor with a list', 'elements are [3, 0, 1, -1]', 'wrong elements')
    t = NVector((3, 0, 1, -1))
    testif.testif(t.elements == [3, 0, 1, -1], 'constructor with a tuple', 'elements are [3, 0, 1, -1]', 'wrong elements')
    lst = [1, 2, 3]
    v = NVector(lst)
    lst[0] = 100
    testif.testif(v.elements == [1, 2, 3], 'constructor copies the list', 'changing the original list does not change the vector', 'the list is shared')

    ok = False
    try:
        NVector(5)
    except TypeError:
        ok = True
    testif.testif(ok, 'constructor with a scalar', 'raised TypeError', 'no TypeError')

    ok = False
    try:
        NVector(1, 'x', 3)
    except TypeError:
        ok = True
    testif.testif(ok, 'constructor with a non-number', 'raised TypeError', 'no TypeError')

    # b) constructor with two or more arguments
    b = NVector(3, 0, 1, -1)
    testif.testif(b.elements == [3, 0, 1, -1], 'constructor with 4 arguments', 'elements are [3, 0, 1, -1]', 'wrong elements')

    # c) __len__
    testif.testif(len(a) == 4, 'len', 'len is 4', 'len is ' + str(len(a)))

    # d) __getitem__
    testif.testif(a[1] == 0, 'getitem', 'a[1] == 0', 'a[1] == ' + str(a[1]))
    testif.testif(a[-2] == 1, 'getitem negative index', 'a[-2] == 1', 'a[-2] == ' + str(a[-2]))

    ok = False
    try:
        a[4]
    except IndexError:
        ok = True
    testif.testif(ok, 'getitem out of range', 'raised IndexError', 'no IndexError')

    ok = False
    try:
        a['1']
    except TypeError:
        ok = True
    testif.testif(ok, 'getitem with a non-int index', 'raised TypeError', 'no TypeError')

    # e) __setitem__
    x = NVector(3, 0, 1, -1)
    x[2] = 5
    testif.testif(x == NVector(3, 0, 5, -1), 'setitem', 'x[2] = 5 gives ' + str(x), 'got ' + str(x))
    x[-1] = 7
    testif.testif(x[3] == 7, 'setitem negative index', 'x[-1] = 7 gives ' + str(x), 'got ' + str(x))

    ok = False
    try:
        x[10] = 1
    except IndexError:
        ok = True
    testif.testif(ok, 'setitem out of range', 'raised IndexError', 'no IndexError')

    ok = False
    try:
        x[0] = 'x'
    except TypeError:
        ok = True
    testif.testif(ok, 'setitem with a non-number', 'raised TypeError', 'no TypeError')

    # f) __str__
    testif.testif(str(a) == 'NVector([3, 0, 1, -1])', 'str', str(a), 'got ' + str(a))

    # g) __eq__ and __ne__
    testif.testif(a == b, 'eq with an equal vector', 'a == b', 'a != b')
    testif.testif(not (a == x), 'eq with a different vector', 'a == x is False', 'a == x is True')
    testif.testif(not (a == [3, 0, 1, -1]), 'eq with a list', 'a == list is False', 'a == list is True')
    testif.testif(a != x, 'ne with a different vector', 'a != x', 'a != x is False')
    testif.testif(not (a != b), 'ne with an equal vector', 'a != b is False', 'a != b is True')

    # h) __add__ and __radd__
    d = NVector(1, 2, 3, 4)
    testif.testif(a + d == NVector(4, 2, 4, 3), 'add two vectors', str(a + d), 'got ' + str(a + d))
    testif.testif(a + 10 == NVector(13, 10, 11, 9), 'add a number', str(a + 10), 'got ' + str(a + 10))
    testif.testif(10 + a == NVector(13, 10, 11, 9), 'radd a number', str(10 + a), 'got ' + str(10 + a))

    ok = False
    try:
        a + NVector(1, 2)
    except ValueError:
        ok = True
    testif.testif(ok, 'add vectors of different lengths', 'raised ValueError', 'no ValueError')

    ok = False
    try:
        a + 'x'
    except TypeError:
        ok = True
    testif.testif(ok, 'add a string', 'raised TypeError', 'no TypeError')

    # i) __mul__ and __rmul__
    testif.testif(a * d == 2, 'mul two vectors', 'a * d == 2', 'got ' + str(a * d))
    testif.testif(a * 2 == 6, 'mul a number', 'a * 2 == 6', 'got ' + str(a * 2))
    testif.testif(2 * a == 6, 'rmul a number', '2 * a == 6', 'got ' + str(2 * a))

    ok = False
    try:
        a * NVector(1, 2)
    except ValueError:
        ok = True
    testif.testif(ok, 'mul vectors of different lengths', 'raised ValueError', 'no ValueError')

    # j) zeros
    z = NVector.zeros(5)
    testif.testif(z == NVector(0, 0, 0, 0, 0), 'zeros', str(z), 'got ' + str(z))

    ok = False
    try:
        NVector.zeros(-1)
    except ValueError:
        ok = True
    testif.testif(ok, 'zeros with a negative length', 'raised ValueError', 'no ValueError')


if __name__ == '__main__':
    main()
