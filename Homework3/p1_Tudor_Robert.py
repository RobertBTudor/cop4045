from numbers import Real
from typing import Iterable, Union

Number = Union[int, float]


def check_number(value: object) -> None:
    """Raise TypeError if value is not a real number (int or float).

    Parameters:
        value: the object to check.
    Postconditions: returns normally only if value is a real number.
    Raises:
        TypeError: if value is not a real number.
    """
    if not isinstance(value, Real):
        raise TypeError('vector elements must be real numbers, got ' + type(value).__name__)


def check_index(index: object) -> None:
    """Raise TypeError if index is not an int.

    Parameters:
        index: the object to check.
    Postconditions: returns normally only if index is an int.
    Raises:
        TypeError: if index is not an int (slices are not supported).
    """
    if not isinstance(index, int):
        raise TypeError('vector indices must be integers, got ' + type(index).__name__)


class NVector:
    """An N-dimensional vector of real numbers.

    The elements are stored in a standard Python list that belongs only to
    this object (it is never shared with the caller).
    """

    def __init__(self, *args: Union[Number, Iterable[Number]]) -> None:
        """Create a new vector.

        Parameters:
            args: either a single sequence of numbers (e.g. a list or tuple),
                  or two or more numbers that become the vector elements.
        Preconditions: with one argument, it must be a sequence of real numbers;
                       with two or more, each argument must be a real number.
        Postconditions: self holds a new list with a copy of the elements.
        Raises:
            TypeError: if the single argument is not a sequence,
                       or if any element is not a real number.
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
        """Return the number of elements (the dimension) of the vector.

        Postconditions: returns an int >= 0; self is not modified.
        """
        return len(self.elements)

    def __getitem__(self, index: int) -> Number:
        """Return the element at position index.

        Parameters:
            index: an int; negative indices count from the end, like with lists.
        Preconditions: -len(self) <= index < len(self).
        Postconditions: self is not modified.
        Raises:
            TypeError: if index is not an int.
            IndexError: if index is out of range.
        """
        check_index(index)
        return self.elements[index]

    def __setitem__(self, index: int, value: Number) -> None:
        """Set the element at position index to value.

        Parameters:
            index: an int; negative indices count from the end, like with lists.
            value: the new real number to store.
        Preconditions: -len(self) <= index < len(self) and value is a real number.
        Postconditions: self[index] == value; all other elements are unchanged.
        Raises:
            TypeError: if index is not an int or value is not a real number.
            IndexError: if index is out of range.
        """
        check_index(index)
        check_number(value)
        self.elements[index] = value

    def __str__(self) -> str:
        """Return the vector as a string, e.g. 'NVector([3, 0, 1, -1])'.

        Postconditions: self is not modified.
        """
        return 'NVector(' + str(self.elements) + ')'

    def __repr__(self) -> str:
        """Return the same representation as __str__.

        Postconditions: self is not modified.
        """
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Return True if other is an NVector with the same elements as self.

        Parameters:
            other: any object.
        Postconditions: returns False if other is not an NVector or has a
                        different length; self and other are not modified.
        """
        if not isinstance(other, NVector):
            return False
        return self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Return True if self is not equal to other (the opposite of __eq__).

        Parameters:
            other: any object.
        Postconditions: self and other are not modified.
        """
        return not self == other

    def __add__(self, other: Union['NVector', Number]) -> 'NVector':
        """Return a new vector that is self + other.

        Parameters:
            other: an NVector (added element-wise) or a number (added to every element).
        Preconditions: if other is an NVector, len(other) == len(self).
        Postconditions: returns a new NVector; self and other are not modified.
        Raises:
            ValueError: if other is an NVector of a different length.
            TypeError: if other is not an NVector or a real number.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError('vectors must have the same length')
            return NVector([a + b for a, b in zip(self.elements, other.elements)])
        if isinstance(other, Real):
            return NVector([a + other for a in self.elements])
        # lets Python raise TypeError: unsupported operand type(s)
        return NotImplemented

    def __radd__(self, other: Number) -> 'NVector':
        """Return other + self, for when the left operand is a number.

        Parameters:
            other: a real number, added to every element.
        Postconditions: returns a new NVector; self is not modified.
        Raises:
            TypeError: if other is not a real number.
        """
        return self.__add__(other)

    def __mul__(self, other: Union['NVector', Number]) -> Number:
        """Return the scalar (dot) product of self and other.

        Parameters:
            other: an NVector, giving sum(A[i] * B[i]),
                   or a number B, giving sum(A[i] * B).
        Preconditions: if other is an NVector, len(other) == len(self).
        Postconditions: returns a number; self and other are not modified.
        Raises:
            ValueError: if other is an NVector of a different length.
            TypeError: if other is not an NVector or a real number.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError('vectors must have the same length')
            return sum(a * b for a, b in zip(self.elements, other.elements))
        if isinstance(other, Real):
            return sum(a * other for a in self.elements)
        # lets Python raise TypeError: unsupported operand type(s)
        return NotImplemented

    def __rmul__(self, other: Number) -> Number:
        """Return other * self, for when the left operand is a number.

        Parameters:
            other: a real number B, giving sum(A[i] * B).
        Postconditions: returns a number; self is not modified.
        Raises:
            TypeError: if other is not a real number.
        """
        return self.__mul__(other)

    @classmethod
    def zeros(cls, n: int) -> 'NVector':
        """Return a new vector of dimension n with all elements 0.

        Parameters:
            n: the dimension of the new vector.
        Preconditions: n is an int and n >= 0.
        Postconditions: returns a new NVector v with len(v) == n and every v[i] == 0.
        Raises:
            TypeError: if n is not an int.
            ValueError: if n is negative.
        """
        if not isinstance(n, int):
            raise TypeError('dimension must be an integer, got ' + type(n).__name__)
        if n < 0:
            raise ValueError('dimension must not be negative')
        return cls([0] * n)


def expect_error(description: str, action, error: type) -> None:
    """Run action() and print whether it raised the expected exception type.

    Parameters:
        description: text describing the call, used in the printed message.
        action: a function with no parameters that should raise error.
        error: the exception class action() is expected to raise.
    Postconditions: prints one line; never lets the exception propagate.
    """
    try:
        action()
        print(description, '-> no exception (WRONG)')
    except error as e:
        print(description, '->', type(e).__name__ + ':', e)
    except Exception as e:
        print(description, '-> unexpected', type(e).__name__ + ':', e)


def main() -> None:
    """Exercise every NVector method, including the error cases."""
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
    expect_error('NVector(5)', lambda: NVector(5), TypeError)
    expect_error("NVector('abc')", lambda: NVector('abc'), TypeError)
    expect_error("NVector(1, 'x', 3)", lambda: NVector(1, 'x', 3), TypeError)
    expect_error('a[4]', lambda: a[4], IndexError)
    expect_error('a[-5]', lambda: a[-5], IndexError)
    expect_error("a['1']", lambda: a['1'], TypeError)
    expect_error('a[0:2]', lambda: a[0:2], TypeError)
    expect_error('a[10] = 1', lambda: a.__setitem__(10, 1), IndexError)
    expect_error("a[0] = 'x'", lambda: a.__setitem__(0, 'x'), TypeError)
    expect_error('a + NVector(1, 2)', lambda: a + NVector(1, 2), ValueError)
    expect_error("a + 'x'", lambda: a + 'x', TypeError)
    expect_error("'x' + a", lambda: 'x' + a, TypeError)
    expect_error('a * NVector(1, 2)', lambda: a * NVector(1, 2), ValueError)
    expect_error('a * [1, 2, 3, 4]', lambda: a * [1, 2, 3, 4], TypeError)
    expect_error('NVector.zeros(-1)', lambda: NVector.zeros(-1), ValueError)
    expect_error('NVector.zeros(2.5)', lambda: NVector.zeros(2.5), TypeError)


if __name__ == '__main__':
    main()
