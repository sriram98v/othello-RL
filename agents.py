import torch
from function_approx import Q_Network
import numpy as np
from helper import *

class Agent:
    def __init__(self):
        self.q_func = Q_Network()
        self.alpha = 1
        self.gamma = 1
        self.loss_func = torch.nn.MSELoss()

    def greedy_move(self, q_vals, legal_moves): #This is a greedy policy, we can replace with epsilon later
        values = []
        print(legal_moves)
        for move in legal_moves:
            values.append(q_vals[pos_to_index(move[0], move[1])])
        
        best_move = legal_moves[np.argmax(np.array(values))]
        print(values)
        print(legal_moves)

        return best_move

    def q_vals(self, state):
        return self.q_func(torch.from_numpy(state)).detach().numpy()
    
    # def learn(self, prev_state, current_state, next_state, action):
    #     q_new = 