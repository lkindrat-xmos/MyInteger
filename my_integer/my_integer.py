import operator
from math import ceil
from itertools import chain, repeat, zip_longest
from typing import Iterable, Any, Optional, Union, Tuple


class MyInteger:
    _is_neg: bool
    _digits: Tuple[int, ...]
    sign: int

    _DIGITS = set(range(10))

    def __init__(
        self,
        n: Union["MyInteger", int, Iterable[int]] = 0,
        *,
        is_neg: Optional[bool] = None,
    ) -> None:
        if isinstance(n, MyInteger):
            self._is_neg = n._is_neg if is_neg is None else is_neg
            self._digits = n._digits
        elif isinstance(n, int):
            self._is_neg = n < 0
            self._digits = tuple(int(d) for d in reversed(str(abs(n))))
        else:  # Iterable[int]
            self._is_neg = bool(is_neg)
            self._digits = tuple(self._remove_trailing_zero_digits(n))
            if len(self._digits) == 0:
                self._digits = (0,)

            if self._is_neg:
                assert self._digits != (
                    0,
                ), "Iterable representing 0 with negative sign"

            set(self._digits) <= self._DIGITS

        self.sign = -1 if self._is_neg else int(bool(self._digits[-1]))

    @classmethod
    def _remove_trailing_zero_digits(cls, digits: Iterable[int]) -> Iterable[int]:
        zero_counter = 0
        for digit in digits:
            if digit:
                while zero_counter:
                    yield 0
                    zero_counter -= 1
                yield digit
            else:
                zero_counter += 1

    def __repr__(self) -> str:
        return "".join(
            chain("-" if self._is_neg else "", (str(d) for d in reversed(self._digits)))
        )

    def __int__(self) -> int:
        return int(str(self))

    def __len__(self) -> int:
        return len(self._digits)

    def __cmp_digits(self, other: "MyInteger") -> int:
        # -1 if self < other, 1 if self > other, 0 if self == other
        if len(self) != len(other):
            return -1 if len(self) < len(other) else 1

        for digit_self, digit_other in zip(
            reversed(self._digits), reversed(other._digits)
        ):
            if digit_self != digit_other:
                return -1 if digit_self < digit_other else 1

        return 0

    def __cmp(self, other: "MyInteger") -> int:
        # -1 if self < other, 1 if self > other, 0 if self == other
        if self.sign != other.sign:
            return -1 if self.sign < other.sign else 1
        elif self.sign == 0:
            return 0
        else:
            return self.sign * self.__cmp_digits(other)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MyInteger):
            return NotImplemented

        return self.__cmp(other) == 0

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, MyInteger):
            return NotImplemented

        return self.__cmp(other) == -1

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, MyInteger):
            return NotImplemented

        return self.__cmp(other) != 1

    def __hash__(self) -> int:
        return hash(str(self))

    def __pos__(self) -> "MyInteger":
        return self

    def __neg__(self) -> "MyInteger":
        return MyInteger(self, is_neg=not self._is_neg) if self.sign else self

    def __abs__(self) -> "MyInteger":
        return -self if self._is_neg else self

    @classmethod
    def _add_digits(cls, a: Iterable[int], b: Iterable[int]) -> Iterable[int]:
        # helper to add two Iterables of digits
        # the second argument can be negated digits
        carry = False
        for digit_self, digit_other in zip_longest(a, b, fillvalue=0):
            s = digit_self + digit_other + carry
            yield s % 10
            carry = (s > 9) - (s < 0)

        if carry:
            yield 1

    def __add__(self, other: Any) -> "MyInteger":
        if not isinstance(other, MyInteger):
            return NotImplemented

        sign_prod = self.sign * other.sign

        if sign_prod == 0:
            return self if self.sign else other

        if sign_prod == 1:
            return MyInteger(
                self._add_digits(other._digits, self._digits), is_neg=self._is_neg
            )

        return self - abs(other) if self.sign == 1 else other - abs(self)

    @classmethod
    def _sub_smaller_digits(cls, a: Iterable[int], b: Iterable[int]) -> Iterable[int]:
        # helper to subtract two Iterables of (positive) digits
        # the second iterable must represent a smaller number
        return cls._add_digits(a, map(operator.neg, b))

    def __sub__(self, other: Any) -> "MyInteger":
        if not isinstance(other, MyInteger):
            return NotImplemented

        sign_prod = self.sign * other.sign

        if sign_prod == 0:
            return self if self.sign else -other

        if sign_prod == -1:
            return MyInteger(
                self._add_digits(self._digits, other._digits), is_neg=self._is_neg
            )

        comparison = self.__cmp(other)
        if comparison == 0:  # self == other
            return MyInteger(0)

        if self._is_neg:
            # both numbers are negative
            return abs(other) - abs(self)

        # otherwise both numbers are positive
        if comparison == 1:  # self > other
            return MyInteger(self._sub_smaller_digits(self._digits, other._digits))
        else:  # self < other
            return MyInteger(
                self._sub_smaller_digits(other._digits, self._digits), is_neg=True
            )

    def __karatsuba_split(self, mid: int) -> Tuple["MyInteger", "MyInteger"]:
        # use only for positive MyIntegers
        return MyInteger(self._digits[mid:]), MyInteger(self._digits[:mid])

    def __up_shifted_digits(self, n: int) -> Iterable[int]:
        # only for non-negative n
        return chain(repeat(0, n), self._digits)

    def __padded_digits(self, n: int) -> Iterable[int]:
        return chain(self._digits, repeat(0, n - len(self)))

    def __mul__(self, other: Any) -> "MyInteger":
        if not isinstance(other, MyInteger):
            return NotImplemented

        sign_prod = self.sign * other.sign
        if sign_prod == 0:
            return MyInteger(0)

        if sign_prod == -1:
            return -(abs(self) * abs(other))

        max_len = max(len(self), len(other))
        if max_len == 1:  # recursion base case
            return MyInteger(self._digits[0] * other._digits[0])

        mid = ceil(max_len / 2)
        a, b = self.__karatsuba_split(mid)
        c, d = other.__karatsuba_split(mid)

        # recursive calls to shorter numbers
        ac, bd = a * c, b * d
        mid_term = (a + b) * (c + d) - (ac + bd)

        return MyInteger(
            self._add_digits(
                chain(bd.__padded_digits(2 * mid), ac._digits),
                mid_term.__up_shifted_digits(mid),
            )
        )

