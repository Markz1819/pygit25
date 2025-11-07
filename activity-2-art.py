import math
import turtle

window = turtle.Screen()

turt = turtle.Turtle()
turt.speed(0)

# This code is supposed to recursively draw an infinite inscribing of regular polygons
# To achieve this, we must first dicuss some math.
# For any regular polygon, there are two circles of note: the circumscribed circle and the inscribed circle(incircle)
# The circumscribed circle is the circle that passes through all the vertices of the polygon, on the outside
# The incircle is the circle that is tangent to all the sides of the polygon, on the inside
#
# If we wish to continuously inscribe regular polygons within each other, we can observe that the centers of all circles
# will be the same point, the center of the polygon.
# And the incircle of one regular polygon is the circumcircle of the next regular polygon.
# Thus, if we find a way to calculate the radius of the incircle for any given polygon,
# we can determine the position of the next polygon

π = math.pi  #


# get the color string based on n for the rainbow thingy.
def rainbow_color(n):
    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    return colors[n % len(colors)]


# n is the number of sides of the polygon
# side_length is the length of each side of the polygon
# This uses the formula for the inradius of a regular polygon
def inradius(n: int, side_length: float) -> float:
    return side_length / (2 * math.tan(π / n))


# n is the number of sides of the polygon
# side_length is the length of each side of the polygon
# This uses the formula for the circumradius of a regular polygon
def circumradius(n: int, side_length: float) -> float:
    return side_length / (2 * math.sin(π / n))


# n is the number of sides of the polygon
# side_length is the length of each side of the polygon
# Draws a polygon with the given n sides and side length, at a given center coord
def draw_polygon(n: int, side_length: float, center: tuple[float, float]):
    radius = inradius(n, side_length)

    angle = 360 / n

    color = rainbow_color(n)  # Set the rainbow color
    turt.pencolor(color)

    turt.penup()
    turt.goto(center[0], center[1] - radius)
    turt.back(side_length / 2)
    turt.pendown()

    for _ in range(n):  # Draw the polygon! (I know theres a turtle method for it, idc)
        turt.forward(side_length)
        turt.left(angle)

    turt.penup()  # Draw the incircle for the current polygon
    turt.goto(center[0], center[1] - radius)
    turt.pendown()
    turt.circle(radius)

    # turt.right(angle / 2)


# n is the number of polygons
# side_length is the initial side length of the polygon
# center is the center of all polygons
# Draws regular polygons recursively inscribed in each other


def recur(n: int, side_length: float, center: tuple[float, float]) -> float:
    if n < 0:  # Termination
        return side_length

    side_length = recur(
        n - 1, side_length, center
    )  # Recursively go to n = 1 to make use of the initial side length, then base every side length off that

    draw_polygon(
        n + 3, side_length, center
    )  # Draw the polygon & circle for the current n
    return (side_length * math.sin(π / (n + 4))) / math.tan(
        π / (n + 3)
    )  # Return the next side length to use


_ = recur(100, 1000, (0, -100))  # Starting call


window.exitonclick()
