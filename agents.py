import torch
from function_approx import Q_Network
import numpy as np
from helper import *
import random

class Q_Agent:
    def __init__(self):
        self.q_func = Q_Network()
        self.alpha = 1
        self.gamma = 1
        self.eps = 0
        self.loss_func = torch.nn.MSELoss()

    def act(self, q_vals, legal_moves): #This is a greedy policy, we can replace with epsilon later
        values = []
        for move in legal_moves:
            values.append(q_vals[pos_to_index(move[0], move[1])])
        
        if random.random() > self.eps:
            return legal_moves[np.argmax(np.array(values))]
        else:
            return legal_moves[np.random.randint(len(legal_moves))]

    def q_vals(self, state):
        return self.q_func(torch.from_numpy(state)).detach().numpy()
    
class Rand_Agent:
    def __init__(self):
        None
    
    def rand_move(self, legal_moves):
        '''
            @param curr_state --> current state of the board
            @param legalmoves --> list of moves

            @return a random moves from legalmoves
        '''
        return legal_moves[np.random.randint(len(legal_moves))]
