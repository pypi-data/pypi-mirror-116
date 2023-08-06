import math
import statistics

# simple operations, basic aritmethic


def add_numbers(num1, num2):
    print(num1 + num2)


def substract_numbers(num1, num2):
    print(num1 - num2)


def multiply_numbers(num1, num2):
    print(num1 * num2)


def divide_numbers(num1, num2):
    print(num1 / num2)


def pow_numbers(num1, num2):
    print(num1 ** num2)


def sqr_root(num1):
    print(math.sqrt(num1))


# trigonometry
def sin(num1):
    print(math.sin(num1))


def cos(num1):
    print(math.cos(num1))


def tan(num1):
    print(math.tan(num1))


def acos(num1):
    print(math.acos(num1))


def asin(num1):
    print(math.asin(num1))


def atan(num1):
    print(math.atan(num1))

# Geometry circle (add radius)


def areacircle(num1):
    area = math.pi * num1 * num1
    print(area)

# Geometry rectangle (add height and width)


def arearectangle(num1, num2):
    area = num1 * num2
    print(area)

# Geometry square (add sides)


def areasquare(num1):
    area = num1 * num1
    print(area)

# Geometry triangle (add all sides)


def areasquare(num1, num2, num3):
    semiperimeter = (num1 + num2 + num3) / 2
    area = (semiperimeter*(semiperimeter-num1) *
            (semiperimeter-num2)*(semiperimeter-num3)) ** 0.5
    print(area)

