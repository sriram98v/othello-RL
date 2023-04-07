from env import *

final_depth = 4
starting_states = []

def list_of_starting_state():

    b = Board()
    start_recursive(b,BLACK,0)
    return starting_states

def start_recursive(board, color, depth):
    if depth == final_depth:
        check = False
        # check if the board exist in the starting states
        for i in starting_states:
            if i.board == board.board:
                check = True
                break
        # if the state does not exist, append the state, or else, append it to the starting states list
        if check == False:
            starting_states.append(board)
    else:
        # get all the board's next state
        list_of_boards = board.next_states(color)
        
        # switch color
        if color == BLACK:
            new_color = WHITE
        else:
            new_color = BLACK
        
        # recursive call for all the legal moves
        for b in list_of_boards:
            start_recursive(b,new_color,depth + 1)

list_of_starting_state()