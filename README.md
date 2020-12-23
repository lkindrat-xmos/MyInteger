# MyInteger

The MyInteger class implements (almost) arbitrary length integers that can be added, subtracted, and multiplied. This was an exercise for my own amusement, but it also shows that you can write short, but powerful code using itertools and rich comparison methods. The code is also statically typed, and was developed using Test Driven Development.

To install:
```
git clone git@github.com:lkindrat-xmos/MyInteger.git
pip install -e MyInteger
```

Example:
```
>>> from my_integer import MyInteger
>>> n = MyInteger(2**65)
>>> n
36893488147419103232
>>> int(n) == 2**65
True
>>> n + n == n * MyInteger(2) == MyInteger(2**66)
True
```
