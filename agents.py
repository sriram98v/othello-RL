import torch
from function_approx import Q_Network
import numpy as np

class Agent:
    def __init__(self):
        self.q_func = Q_Network()

    def play(self, current_state, legal_moves):
        q_func_out = self.q_func(torch.from_numpy(current_state)).detach()
        values = []
        for move in legal_moves:
            values.append(q_func_out[move[0], move[1]])
        
        best_move = legal_moves[np.argmax(np.array(values))]

        return best_move