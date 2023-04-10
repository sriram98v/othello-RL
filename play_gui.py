from tkinter import *
from time import *
import numpy as np
from env import *
from agents import *


global screen
root = Tk()
screen = Canvas(root, width=500, height=600, background="#555",highlightthickness=0)
screen.pack()


# testing here
board = Board()
global player
global legal_moves

def reset_screen(root):
    screen.destroy()
    screen = Canvas(root, width=500, height=600, background="#555",highlightthickness=0)
    screen.pack()

def drawbackground():
    for i in range(7):
        lineShift = 50+50*(i+1)
        screen.create_line(50,lineShift,450,lineShift,fill="#111")
        screen.create_line(lineShift,50,lineShift,450,fill="#111")

def update(board):
    for x in range(8):
        for y in range(8):
            if board.board[x][y]== WHITE:
                screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")
    for x in range(8):
        for y in range(8):
            if board.board[x][y]== BLACK:
                screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
    
    screen.update()
    #time.sleep(0.1)

def play_game(black_agent, white_agent, board=None):
    if board==None:
        board=Board()
    board=deepcopy(board)
    update(board)
    while not board.game_ended(): 
        black_current_state, legal_moves = board.get_current_state(), board.get_valid_moves(BLACK)
        if len(legal_moves) != 0:
            black_move = black_agent.get_move(black_current_state, legal_moves)
            board.play(black_move, BLACK)  
            update(board)
        
        white_current_state, legal_moves = board.get_current_state(), board.get_valid_moves(WHITE)
        if len(legal_moves) != 0:
            white_move = white_agent.get_move(white_current_state, legal_moves)
            board.play(white_move, WHITE)
            update(board)

    white_count, black_count, _ = board.count_stones()
    if black_count>white_count:
            print("BLACK WIN")
            return "B"
    if black_count<white_count:
            print("WHITE WIN")
            return "W"
    print("DRAW")
    return "D"

def clickHandle(event):
    xMouse = event.x
    xMoune = event.y
    if player:
        x = int((event.x-50)/50)
        y = int((event.y-50)/50)
        if 0<=x<=7 and 0<=y<=7:
            if (x,y) in legal_moves:
                board.boardMove(x,y)


if __name__ == "__main__":
    drawbackground()
    screen.focus_set()
    root.wm_title("Othello")
    
    bw = 0
    ww = 0
    for _ in range(10):
        # BLACK, WHITE
        result = play_game(Rand_Agent(), Heu_Agent())
        if result == "W":
            ww+=1      
        if result == "B":
            bw+=1
        #reset_screen(root)
        print("black wins: {}".format(str(bw)))
        print("white wins: {}".format(str(ww)))

    root.mainloop()
    
    