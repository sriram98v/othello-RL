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

    def eval(self):
        self.model.eval()

    def train(self):
        self.model.train()

    def init_normal(self, m):
        if type(m) == torch.nn.Linear:
            torch.nn.init.uniform_(m.weight, -0.5, 0.5)
            torch.nn.init.uniform_(m.bias, -0.5, 0.5)

class Q_Agent(Trainable_Agent):
    def __init__(self, alpha=0.01, gamma=1, eps=0.1, device=torch.device('cpu')):
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
        self.eps_original = eps
        self.loss_func = torch.nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.alpha, momentum=0.9)
        self.device = device

        self.model.apply(self.init_normal)
        self.model.to(self.device)

    def eval(self):
        self.model.eval()

    def train(self):
        self.model.train()

    def get_move(self, state, legal_moves):
        """Chooses an action given a current state using an epsilon greedy policy

        Args:
            q_vals (np.array): q values of all actions for a state
            legal_moves (list): all legal moves on the board

        Returns:
            tuple: xy position on the board
        """
        if self.device!=torch.device('cpu'):
            q_vals = self.model(torch.from_numpy(state).to(device=self.device)).detach().cpu().numpy()
        else:
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

    def learn(self, s, a, r, s_, valid_moves_s_, is_terminal=False):
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
        current = self.model(torch.from_numpy(s)) # Compute actual value
        target = torch.clone(current).detach()
        s_a_values = [self.model(torch.from_numpy(s_)).detach()[pos_to_index(*i)].item() for i in valid_moves_s_]
        if is_terminal:
            target[pos_to_index(a[0], a[1])] = r
        else:
            target[pos_to_index(a[0], a[1])] = r + self.gamma*max(s_a_values)


        loss = current.shape[0]*self.loss_func(current, target)
        loss.backward() # Compute gradients
        self.optimizer.step() # Backpropagate error

        return loss.item()
    
    def decay_eps_linear(self, num_episodes):
        self.eps -= self.eps_original/num_episodes

    def export_model(self, fname="./q_model.pth"):
        torch.save(self.model.state_dict(), fname)

    def import_model(self, fname="./q_model.pth"):
        print(f"Loaded model from {fname}")
        self.model.load_state_dict(torch.load(fname))
        # print(self.model.hidden2.weight)
        # print(f"loaded from {fname}")

class Sarsa_Agent(Trainable_Agent):
    def __init__(self, alpha=0.01, gamma=1, eps=0.1, device=torch.device('cpu')):
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
        self.eps_original = eps
        self.loss_func = torch.nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.alpha, momentum=0.9)
        self.device = device
        self.next_action = None

        self.model.apply(self.init_normal)
        self.model.to(self.device)

    def eval(self):
        """Freezes NN
        """
        self.model.eval()

    def train(self):
        self.model.train()

    def get_move(self, state, legal_moves):
        """Chooses an action given a current state using an epsilon greedy policy

        Args:
            q_vals (np.array): q values of all actions for a state
            legal_moves (list): all legal moves on the board

        Returns:
            tuple: xy position on the board
        """
        if self.next_action:
            return self.next_action
        else:
            if self.device!=torch.device('cpu'):
                q_vals = self.model(torch.from_numpy(state).to(device=self.device)).detach().cpu().numpy()
            else:
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

    def learn(self, s, a, r, s_, valid_moves_s_, is_terminal=False):
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
        self.next_action = None

        # Q-Learning target is Q*(S, A) <- r + γ max_a Q(S', a)
        current = self.model(torch.from_numpy(s)) # Compute actual value
        target = torch.clone(current).detach()
        #s_a_values = [self.model(torch.from_numpy(s_)).detach()[pos_to_index(*i)].item() for i in valid_moves_s_]  -> from Q agent
        s_a_values = self.q_vals(s_)
        if is_terminal:
            target[pos_to_index(a[0], a[1])] = r
        else:
            self.next_action = self.get_move(s_, valid_moves_s_)
            # target[pos_to_index(a[0], a[1])] = r + self.gamma*max(s_a_values)  -> from Q agent
            # move = self.get_move(self, s_, valid_moves_s_)
            idx = pos_to_index(self.next_action[0], self.next_action[1])
            target[pos_to_index(a[0], a[1])] = r + self.gamma*s_a_values[idx]
        
        loss = current.shape[0]*self.loss_func(current, target)
        loss.backward() # Compute gradients
        self.optimizer.step() # Backpropagate error

        return loss.item()
    
    def decay_eps_linear(self, num_episodes):
        """decays epsilon linearly for 1 episode

        Args:
            num_episodes (int): total number of episodes
        """
        self.eps -= self.eps_original/num_episodes

    def update_eps(self, n, num_episodes):
        """decays epsilon for n iterations

        Args:
            n (int): num iterations
            num_episodes (int): total number of episodes
        """
        for _ in range(n):
            self.decay_eps_linear(num_episodes)

    def export_model(self, fname="./q_model.pth"):
        torch.save(self.model.state_dict(), fname)

    def import_model(self, fname="./q_model.pth"):
        print(f"Loaded model from {fname}")
        self.model.load_state_dict(torch.load(fname))
        # print(self.model.hidden2.weight)
        # print(f"loaded from {fname}")


