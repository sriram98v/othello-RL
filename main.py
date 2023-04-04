from env import *
from function_approx import Q_Network
import torch
from agents import Agent

board = Board()
agent = Agent()
agent_color = BLACK
other_color = WHITE
print(board.get_current_state())

agent.play(board.get_current_state(), board.get_valid_moves(agent_color))

