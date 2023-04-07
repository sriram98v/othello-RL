from env import *
from agents import *
import tqdm

NUM_EPISODES = 10000
ALPHA = 0.01
GAMMA = 1
EPS = 0.1

board = Board()
agent = Q_Agent(alpha=ALPHA, gamma=GAMMA, eps=EPS)
other = Rand_Agent()
agent_color = BLACK
other_color = WHITE

pbar = tqdm.tqdm(total=NUM_EPISODES)

for _ in range(NUM_EPISODES):
    board.reset()

    while True: 
        # end game, both player does not have any legal moves
        if board.game_ended():
            break
        
        # get agent current state and legal moves
        agent_current_state, agent_legal_moves = board.get_current_state(), board.get_valid_moves(agent_color)
        
        # if agent has legal moves, select agent move and play
        if len(agent_legal_moves) != 0:
            agent_move = agent.act(agent_current_state, agent_legal_moves)
            agent_reward = board.play(agent_move,agent_color)
        
        # get other current state and legal moves
        other_current_state, other_legal_moves = board.get_current_state(), board.get_valid_moves(other_color)
        
        # if other has legal moves, select agent move and play
        if len(other_legal_moves) != 0:
            other_move = other.rand_move(other_legal_moves)
            other_reward = board.play(other_move,other_color)
    
    white_count, black_count, empty_count = board.count_stones()

    pbar.update(1)

    # if white_count > black_count:
    #     # pbar.write('agent win')
    # elif black_count > white_count:
    #     # pbar.write('other win')
    # else:
    #     # pbar.write('Draw game')