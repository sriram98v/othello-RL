from env import *
from function_approx import Q_Network
import torch
from agents import Agent

board = Board()
agent = Agent()
agent_color = BLACK
other_color = WHITE
NUM_EPISODES = 100

print(board.get_current_state())

print(agent.play(board.get_current_state(), board.get_valid_moves(agent_color)))

current_state, legal_moves = board.get_current_state(), board.get_valid_moves()
q_vals = agent.q_vals(current_state)
best_move = agent.greedy_move(current_state, legal_moves) #here we may have to change to epsilon policy, as we have implemented a greedy policy.