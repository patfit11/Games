########################################################################################
# This code is for Snake in python
# Created November 21, 2019
# Edited:
########################################################################################

# import packages
import random
import curses

########################################################################################
# Create the basic screen to play on
########################################################################################

# use curses to initialize the screen
s = curses.initscr()
# set the cursor to 0 so it doesn't show up on the screen
curses.curs_set(0)
# get the height and width of the screen
sh, sw = s.getmaxyx()
# create new screen using the height and width
w = curses.newwin(sh, sw, 0, 0)
# accept keypad input
w.keypad(1)
# refresh the screen every 100 milliseconds
w.timeout(100)


########################################################################################
# Create the snake
########################################################################################

# define snake's initial position and body size
snk_x = sw/4
snk_y = sh/2
snake = [
	[snk_y, snk_x],
	[snk_y, snk_x-1],
	[snk_y, snk_x-2]
]


########################################################################################
# create the food
########################################################################################

# assign the foods initial position
food = [sh/2, sw/2]
# add the food to the screen and make is a 'Lantern'
w.addch(int(food[0]), int(food[1]), curses.ACS_LANTERN)
# define the snake's initial direction
key = curses.KEY_RIGHT


########################################################################################
# start infinite loop for the snake's movement
########################################################################################
while True:
	# get the next key
	next_key = w.getch()
	# either nothing or the next key
	key = key if next_key == -1 else next_key

	# check to see if the player has lost - top / sides/ itself
	if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
		curses.endwin()
		quit()

	# determine the new head of the snake after grabbing a 'Lantern'
	new_head = [snake[0][0], snake[0][1]]

	# define the movement 
	if key == curses.KEY_DOWN:
		new_head[0] += 1
	if key == curses.KEY_UP:
		new_head[0] -= 1
	if key == curses.KEY_LEFT:
		new_head[1] -= 1
	if key == curses.KEY_RIGHT:
		new_head[1] += 1

	# inset the new head of the snake
	snake.insert(0, new_head)

	# determine what to do when the snake has grabbed the 'Lantern'
	if snake[0] == food:
		food = None

		# create a new food on-screen once the previously has been captured
		while food is None:
			nf = [
				random.randint(1, sh-1),
				random.randint(1, sw-1)
			]
			food = nf if nf not in snake else None
		w.addch(int(food[0]), int(food[1]), curses.ACS_LANTERN)
	
	# add another piece to the tail of the snake after collecting a 'Lantern'
	else:
		tail = snake.pop()
		w.addch(int(tail[0]), int(tail[1]), ' ')

	w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)











































