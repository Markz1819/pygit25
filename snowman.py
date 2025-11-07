import turtle

window = turtle.Screen()
snowman = turtle.Turtle()

window.title("Snowman")
window.bgcolor("white")
snowman.speed(10)

snowman.penup()
snowman.goto(0, -450)
snowman.pendown()
snowman.circle(200)

snowman.penup()
snowman.goto(0, -100)
snowman.pendown()
snowman.circle(150)

snowman.penup()
snowman.goto(0, 200)
snowman.pendown()
snowman.circle(100)

window.exitonclick()
