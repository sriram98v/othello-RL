# script for 673 project, Michael, Sriram, Srijita, Benjamin, Yee

# GUI template file

# Script reference from 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Othello Program
# John Fish
# Updated from May 29, 2015 - June 26, 2015
#
# Has both basic AI (random decision) as well as
# educated AI (minimax).
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy
from env import *

#Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=600, background="#222",highlightthickness=0)
screen.pack()



	#Updating the board to the screen
    # GUI related
    # curr_player is int of -1 or 1
def update(oldboard, board, curr_player):
		screen.delete("highlight")
		screen.delete("tile")
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if board.board[x][y]==WHITE:
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

				elif board.board[x][y]==BLACK:
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		#Animation of new tiles
		screen.update(oldboard, board, curr_player)
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if board.board[x][y] != oldboard[x][y] and board.board[x][y]==WHITE:
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update(oldboard, board, curr_player)
						screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update(oldboard, board, curr_player)
						screen.delete("animated")
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
					screen.update(oldboard, board, curr_player)

				elif board.board[x][y] != oldboard[x][y] and board.board[x][y]==WHITE:
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update(oldboard, board, curr_player)
						screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update(oldboard, board, curr_player)
						screen.delete("animated")

					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
					screen.update(oldboard, board, curr_player)

		#Drawing of highlight circles
		for x in range(8):
			for y in range(8):
				legalmoves=board.get_valid_moves(curr_player)
				
				# debug only
				print(type(legalmoves[0]))
				if (x,y) in legalmoves:
						screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#008000",outline="#008000")

	#METHOD: Draws scoreboard to screen
    # GUI related
def drawScoreBoard(board):
		w_count, b_count , _ = board.count_stones()

		global moves
		#Deleting prior score elements
		screen.delete("score")

        # count

		#Scoring based on number of tiles
		"""player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y]=="w":
					player_score+=1
				elif self.array[x][y]=="b":
					computer_score+=1

		if self.player==0:
			player_colour = "green"
			computer_colour = "gray"
		else:
			player_colour = "gray"
			computer_colour = "green"

		screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
		screen.create_oval(380,540,400,560,fill=computer_colour,outline=computer_colour)"""

		#Pushing text to screen
		screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=w_count)
		screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=b_count)

		# Unsure of what "moves" is
        # moves = player_score+computer_score
		
# GUI related
#Method for drawing the gridlines
def drawGridBackground(outline=False):
	#If we want an outline on the board then draw one
	if outline:
		screen.create_rectangle(50,50,450,450,outline="#111")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		screen.create_line(50,lineShift,450,lineShift,fill="#111")

		#Vertical line
		screen.create_line(lineShift,50,lineShift,450,fill="#111")

	screen.update()

# GUI related
#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
	global depth
	xMouse = event.x
	yMouse = event.y
	if running:
		if xMouse>=450 and yMouse<=50:
			root.destroy()
		elif xMouse<=50 and yMouse<=50:
			playGame()
		else:
			#Is it the player's turn?
            # TODO: check if it is player's turn, how to modify this to automatic

			# if board.player==0:
				#Delete the highlights
				x = int((event.x-50)/50)
				y = int((event.y-50)/50)
				#Determine the grid index for where the mouse was clicked
				
				#If the click is inside the bounds and the move is valid, move to that location
				if 0<=x<=7 and 0<=y<=7:
					# check valid move
					if valid(board.array,board.player,x,y):
						board.boardMove(x,y)
	else:
		#Difficulty clicking
		if 300<=yMouse<=350:
			#One star
			if 25<=xMouse<=155:
				depth = 1
				playGame()
			#Two star
			elif 180<=xMouse<=310:
				depth = 4
				playGame()
			#Three star
			elif 335<=xMouse<=465:
				depth = 6
				playGame()

# GUI related
def keyHandle(event):
	symbol = event.keysym
	if symbol.lower()=="r":
		playGame()
	elif symbol.lower()=="q":
		root.destroy()

# GUI related
def create_buttons():
		#Restart button
		#Background/shadow
		screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
		screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")

		#Arrow
		screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline="white",extent=300)
		screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")

		#Quit button
		#Background/shadow
		screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
		screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")
		#"X"
		screen.create_line(455,5,495,45,fill="white",width="3")
		screen.create_line(495,5,455,45,fill="white",width="3")

# GUI related
def runGame():
	global running
	running = False
	#Title and shadow
	screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
	screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")
	
	#Creating the play buttons
	"""screen.create_rectangle(25+155*1, 310, 155+155*1, 355, fill="#000", outline="#000")
	screen.create_rectangle(25+155*1, 300, 155+155*1, 350, fill="#111", outline="#111")
	screen.create_text(25+(+1)*130/(1+2)+155*1,326,anchor="c",text="play", font=("Consolas", 25),fill="#b29600")"""

	for i in range(3):
		#Background
		screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
		screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")

		spacing = 130/(i+2)
		for x in range(i+1):
			#Star with double shadow
			screen.create_text(25+(x+1)*spacing+155*i,326,anchor="c",text="\u2605", font=("Consolas", 25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="\u2605", font=("Consolas",25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="\u2605", font=("Consolas", 25),fill="#ffd700")

	# debug
	print("DEBUG 2")

	screen.update()

# GUI related
def playGame():
	global board, running
	running = True
	screen.delete(ALL)
	#create_buttons()
	board = 0

	#Draw the background
	drawGridBackground()

	#Create the board and update it
	board = Board()
	update(board, board, BLACK)
	global curr_player
	while not board.game_ended():
		oldboard = board.board
		curr_player = BLACK
		b_curr_state,b_legal_moves = board.get_current_state(), board.get_valid_moves(BLACK)
		if len(b_legal_moves)!=0:
			black_move = black_agent.get_move(black_current_state, black_legal_moves)
			board.play(black_move, BLACK)
			update(oldboard, board, curr_player)
			
		oldboard = board.board
		curr_player = WHITE
		w_curr_state,w_legal_moves = board.get_current_state(), board.get_valid_moves(WHITE)
		if len(b_legal_moves)!=0:
			white_move = white_agent.get_move(black_current_state, black_legal_moves)
			board.play(black_move, BLACK)
			update(oldboard, board, curr_player)

# runGame()
playGame()

"""#Binding, setting
screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()"""

#Run forever
root.wm_title("Othello")
root.mainloop()
