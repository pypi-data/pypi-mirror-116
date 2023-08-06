# Geometry circle (add radius)
def areacircle(num1):
    area = math.pi * num1 * num1
    print("The area of the cirlce is: " + str(area))

# Geometry rectangle (add height and width)


def arearectangle(num1, num2):
    area = num1 * num2
    print("The area of the Rectangle is: " + str(area))

# Geometry square (add sides)


def areasquare(num1):
    area = num1 * num1
    print("The area of the square is: " + str(area))

# Geometry triangle (add all sides)


def areasquare(num1, num2, num3):
    semiperimeter = (num1 + num2 + num3) / 2
    area = (semiperimeter*(semiperimeter-num1) *
            (semiperimeter-num2)*(semiperimeter-num3)) ** 0.5
    print("The area of the triangle is: " + str(area))
