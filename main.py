from env import *
from function_approx import Q_Network
import torch
from agents import *

board = Board()
agent = Q_Agent()
other = Rand_Agent()
agent_color = BLACK
other_color = WHITE
NUM_EPISODES = 100

print('get current state')
print(board.get_current_state())
print()

# print(agent.play(board.get_current_state(), board.get_valid_moves(agent_color)))

current_state, legal_moves = board.get_current_state(), board.get_valid_moves(agent_color)
q_vals = agent.q_vals(current_state)
# print('q values: ' ,q_vals)
agent_move = agent.greedy_move(q_vals, legal_moves) #here we may have to change to epsilon policy, as we have implemented a greedy policy.

board.play(agent_move,agent_color)

# print(board.get_current_state())
print(board.print_board())

current_state, legal_moves = board.get_current_state(), board.get_valid_moves(other_color)
other_move = other.rand_move(legal_moves)
board.play(other_move,other_color)

# print(board.get_current_state())
print(board.print_board())