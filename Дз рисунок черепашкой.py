import turtle
import random

# Фон
screen = turtle.Screen()
screen.bgcolor("deep sky blue")
screen.title("Полянка с цветочками")
screen.setup(800, 600)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

def draw_cloud(x, y, size=1):
    cloud = turtle.Turtle()
    cloud.speed(0)
    cloud.hideturtle()
    cloud.penup()
    cloud.color("white")
    cloud.goto(x, y)
    
    cloud.begin_fill()
    for _ in range(4):
        cloud.circle(20 * size, 180)
        cloud.right(90)
    cloud.end_fill()

def draw_flower(x, y, color="red"):

    flower = turtle.Turtle()
    flower.speed(0)
    flower.hideturtle()
    flower.penup()
    
    # Ножка
    flower.goto(x, y)
    flower.color("green")
    flower.pendown()
    flower.setheading(90)
    flower.forward(40)
    
# Сердцевинка
    center_x = x
    center_y = y + 40  
    
    flower.penup()
    flower.goto(center_x, center_y)
    flower.color(color)
    

    for i in range(6):
        flower.penup()
        flower.goto(center_x, center_y)
        flower.setheading(i * 60)  
        flower.forward(15)
        flower.pendown()
        flower.begin_fill()
        flower.circle(10)
        flower.end_fill()
    

    flower.penup()
    flower.goto(center_x - 7, center_y - 5)  #Подгон центра (делалось просто на глаз)
    flower.color("yellow")
    flower.pendown()
    flower.begin_fill()
    flower.circle(9)
    flower.end_fill()

def draw_grass():
    grass = turtle.Turtle()
    grass.speed(0)
    grass.hideturtle()
    grass.penup()
    
    # Трава
    grass.color("lime green")
    grass.goto(-400, -100)
    grass.begin_fill()
    for _ in range(2):
        grass.forward(800)
        grass.right(90)
        grass.forward(200)
        grass.right(90)
    grass.end_fill()

#Список цветов, чтобы не накладывались
flower_positions = []

def is_valid_position(x, y, existing_positions, min_distance=80):

    for pos_x, pos_y in existing_positions:
        distance = ((x - pos_x)**2 + (y - pos_y)**2) ** 0.5
        if distance < min_distance:
            return False
    return True

# Трава
draw_grass()

# Облака
draw_cloud(-300, 180, 1.2)
draw_cloud(-100, 100, 1.3)
draw_cloud(150, 190, 1.5)
draw_cloud(300, 100, 0.8)

# Цветы
flower_colors = ["crimson", "deep pink", "purple", "orange", "white", "blue violet", "slate blue"]
flowers_drawn = 0
attempts = 0

while flowers_drawn < 15 and attempts < 100:
    x = random.randint(-350, 350)
    y = random.randint(-200, -100)  # Цветы ниже, на самой полянке
    
    if is_valid_position(x, y, flower_positions):
        color = random.choice(flower_colors)
        draw_flower(x, y, color)
        flower_positions.append((x, y))
        flowers_drawn += 1
    attempts += 1

# Солнце
sun = turtle.Turtle()
sun.speed(0)
sun.hideturtle()
sun.penup()
sun.goto(250, 170)
sun.color("yellow")
sun.pendown()
sun.begin_fill()
sun.circle(50)
sun.end_fill()

turtle.done()