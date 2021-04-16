import turtle
import time
import random

'''
TO DO LIST

In queue:
- Collider between head and first body part
- Create a main menu
- Set different difficulties (Easy, Medium and High)
- Use json to save the scores instead of txt

Done:
- Add scoreboard
- Create division between scoreboard and play zone
- Add speed to the snake everytime that eats an apple
- Show "Game over" message
- Regulate speed increase
- Allow to use wasd and arrows to move
- Save highscore after execution
'''

'''
NOTES:
- Game zone = 600 x 600
- Speed increase: 1 ms -> -0'0025
'''

# Score reading
arch = open("score.txt", "r")
highscore = arch.readline()
if (highscore == ''):
	highscore = 0
else:
	highscore = int(highscore)

arch.close()

# General variables
postpone = 0.1 							# 1 milisecond
score = 0
level = "medium"

# Window config
wdw = turtle.Screen()
wdw.title("Snake Game 2020")
wdw.bgpic("background.gif")				# Background image. The image always need to be in format ".gif"
#wdw.bgcolor("black")
wdw.setup(width = 600, height = 700)	# Windows size
wdw.tracer(0)

# Shapes
wdw.register_shape("apple.gif")

# Snake head
head = turtle.Turtle()					# Object declaration
head.speed(0)							# Start speed of the object
head.shape("square")					# Gives to the object an square shape
head.penup()							# Eliminate the trace
head.goto(0, 0)							# Start at the point 0,0 of the screen
head.color("#088A29")					# Add to the object the selected color
head.direction = "stop"					# Create an state for the object

# Snake body
bodyParts = []

# Apple
apple = turtle.Turtle()				# Object declaration
apple.speed(0)						# Start speed of the object
apple.shape("apple.gif")			# Gives to the object an square shape
apple.penup()						# Eliminate the trace
apple.goto(0, 100)					# Start at the point 0,0 of the screen
apple.color("red")					# Add to the object the selected color

# Score text
text = turtle.Turtle()
text.speed(0)						# To print the text automatically when we open the program, not during
text.color("white")
text.penup()
text.hideturtle()
text.goto(0, 310)
text.write("Score: {}      Level: {}      Highscore: {}".format(score, level.title(), highscore), align = "center", font = ("Courier", 15, "normal"))

# Division text
division = turtle.Turtle()
division.speed(0)
division.color("white")
division.penup()
division.hideturtle()
division.goto(0, 300)
division.write("-----------------------------------------------------------------------", align = "center", font = ("Courier", 10, "normal"))

# Game Over text
gameover = turtle.Turtle()
gameover.speed(0)
gameover.color("white")
gameover.penup()
gameover.hideturtle()
gameover.goto(0, 200)



# Functions
def up():
	head.direction = "up"
def down():
	head.direction = "down"
def left():
	head.direction = "left"
def right():
	head.direction = "right"

def mov():
	if head.direction == "up":
		gameover.clear()			# Eliminate "Game over" text
		y = head.ycor()				# Get the actual "y" coordinates (turtle use a cartesian map)
		head.sety(y + 20)			# Set the new "y" coordinate position for the object
	if head.direction == "down":
		gameover.clear()
		y = head.ycor()
		head.sety(y - 20)
	if head.direction == "left":
		gameover.clear()
		x = head.xcor()				# Get the actual "x" coordinates (turtle use a cartesian map)
		head.setx(x - 20)			# Set the new "x" coordinate position for the object
	if head.direction == "right":
		gameover.clear()
		x = head.xcor()
		head.setx(x + 20)

# Not a really good solution
def save():
	arch = open("score.txt", "w");
	arch.write(str(highscore) + "\n")
	arch.close

# Keyboard
wdw.listen()						# Tells the window to be listening to the keyboard

wdw.onkeypress(up, "w")				# Call a function if a key is pressed (function, "key")
wdw.onkeypress(up, "Up")

wdw.onkeypress(down, "s")
wdw.onkeypress(down, "Down")

wdw.onkeypress(left, "a")
wdw.onkeypress(left, "Left")

wdw.onkeypress(right, "d")
wdw.onkeypress(right, "Right")

# Principal loop
while True:
	wdw.update()
	# Apple colides
	if head.distance(apple) < 20:	# Check the distance between two object (the square's measure is 20 pixels)
		# Spawn an apple in a random position
		x = (random.randint(- 280, 280) // 20) * 20
		y = (random.randint(- 300, 280) // 20) * 20
		apple.goto(x, y)

		postpone -= 0.0025							# Increase speed everytime that the snake eats an apple

		# Add new parts to the snake's body
		new_bodyPart = turtle.Turtle()				# Object declaration
		new_bodyPart.speed(0)						# Start speed of the object
		new_bodyPart.shape("square")				# Gives to the object an square shape
		new_bodyPart.penup()						# Eliminate the trace
		new_bodyPart.color("#01DF3A")				# Add to the object the selected color
		bodyParts.append(new_bodyPart)				# Add to the queue the new body part


		# Increase score
		score += 10

		if score > highscore:
			highscore = score

		save();

		text.clear()								# Erase the actual text in screen
		text.write("Score: {}      Level: Easy      Highscore: {}".format(score, highscore), align = "center", font = ("Courier", 15, "normal"))


	# Move snake body
	totalBody = len(bodyParts)						# Get number of objects in the list
	for index in range(totalBody - 1, 0, -1):
		x = bodyParts[index - 1].xcor()
		y = bodyParts[index - 1].ycor()
		bodyParts[index].goto(x, y)

	if totalBody > 0:
		x = head.xcor()
		y = head.ycor()
		bodyParts[0].goto(x, y)

	# Window colliders
	if head.xcor() > 280 or head.ycor() > 280 or head.xcor() < -280 or head.ycor() < -320:
		gameover.write("GAME OVER", align = "center", font = ("Courier", 40, "normal"))
		time.sleep(1)
		head.goto(0, 0)
		head.direction = "stop"

		apple.goto(0, 100)							# Restart apple

		postpone = 0.1								# Restart speed

		# Hide body parts
		for part in bodyParts:
			part.goto(-400, 400)

		bodyParts.clear()

		# Reset score
		score = 0
		text.clear()
		text.write("Score: {}      Level: Easy      Highscore: {}".format(score, highscore), align = "center", font = ("Courier", 15, "normal"))

	mov()

	# Body colliders
	for part in bodyParts:
		if part.distance(head) < 20:
			gameover.write("GAME OVER", align = "center", font = ("Courier", 40, "normal"))
			time.sleep(1)
			head.goto(0, 0)
			head.direction = "stop"

			apple.goto(0, 100)						# Restart apple

			postpone = 0.1							# Restart speed

			# Hide body parts
			for part in bodyParts:
				part.goto(-400, 400)

			bodyParts.clear()

			# Reset score
			score = 0
			text.clear()
			text.write("Score: {}      Level: Easy      Highscore: {}".format(score, highscore), align = "center", font = ("Courier", 15, "normal"))

	time.sleep(postpone)