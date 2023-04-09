#!/usr/bin/env python
""" game.py Humberto Henrique Campos Pinheiro
Game logic.
"""

from copy import deepcopy
import numpy as np
from helper import *
import time

EMPTY = 0
BLACK = 1
WHITE = -1

DRAW = 0
BLACK_WIN = 1
WHITE_WIN = -1

class Board:

    """ Rules of the game """

    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[3][3] = WHITE
        self.board[4][4] = WHITE
        self.valid_moves = []

    def reset(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[3][3] = WHITE
        self.board[4][4] = WHITE
        self.valid_moves = []

    def __getitem__(self, i, j):
        return self.board[i][j]

    def lookup(self, row, column, color):
        """Returns the possible positions that there exists at least one
        straight (horizontal, vertical, or diagonal) line between the
        piece specified by (row, column, color) and another piece of
        the same color.

        """
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        places = []

        if row < 0 or row > 7 or column < 0 or column > 7:
            return places

        # For each direction search for possible positions to put a piece.
        for (x, y) in [
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
                (-1, -1)
            ]:
            pos = self.check_direction(row, column, x, y, other)
            if pos:
                places.append(pos)
        return places

    def check_direction(self, row, column, row_add, column_add, other_color):
        i = row + row_add
        j = column + column_add
        if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
            i += row_add
            j += column_add
            while (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other_color):
                i += row_add
                j += column_add
            if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == EMPTY):
                return (i, j)

    def get_valid_moves(self, color):
        """Get the avaiable positions to put a piece of the given color. For
        each piece of the given color we search its neighbours,
        searching for pieces of the other color to determine if is
        possible to make a move. This method must be called before
        apply_move.
        """

        if color == BLACK:
            other = WHITE
        else:
            other = BLACK

        places = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    places = places + self.lookup(i, j, color)

        places = list(set(places))
        self.valid_moves = places
        return places

    def play(self, move, color):
        """ Determine if the move is correct and apply the changes in the game.
        """
        current_board = deepcopy(self.board)
        if move in self.valid_moves:
            self.board[move[0]][move[1]] = color
            for i in range(1, 9):
                self.flip(i, move, color)
        new_board = deepcopy(self.board)
        if self.game_ended():
            white, black, empty = self.count_stones()
            if white==black:
                return 0.5
            elif white>black:
                return 1.0
            else:
                return 0.0
        else:
            return 0.0 # replace with reward func in future



    def flip(self, direction, position, color):
        """ Flips (capturates) the pieces of the given color in the given direction
        (1=North,2=Northeast...) from position. """

        if direction == 1:
            # north
            row_inc = -1
            col_inc = 0
        elif direction == 2:
            # northeast
            row_inc = -1
            col_inc = 1
        elif direction == 3:
            # east
            row_inc = 0
            col_inc = 1
        elif direction == 4:
            # southeast
            row_inc = 1
            col_inc = 1
        elif direction == 5:
            # south
            row_inc = 1
            col_inc = 0
        elif direction == 6:
            # southwest
            row_inc = 1
            col_inc = -1
        elif direction == 7:
            # west
            row_inc = 0
            col_inc = -1
        elif direction == 8:
            # northwest
            row_inc = -1
            col_inc = -1

        places = []     # pieces to flip
        i = position[0] + row_inc
        j = position[1] + col_inc

        if color == WHITE:
            other = BLACK
        else:
            other = WHITE

        if i in range(8) and j in range(8) and self.board[i][j] == other:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + row_inc
            j = j + col_inc
            while i in range(8) and j in range(8) and self.board[i][j] == other:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + row_inc
                j = j + col_inc
            if i in range(8) and j in range(8) and self.board[i][j] == color:
                # found a piece of the right color to flip the pieces between
                for pos in places:
                    # flips
                    self.board[pos[0]][pos[1]] = color

    def get_changes(self):
        """ Return black and white counters. """

        whites, blacks, empty = self.count_stones()

        return (self.board, blacks, whites)

    def game_ended(self):
        """ Is the game ended? """
        # board full or wipeout
        whites, blacks, empty = self.count_stones()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # no valid moves for both players
        if self.get_valid_moves(BLACK) == [] and \
        self.get_valid_moves(WHITE) == []:
            return True

        return False

    def print_board(self):
        for i in range(8):
            print(i, ' |', end=' ')
            for j in range(8):
                if self.board[i][j] == BLACK:
                    print('B', end=' ')
                elif self.board[i][j] == WHITE:
                    print('W', end=' ')
                else:
                    print(' ', end=' ')
                print('|', end=' ')
            print()

    def count_stones(self):
        """ Returns the number of white pieces, black pieces and empty squares, in
        this order.
        """
        whites = 0
        blacks = 0
        empty = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == WHITE:
                    whites += 1
                elif self.board[i][j] == BLACK:
                    blacks += 1
                else:
                    empty += 1
        return whites, blacks, empty

    def next_states(self, color):
        """Given a player's color return all the boards resulting from moves
        that this player cand do. It's implemented as an iterator.
        """
        valid_moves = self.get_valid_moves(color)
        for move in valid_moves:
            newBoard = deepcopy(self)
            newBoard.play(move, color)
            yield newBoard

    def get_current_state(self):
        return np.array(deepcopy(self.board), dtype=np.float32).flatten()
    
    # test update for GUI
    	#Updating the board to the screen
    # GUI related
    def update(self, screen):
        screen.delete("highlight")
        screen.delete("tile")
        for x in range(8):
            for y in range(8):
				#Could replace the circles with images later, if I want
                if self.oldarray[x][y]=="w":
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

                elif self.oldarray[x][y]=="b":
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		#Animation of new tiles
        screen.update()
        for x in range(8):
            for y in range(8):
				#Could replace the circles with images later, if I want
                if self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="w":
                    screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
                    for i in range(21):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                        if i%3==0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")
					#Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                        if i%3==0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
                    screen.update()
                
                elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="b":
                    screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
                    for i in range(21):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                        if i%3==0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")
					#Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                        screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                        if i%3==0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")

                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
                    screen.update()

		#Drawing of highlight circles
        for x in range(8):
            for y in range(8):
                if self.player == 0:
					# TODO: valid checks for valid move
                    if valid(self.array,self.player,x,y):
                        screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#008000",outline="#008000")

        if not self.won:
			#Draw the scoreboard and update the screen
            self.drawScoreBoard()
            screen.update()
			#If the computer is AI, make a move
            if self.player==1:
                startTime = time()
                self.oldarray = self.array
                alphaBetaResult = self.alphaBeta(self.array,depth,-float("inf"),float("inf"),1)
                self.array = alphaBetaResult[1]
                
                if len(alphaBetaResult)==3:
                    position = alphaBetaResult[2]
                    self.oldarray[position[0]][position[1]]="b"
                self.player = 1-self.player
                deltaTime = round((time()-startTime)*100)/100
                if deltaTime<2:
                    sleep(2-deltaTime)
                    nodes = 0
				#Player must pass?
                # self.passTest()
        else:
            screen.create_text(250,550,anchor="c",font=("Consolas",15), text="The game is done!")