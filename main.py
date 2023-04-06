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
    counter = 3
    check = True
    board.reset()
    while check: 
        if board.game_ended():
            break
        else:
            if counter % 2 == 0:
                player = other
                color = other_color
            else:
                player = agent
                color = agent_color
        current_state, legal_moves = board.get_current_state(), board.get_valid_moves(color)
        if len(legal_moves)==0:
            counter += 1
            continue
        if color == 'WHITE':        
            move = other.rand_move(legal_moves)
        else:
            move = agent.act(current_state, legal_moves)

        reward = board.play(move,color)
        # print(color)
        # board.print_board()
        # print()
        counter += 1
    white_count, black_count, empty_count = board.count_stones()
    pbar.update(1)

    # if white_count > black_count:
    #     # pbar.write('agent win')
    # elif black_count > white_count:
    #     # pbar.write('other win')
    # else:
    #     # pbar.write('Draw game')