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

"""print('get current state')
print(board.get_current_state())
print()

# print(agent.play(board.get_current_state(), board.get_valid_moves(agent_color)))

current_state, legal_moves = board.get_current_state(), board.get_valid_moves(agent_color)
q_vals = agent.q_vals(current_state)
# print('q values: ' ,q_vals)
agent_move = agent.act(q_vals, legal_moves) #here we may have to change to epsilon policy, as we have implemented a greedy policy.

reward = board.play(agent_move,agent_color)

# print(board.get_current_state())
board.print_board()
print()

other_state, other_legal_moves = board.get_current_state(), board.get_valid_moves(other_color)
other_move = other.rand_move(other_legal_moves)
other_reward = board.play(other_move,other_color)

# print(board.get_current_state())
board.print_board()

next_state = board.get_current_state()
agent.learn(current_state, agent_move, reward, next_state)
"""
counter = 3
check = True
while check: 
    if board.game_ended():
        break
    else:
        if counter % 2 == 0:
            player = other
            color = other_color
        else:
            player = agent
            color = agent_color

    if color == 'WHITE':
        current_state, legal_moves = board.get_current_state(), board.get_valid_moves(color)
        other_move = other.rand_move(legal_moves)
        reward = board.play(other_move,color)
    else:
        current_state, legal_moves = board.get_current_state(), board.get_valid_moves(color)
        q_vals = agent.q_vals(current_state)
        agent_move = agent.act(q_vals, legal_moves)
        reward = board.play(agent_move,color)
    board.print_board()
    print()
    counter += 1