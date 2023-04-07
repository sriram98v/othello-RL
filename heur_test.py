from env import *
from function_approx import Q_Network
import torch
from agents import *
import time

board = Board()
agent_color = BLACK
other_color = WHITE
agent = Rand_Agent()
other = Heu_Agent(color=agent_color)
NUM_EPISODES = 100

global move
while True:
    counter = 3
    check = True
    board.reset()
    print("new game")
    board.print_board()
    print("----------------------------")
    while check: 
        if board.game_ended():
            break
        else:
            if counter % 2 == 0:
                player = other
                color = other_color
                print("{} turn, {}".format(player,str(counter)))
            else:
                player = agent
                color = agent_color
                print("{} turn, {}".format(player,str(counter)))

        current_state, legal_moves = board.get_current_state(), board.get_valid_moves(color)

        if len(legal_moves)==0:
            counter += 1
            continue
        if color == WHITE:        
            move = agent.rand_move(legal_moves)
        else: # else randome
            move = other.heu_move(current_state,legal_moves)

        print("--- information on moves ---")
        print(type(move))
        print(move)
        print("--- end on moves ---")
        reward = board.play(move,color)
        print("color: {}".format(str(color)))
        print("updated board:")
        board.print_board()
        print()
        counter += 1
        time.sleep(1)