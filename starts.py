from env import *

final_depth = 4
starting_boards = []
def generate_starting_boards():
    global starting_boards
    starting_boards=[]
    b = Board()
    start_recursive(b,BLACK,0)
    return starting_boards

def start_recursive(board, color, depth):
    if depth == final_depth:
        check = False
        # check if the board exist in the starting states, check will be True if the board exist
        for i in starting_boards:
            if i.board == board.board:
                check = True
                break
        
        # if the state does not exist, append the state, or else, do not append the state
        if check == False:
            starting_boards.append(board)
    
    else:
        # get all the board's next state
        list_of_boards = board.next_states(color)
        
        # switch color
        new_color = WHITE if color==BLACK else BLACK
        
        # recursive call for all the legal moves
        for b in list_of_boards:
            start_recursive(b, new_color, depth + 1)
