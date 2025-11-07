import turtle

window = turtle.Screen()
window.bgcolor("white")


turt = turtle.Turtle()
turt.turtlesize(5)
turt.pensize(5)
turt.shape("turtle")
turt.color("red")

turt.speed(1)
turt.penup()
turt.goto(-250, 0)
turt.pendown()
turt.fillcolor("red")
turt.begin_fill()
for i in range(5):
    turt.forward(500)
    turt.right(144)

turt.end_fill()

window.exitonclick()
