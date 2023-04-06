import torch
from function_approx import Q_Network
import numpy as np
from helper import *
import random
from env import *
import copy

class Q_Agent:
    def __init__(self):
        self.model = Q_Network()
        self.alpha = 1
        self.gamma = 1
        self.eps = 0.9 # change in future
        self.loss_func = torch.nn.MSELoss()
        self.lr = 0.01
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1, momentum=0.9)

    def act(self, q_vals, legal_moves):
        """Chooses an action given a current state using an epsilon greedy policy

        Args:
            q_vals (np.array): q values of all actions for a state
            legal_moves (list): all legal moves on the board

        Returns:
            tuple: xy position on the board
        """
        values = []
        # print(len(legal_moves))
        for move in legal_moves:
            values.append(q_vals[pos_to_index(move[0], move[1])])
        
        if random.random() > self.eps:
            return legal_moves[np.argmax(np.array(values))]
        else:
            return legal_moves[np.random.randint(len(legal_moves))]

    def q_vals(self, state):
        """Return q values of all actions given a state

        Args:
            state (np.array): State

        Returns:
            np.array: q_values
        """
        return self.model(torch.from_numpy(state)).detach().numpy()
    
    def learn(self, s, a, r, s_):
        """updates model for a single step

        Args:
            s (np.array): current state
            a (tuple): position on board
            r (float): reward
            s_ (np.array): next state

        Returns:
            None: None
        """
        self.optimizer.zero_grad()
        # Q-Learning target is Q*(S, A) <- r + γ max_a Q(S', a) 
        target = r + self.gamma*(torch.max(self.model(torch.from_numpy(s_)))) # Compute expected value 
        current = self.model(torch.from_numpy(s))[pos_to_index(a[0], a[1])] # compute actual value

        
        loss = self.loss_func(current, target)
        loss.backward() # Compute gradients
        self.optimizer.step() # Backpropagate error

    def export_model(self, fname):
        torch.save(self.model.state_dict(), fname)

HEUR =  [[100, -25, 10, 5, 5, 10, -25, 100],
        [-25, -25, 2, 2, 2, 2, -25, -25],
        [10, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0],
        [10, 0, 0, 0, 0, 0, 0, 0],
        [-25, -25, 0, 0, 0, 0, 0, 0],
        [100, -25, 0, 0, 0, 0, 0, 0]]

class Heu_Agent:
    def __init__(self, heuristic=HEUR, color=WHITE):
        '''
            @param heuristics --> heuristics of hard coded (2D grid)
            @param color --> color pieces of the heuristic agent
        '''
        self.color = WHITE
        self.heur = heuristic

    def eval_function(self, curr_board):
        '''
        calculate the sum of c_i*w_i using heur and current board information

            @param curr_board --> current board 

            @return result --> an integer after the calculation
        '''

    def heu_move(self, state):
        '''
            @param state --> a 1D state of the current board
        '''
        state_2d = state.reshape((8,8))
        b = Board()
        # TODO: make state_2d to list of list
        b.board = state_2d

        valid_moves = b.get_valid_moves(self.color)
        eval_max = 0    # eval_max to store the highest eval:
        global best_move
        for move in valid_moves:
            b_after_action = Board()
            b_after_action.board = copy.deepcopy(b.board)
            b_after_action.play(move, self.color)       # play a move on a copy board (prevent reference that might mess with actual)
            # TODO: new varaible convert_board, convert board so that the integer matches the color
            new_eval = self.eval_function(convert_board)
            if  new_eval > eval_max:
                eval_max = new_eval
                best_move = move

        return best_move

    
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
