import torch
from function_approx import Q_Network
import numpy as np
from helper import *
import random

class Q_Agent:
    def __init__(self):
        self.model = Q_Network()
        self.alpha = 1
        self.gamma = 1
        self.eps = 0
        self.loss_func = torch.nn.MSELoss()
        self.lr = 0.01
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1, momentum=0.9)

    def act(self, q_vals, legal_moves): #This is a greedy policy, we can replace with epsilon later
        values = []
        for move in legal_moves:
            values.append(q_vals[pos_to_index(move[0], move[1])])
        
        if random.random() > self.eps:
            return legal_moves[np.argmax(np.array(values))]
        else:
            return legal_moves[np.random.randint(len(legal_moves))]

    def q_vals(self, state):
        return self.model(torch.from_numpy(state)).detach().numpy()
    
    def learn(self, s, a, r, s_):
        """updates model for a single step

        Args:
            s (np.array): current state
            a (np.array): action
            r (float): reward
            s_ (np.array): next state

        Returns:
            None: None
        """
        self.optimizer.zero_grad()
        # Q-Learning target is Q*(S, A) <- r + γ max_a Q(S', a) 
        target = None # Compute expected value 
        current = None # compute actual value
        
        loss = self.loss(current, target)
        loss.backward() # Compute gradients
        self.optimizer.step() # Backpropagate error

    
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
