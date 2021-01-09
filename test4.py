#   a113_tower.py
#   Modify this code in VS Code to alternate the colors of the 
#   floors every three floors
import turtle as trtl

painter = trtl.Turtle()
painter.speed(0)
painter.pensize(5)

# starting location of the tower
x = -150
y = -150

# height of tower and a counter for each floor
num_floors = 63
floor = 0

# iterate
color=0
colors=["red","green","orange"]
while floor < num_floors:
  # set placement and color of turtle
  painter.penup()
  painter.goto(x, y)
  painter.color(colors[color])
  y = y + 5 # location of next floor
  floor = floor + 1
   
  #draw the floor
  painter.pendown()
  painter.forward(50)
  color=color+1
  if color>=3:
    color=0

wn = trtl.Screen()
wn.mainloop()