# This program determines the type of triangle based on the lengths of its sides.
def calling(x, y, z):
    if x == y == z:
        print("The triangle is equilateral")
    elif x == y or y == z or x == z:
        print("The triangle is isosceles")
    else:
        print("The triangle is scalene")

x = float(input("Enter a length of a triangle: "))
y = float(input("Enter a width of a triangle: "))
z= float(input("Enter a height of a triangle: "))
calling(x, y, z)