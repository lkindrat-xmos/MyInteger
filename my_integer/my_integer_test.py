import pytest
import random
from math import log10, ceil
from typing import Optional

from my_integer import MyInteger

NUM_CASES = 100


class ValueUnderTest:
    def __init__(
        self,
        a: Optional[int] = None,
        b: Optional[int] = None,
        *,
        minval: int = 2 ** 64,
        maxval: int = 2 ** 66,
        ensure_same_a_b: bool = False
    ) -> None:
        assert maxval > minval
        if a is None or ensure_same_a_b:
            assert b is None

        self.a = random.randint(minval, maxval) if a is None else a

        if b is not None:
            self.b = b
        elif ensure_same_a_b:
            self.b = self.a
        else:
            while True:
                self.b = random.randint(minval, maxval)
                if self.a != self.b:
                    break

        self.A = MyInteger(self.a)
        self.B = MyInteger(self.b)


@pytest.fixture(params=list(range(NUM_CASES)))
def vut(request) -> ValueUnderTest:
    return ValueUnderTest()


def test_zero() -> None:
    assert int(MyInteger(0)) == 0
    assert str(MyInteger(0)) == "0"
    assert abs(MyInteger(0)) == MyInteger(0)
    assert MyInteger(0) == -MyInteger(0)
    assert MyInteger(0) + MyInteger(0) == MyInteger(0)
    assert MyInteger(0) - MyInteger(0) == MyInteger(0)
    assert MyInteger(0) * MyInteger(0) == MyInteger(0)


def test_neg(vut: ValueUnderTest) -> None:
    assert -vut.A == MyInteger(-vut.a)
    assert (
        -(-vut.A) == vut.A == -MyInteger(-vut.a)  # pylint: disable=nonexistent-operator
    )


def test_int(vut: ValueUnderTest) -> None:
    assert int(vut.A) == vut.a
    assert int(-vut.A) == -vut.a


def test_repr(vut: ValueUnderTest) -> None:
    assert str(vut.A) == str(vut.a)
    assert str(-vut.A) == str(-vut.a)

    assert str(-vut.A)[0] == "-"
    assert str(-vut.A)[1:] == str(vut.A)

    set(str(vut.A)) <= set("0123456789")


def test_len(vut: ValueUnderTest) -> None:
    assert ceil(log10(vut.a)) == len(vut.A)
    assert ceil(log10(vut.a)) == len(-vut.A)


def test_abs(vut: ValueUnderTest) -> None:
    assert abs(vut.A) == vut.A
    assert abs(MyInteger(-vut.a)) == abs(-vut.A) == vut.A


def test_eq(vut: ValueUnderTest) -> None:
    assert vut.A == vut.A
    assert -vut.A == -vut.A

    if vut.a == vut.b:
        assert vut.A == vut.B
        assert -vut.A == -vut.B
    else:
        assert not vut.A == vut.B
        assert not -vut.A == -vut.B


def test_ne(vut: ValueUnderTest) -> None:
    assert not vut.A != vut.A
    assert not -vut.A != -vut.A

    if vut.a != vut.b:
        assert vut.A != vut.B
        assert -vut.A != -vut.B
    else:
        assert not vut.A != vut.B
        assert not -vut.A != -vut.B


def _test_lt(A: MyInteger, B: MyInteger) -> None:
    assert -A < A
    assert not A < -A

    assert A < B
    assert not B < A

    assert -B < -A
    assert not -A < -B


def test_lt(vut: ValueUnderTest) -> None:
    if vut.a < vut.b:
        _test_lt(vut.A, vut.B)
    if vut.a > vut.b:
        _test_lt(vut.B, vut.A)


def _test_le(A: MyInteger, B: MyInteger) -> None:
    assert -A <= A
    assert A <= A
    assert not A <= -A

    assert A <= B
    assert not B < A

    assert -B <= -A
    assert not -A < -B


def test_le(vut: ValueUnderTest) -> None:
    if vut.a <= vut.b:
        _test_le(vut.A, vut.B)
    if vut.a >= vut.b:
        _test_le(vut.B, vut.A)


def test_add(vut: ValueUnderTest) -> None:
    assert MyInteger(0) + vut.A == vut.A
    assert MyInteger(0) + (-vut.A) == (-vut.A)

    assert MyInteger(vut.a + vut.b) == vut.A + vut.B
    assert MyInteger(-vut.a - vut.b) == (-vut.A) + (-vut.B) == -(vut.A + vut.B)

    assert vut.A + (-vut.B) == (-vut.B) + vut.A == vut.A - vut.B
    assert vut.B + (-vut.A) == (-vut.A) + vut.B == vut.B - vut.A


def test_sub(vut: ValueUnderTest) -> None:
    assert vut.A - vut.A == MyInteger(0)
    assert (-vut.A) - (-vut.A) == MyInteger(0)

    assert MyInteger(0) - vut.A == -vut.A
    assert vut.A - MyInteger(0) == vut.A

    assert vut.A - vut.B == MyInteger(vut.a - vut.b)
    assert vut.B - vut.A == MyInteger(vut.b - vut.a)

    assert vut.A - (-vut.B) == vut.B - (-vut.A) == vut.A + vut.B
    assert -vut.A - vut.B == -vut.B - vut.A == -(vut.A + vut.B)

    assert (-vut.A) - (-vut.B) == vut.B - vut.A
    assert (-vut.B) - (-vut.A) == vut.A - vut.B


def test_mul(vut: ValueUnderTest) -> None:
    assert vut.A * MyInteger(0) == MyInteger(0)

    assert vut.A * vut.B == (-vut.A) * (-vut.B) == MyInteger(vut.a * vut.b)
    assert (-vut.A) * vut.B == vut.A * (-vut.B) == MyInteger(-vut.a * vut.b)


if __name__ == "__main__":
    pytest.main()
