# Stoa Calculator
> Stoa Calculator is a powerdul calculator that have everything you need for calculating anything!

[![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/stoacalculator/)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![Downloads](https://static.pepy.tech/personalized-badge/stoacalculator?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/stoacalculator)

This calculator can do from basic aritmethic to advanced calculus, we will be releasing more
updates and adding more features, our goal is to make this calculator the most powerful calculator
ever to exist.

![](https://raw.githubusercontent.com/jorgeeldis/StoaCalculator/main/header.png)

## Installation
<!--
OS X & Linux:

```sh
npm install my-crazy-module --save
```
-->

Windows:

```sh
python3 -m pip install stoacalculator
```

## Usage example

We can use Stoa Calculator in many ways, one of the best ways is to use it for trigonometry and calculus.

```py
import stoacalculator

# Basic Aritmethic
stoacalculator.add_numbers(1,2)
stoacalculator.substract_numbers(1,2)
stoacalculator.multiply_numbers(1,2)
stoacalculator.divide_numbers(1,2)
stoacalculator.pow_numbers(1,2)
stoacalculator.sqr_root(1,2)

# Trigonometry
stoacalculator.sin(4)
stoacalculator.cos(4)
stoacalculator.tan(4)
stoacalculator.asin(4)
stoacalculator.acos(4)
stoacalculator.atan(4)

# Basic Geometry
stoacalculator.areacircle(25)
stoacalculator.areatriangle(25,10,30)
stoacalculator.areasquare(50,10)
stoacalculator.arearectangle(25,10)

# Basic Statistics
stoacalculator.mean(list)
stoacalculator.mode(list)
stoacalculator.median(list)

# Plotting
# We recommend to always use 100 linearly spaced numbers 
x = np.linspace(-5, 5, 100)
# For trigonometry we recommend to use this configuration
x = np.linspace(-np.pi,np.pi,100)
linearformula = 2*x
quadraticformula = 1*x+x**2
cubicformula = 6*x+x**3
trigonometricformula = np.sin(x)
exponentialformula = np.exp(x)
stoacalculator.linearplot(x, linearformula)
stoacalculator.quadraticplot(x, quadraticformula)
stoacalculator.cubicplot(x, cubicformula)
stoacalculator.trigonometricplot(x, trigonometricformula)
stoacalculator.exponentialplot(x, exponentialformula)
stoacalculator.biplot(x, trigonometricformula, exponentialformula)
```

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

You'll only need for now the matlibplot, math and statistic modules from python, this program already import all those modules. So you won't need to import them in your code.


```sh
pip install math
pip install statistics
pip install matlibplot
```

## Release History
* 0.0.9 (13/08/21)
    * Ninth Release `(Plotting Calculator from Linear to Exponential Equations)`
* 0.0.8 (13/08/21)
    * Eighth Release `Performance improvements & bug fixes`
* 0.0.7 (13/08/21)
    * Seventh Release `Performance improvements & bug fixes`
* 0.0.6 (13/08/21)
    * Sixth Release `(Basic Statistics (Mean, Mode, Median))`
* 0.0.5 (13/08/21)
    * Fifth Release `(Basic Geometry (Area of basic shapes))`
* 0.0.4 (13/08/21)
    * Fourth Release `(Trigonometric Functions)`
* 0.0.3 (12/08/21)
    * Third Release `(Square Root)`
* 0.0.2 (27/03/21)
    * Second Release `(Powers/Exponents)`
* 0.0.1 (27/03/21)
    * First Release `(Addition, Substraction, Multiplication, Division)`

## Meta

Jorge Eldis ~ [@jorgeeldis](https://twitter.com/jorgeeldis) ~ jorgeeldisg30@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/jorgeeldis/](https://github.com/jorgeeldis/)


## Contributing

1. Fork it (<https://github.com/jorgeeldis/StoaCalculator/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


<!-- Markdown link & img dfn's -->
[wiki]: https://github.com/yourname/yourproject/wiki
