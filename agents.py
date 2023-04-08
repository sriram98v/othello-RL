import torch
from function_approx import Q_Network
import numpy as np
from helper import *
import random
from env import *
import copy

class Agent:
    def get_move(self, state, legal_moves):
        pass

class Trainable_Agent(Agent):
    def learn(self, s, a, r, s_):
        pass

    def export_model(self, fname):
        pass

    def import_model(self, fname):
        pass

class Q_Agent(Trainable_Agent):
    def __init__(self, alpha=0.01, gamma=1, eps=0.1):
        """_summary_

        Args:
            alpha (float, optional): learning rate of the NN. Defaults to 0.01.
            gamma (int, optional): discount factor. Defaults to 1.
            eps (float, optional): exploration parameter. Defaults to 0.1.
        """
        self.model = Q_Network()
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps # change in future
        self.loss_func = torch.nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.alpha, momentum=0.9)

    def get_move(self, state, legal_moves):
        """Chooses an action given a current state using an epsilon greedy policy

        Args:
            q_vals (np.array): q values of all actions for a state
            legal_moves (list): all legal moves on the board

        Returns:
            tuple: xy position on the board
        """
        q_vals = self.model(torch.from_numpy(state)).detach().numpy()
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
            loss: float
        """
        self.optimizer.zero_grad()
        # Q-Learning target is Q*(S, A) <- r + γ max_a Q(S', a)
        target = r + self.gamma*(torch.max(self.model(torch.from_numpy(s_)))) # Compute expected value
        current = self.model(torch.from_numpy(s))[pos_to_index(a[0], a[1])] # Compute actual value


        loss = self.loss_func(current, target)
        loss.backward() # Compute gradients
        self.optimizer.step() # Backpropagate error

        return loss.item()
    
    def decay_eps(self, num_episodes):
        self.eps -= self.eps/num_episodes

    def export_model(self, fname="./q_model.pth"):
        torch.save(self.model.state_dict(), fname)

    def import_model(self, fname="./q_model.pth"):
        self.model.load_state_dict(torch.load(fname))


HEUR =  [[100, -25, 10, 5, 5, 10, -25, -100],
        [-25, -25, 2, 2, 2, 2, -25, -25],
        [10, 2, 5, 1, 1, 5, 2, 10],
        [5, 2, 1, 2, 2, 1, 2, 5],
        [5, 2, 1, 2, 2, 1, 2, 5],
        [10, 2, 5, 1, 1, 5, 2, 10],
        [-25, -25, 2, 2, 2, 2, -25, -25],
        [100, -25, 10, 5, 5, 10, -25, 100]]
class Heu_Agent(Agent):
    def __init__(self, heuristic=HEUR, color=WHITE):
        '''
        input:
            @param heuristics --> heuristics of hard coded (2D grid)
            @param color --> color pieces of the heuristic agent
        '''
        self.color = color
        self.heur = heuristic

    def eval_function(self, curr_board):
        '''
        calculate the sum of c_i*w_i using heur and current board information
        input:
            @param curr_board --> current board, where self pieces = 1, opponent = -1, empty = 0
        output:
            @return result --> an integer after the calculation
        '''
        eval_score = 0
        mul = np.multiply(curr_board, HEUR)
        eval_score = np.sum(mul)
        return eval_score

    def get_move(self, state, legal_moves):
        '''
        input:
            @param state --> a 1D state of the current board
        output:
            @return best_move --> select the best move out of all legal move for the move that return highest eval_function
        '''
        state_2d = state.reshape((8,8))
        b = Board()
        b.board = list(state_2d)    # list(<array>) should change it to list of list. double check.

        valid_moves = b.get_valid_moves(self.color)
        eval_max = 0    # eval_max to store the highest eval
        best_move = None

        for move in valid_moves:
            b_after_action = Board()    # new board to prevent referencing game board
            b_after_action.board = copy.deepcopy(b.board)
            b_after_action.play(move, self.color)       # play a move on a copy board (prevent reference that might mess with actual)

            convert_board = copy.deepcopy(b_after_action.board)
            # WHITE = -1, BLACK = 1 in env.py
            # so if color is WHITE, we need to invert to feed to eval_function
            if self.color == WHITE:
                convert_board=invert_board(copy.deepcopy(b_after_action.board))

            new_eval = self.eval_function(convert_board)
            if  new_eval > eval_max:
                eval_max = new_eval
                best_move = move

        return best_move

class Rand_Agent(Agent):
    def __init__(self):
        None

    def get_move(self, state, legal_moves):
        '''
        input:
            @param curr_state --> current state of the board
            @param legalmoves --> list of moves
        output:
            @return a random moves from legalmoves
        '''
        return legal_moves[np.random.randint(len(legal_moves))]
