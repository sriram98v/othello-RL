from env import *
from agents import *
from starts import * 
from matplotlib import pyplot as plt
import os

ALPHA = 0.01
GAMMA = 1
EPS = 0.1

def play_game(black_agent, white_agent, board=None):
    if board==None:
        board=Board()
    
    board=deepcopy(board)
    #board.print_board()
    while not board.game_ended(): 
        black_current_state, black_legal_moves = board.get_current_state(), board.get_valid_moves(BLACK)
        if len(black_legal_moves) != 0:
            black_move = black_agent.get_move(black_current_state, black_legal_moves)
            board.play(black_move, BLACK)
        
        white_current_state, white_legal_moves = board.get_current_state(), board.get_valid_moves(WHITE)
        if len(white_legal_moves) != 0:
            white_move = white_agent.get_move(white_current_state, white_legal_moves)
            board.play(white_move, WHITE)

    white_count, black_count, _ = board.count_stones()
    if black_count>white_count:
        return BLACK_WIN
    if black_count<white_count:
        return WHITE_WIN
    return DRAW
       

def play_testbed(agent, other, multiplier=1):
    """multiplier is for random agents"""
    starting_boards=generate_starting_boards()
    agent_wins   = 0
    agent_loss   = 0
    agent_draws  = 0
    games_played = 0

    for i in range(multiplier):
        for b in starting_boards:
            result1=play_game(agent, other, board=b)
            if result1 == BLACK_WIN:
                agent_wins  += 1
            elif result1 == WHITE_WIN:
                agent_loss  += 1
            else:
                agent_draws += 1
            games_played+=1
            #input()


            # result2=play_game(other, agent, board=b)
            # if result2 == WHITE_WIN:
            #     agent_wins  += 1
            # elif result2 == BLACK_WIN:
            #     agent_loss  += 1
            # else:
            #     agent_draws += 1
            # games_played+=1

    return agent_wins, agent_loss, agent_draws, games_played

def run_test_over_models(dir):
    q_Agent = Q_Agent(alpha=ALPHA, gamma=GAMMA, eps=0)
    indices = []
    scores  = []
    fnames  = os.listdir(dir) 
    #for idx in range(0,2000000,1000):
    for idx in range(0,2000000,100000):
        """Cycle over 2,000,000 million with steps of 20,000. We have a model at every 1,000 episodes, but we don't need to sample that frequently"""
        fname = 'q_agent_vs_rand_'+str(idx)+'.pth'
        fdir = dir+fname
        if fname not in fnames:
            break
        print(fdir)
        
        q_Agent.import_model(fdir)
        w, _, _, g = play_testbed(q_Agent, Rand_Agent(), 100)
        
        indices.append(idx)
        scores.append(w/g)
        if idx>100000:
            break

    return indices, scores

def plotter():
    dir='./models/qagents/'
    indices, scores = run_test_over_models(dir)
    print(indices)
    print(scores)
    plt.plot(indices, scores)
    plt.show()


plotter()

# q_Agent = Q_Agent(alpha=ALPHA, gamma=GAMMA, eps=0.0)
# q_Agent.import_model("models/qagents/q_agent_vs_rand.pth")
#result = play_testbed(Heu_Agent(), Rand_Agent(), 100)

#print(result)

# q_Agent = Q_Agent(alpha=ALPHA, gamma=GAMMA, eps=0.0)
# q_Agent.import_model("q_agent_vs_rand_prev.pth")
# result = play_testbed(q_Agent, Rand_Agent(), 100)

# print(result)

