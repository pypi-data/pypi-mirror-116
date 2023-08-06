from sympy import *
import numpy as np

x = Symbol('x')


def integrals(function):
    print(integrate(function))

integrals(sin(x)+exp(x)*log(x))