HEUR =  [[100,  -25, 10, 5, 5, 10, -25, 100],
        [-25,   -25, 2, 2, 2, 2, -25, -25],
        [10,    2, 5, 1, 1, 5, 2, 10],
        [5, 2, 1, 2, 2, 1, 2, 5],
        [5, 2, 1, 2, 2, 1, 2, 5],
        [10, 2, 5, 1, 1, 5, 2, 10],
        [-25, -25, 2, 2, 2, 2, -25, -25],
        [100, -25, 10, 5, 5, 10, -25, 100]]
class Heu_Agent(Agent):
    def __init__(self, heuristic=HEUR, color=WHITE, eps=0.0):
        '''
        input:
            @param heuristics --> heuristics of hard coded (2D grid)
            @param color --> color pieces of the heuristic agent
        '''
        self.color = color
        self.heur = copy.deepcopy(heuristic)
        self.eps = eps

    def eval_function(self, curr_board):
        '''
        calculate the sum of c_i*w_i using heur and current board information
        input:
            @param curr_board --> current board, where self pieces = 1, opponent = -1, empty = 0
        output:
            @return result --> an integer after the calculation
        '''
        eval_score = 0
        mul = np.multiply(curr_board, self.heur)
        eval_score = np.sum(mul)
        return eval_score

    def get_move(self, state, legal_moves):
        '''
        input:
            @param state --> a 1D state of the current board
            @param legalmoves --> list of moves
        output:
            @return best_move --> select the best move out of all legal move for the move that return highest eval_function
        '''
        state_2d = state.reshape((8,8))
        b = Board()
        b.board = list(state_2d)    # list(<array>) should change it to list of list. double check.

        eval_max = -np.inf    # eval_max to store the highest eval
        best_move = None

        # below does not work because we still do not know which move resulted which action, hence
        # unable to return "best" move

        #print("------------- TEST STATE -------------")
        #print("possible legal move:")
        #print(legal_moves)
        for move in legal_moves:
            #print("trying out move for {}".format(str(self.color)))
            #print(move)
            b_after_action = Board()    # new board to prevent referencing game board
            b_after_action.board = copy.deepcopy(b.board)
            #print("cloned board")
            #b_after_action.print_board()
            temp=b_after_action.get_valid_moves(self.color)
            b_after_action.play(move, self.color)       # play a move on a copy board (prevent reference that might mess with actual)
            #print("cloned board after move")
            #b_after_action.print_board()

            convert_board = copy.deepcopy(b_after_action.board)

            #def print_board(board):
            #    for l in board:
            #        print(l)

            # WHITE = -1, BLACK = 1 in env.py
            # so if color is WHITE, we need to invert to feed to eval_function
            #print("before convert")
            #print_board(convert_board)
            if self.color == WHITE:
                convert_board=invert_board(copy.deepcopy(b_after_action.board))
            #print("after convert")
            #print_board(convert_board)

            # check the new eval score for new board
            new_eval = self.eval_function(convert_board)
            #print("eval function for such board:")
            #print(new_eval)
            if  new_eval > eval_max:
                eval_max = new_eval
                best_move = move
        return eps_greedy(best_move, legal_moves=legal_moves, EPSILON=self.eps)

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

class Human(Agent):
    def get_move(self, state, legal_moves):
        '''
        input:
            @param state --> current state of the board
            @param legalmoves --> list of moves
        output:
            @return a random moves from legalmoves (chosen from human)
        '''

        print("select one(index) of all legal moves")   # show all legal moves for player
        for i in range(len(legal_moves)):
            print("[{}]. {}".format(str(i),str(legal_moves[i])))


        print(state.reshape((8,8)))

        a = input()     # human player chooses an action (chooses the index)

        if int(a) not in range(len(legal_moves)):
            print("invalid move selected.")     #check selected index is within list length    

        return legal_moves[int(a)]
