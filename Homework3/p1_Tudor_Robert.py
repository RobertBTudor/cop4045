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
    """Test every NVector method, including the error cases"""
    a = NVector([3, 0, 1, -1])
    b = NVector((3, 0, 1, -1))
    c = NVector(3, 0, 1, -1)
    print('a =', a, ' b =', b, ' c =', c)
    print('a == b == c:', a == b and b == c)

    # the vector must not share the list passed to the constructor
    lst = [1, 2, 3]
    v = NVector(lst)
    lst[0] = 100
    print('v after changing the original list:', v)

    print('len(a) =', len(a))
    print('a[1] =', a[1], ' a[-2] =', a[-2])

    x = NVector([3, 0, 1, -1])
    x[2] = 5
    print('x after x[2] = 5:', x, x == NVector([3, 0, 5, -1]))
    x[-1] = 7
    print('x after x[-1] = 7:', x)

    print('a != x:', a != x, ' a != c:', a != c, ' a == [3, 0, 1, -1]:', a == [3, 0, 1, -1])

    d = NVector([1, 2, 3, 4])
    print('a + d =', a + d)
    print('a + 10 =', a + 10)
    print('10 + a =', 10 + a)

    print('a * d =', a * d)
    print('a * 2 =', a * 2)
    print('2 * a =', 2 * a)

    print('zeros(5) =', NVector.zeros(5))

    print()
    print('Error cases:')

    try:
        NVector(5)
        print('NVector(5) -> no exception (WRONG)')
    except TypeError as e:
        print('NVector(5) -> TypeError:', e)

    try:
        NVector('abc')
        print("NVector('abc') -> no exception (WRONG)")
    except TypeError as e:
        print("NVector('abc') -> TypeError:", e)

    try:
        NVector(1, 'x', 3)
        print("NVector(1, 'x', 3) -> no exception (WRONG)")
    except TypeError as e:
        print("NVector(1, 'x', 3) -> TypeError:", e)

    try:
        a[4]
        print('a[4] -> no exception (WRONG)')
    except IndexError as e:
        print('a[4] -> IndexError:', e)

    try:
        a[-5]
        print('a[-5] -> no exception (WRONG)')
    except IndexError as e:
        print('a[-5] -> IndexError:', e)

    try:
        a['1']
        print("a['1'] -> no exception (WRONG)")
    except TypeError as e:
        print("a['1'] -> TypeError:", e)

    try:
        a[0:2]
        print('a[0:2] -> no exception (WRONG)')
    except TypeError as e:
        print('a[0:2] -> TypeError:', e)

    try:
        a[10] = 1
        print('a[10] = 1 -> no exception (WRONG)')
    except IndexError as e:
        print('a[10] = 1 -> IndexError:', e)

    try:
        a[0] = 'x'
        print("a[0] = 'x' -> no exception (WRONG)")
    except TypeError as e:
        print("a[0] = 'x' -> TypeError:", e)

    try:
        a + NVector(1, 2)
        print('a + NVector(1, 2) -> no exception (WRONG)')
    except ValueError as e:
        print('a + NVector(1, 2) -> ValueError:', e)

    try:
        a + 'x'
        print("a + 'x' -> no exception (WRONG)")
    except TypeError as e:
        print("a + 'x' -> TypeError:", e)

    try:
        a * NVector(1, 2)
        print('a * NVector(1, 2) -> no exception (WRONG)')
    except ValueError as e:
        print('a * NVector(1, 2) -> ValueError:', e)

    try:
        NVector.zeros(-1)
        print('NVector.zeros(-1) -> no exception (WRONG)')
    except ValueError as e:
        print('NVector.zeros(-1) -> ValueError:', e)

    try:
        NVector.zeros(2.5)
        print('NVector.zeros(2.5) -> no exception (WRONG)')
    except TypeError as e:
        print('NVector.zeros(2.5) -> TypeError:', e)


if __name__ == '__main__':
    main()
