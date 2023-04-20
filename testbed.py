from env import *
from agents import *
from starts import * 
from matplotlib import pyplot as plt
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--a', type=str, required=True) # agent type.
parser.add_argument('--t', type=str, required=True) # trainer type.
parser.add_argument('--o', type=str, required=True) # opponent type.
parser.add_argument('--s', type=str, required=True) # save directory location.
# save directory argument
args = parser.parse_args() 

"""
usage:
python train_heu.py --a <agent> --t <trainer> --o <opponent> --s <path>
<agent>, choose {q,s}: 
    q --> q agent
    s --> sarsa agent
<trainer>, choose {h,r}:
    h --> heuristic trainer
    r --> random trainer
<opponent>, choose {h,r}:
    h --> heuristic trainer
    r --> random trainer
<path>:
    for loading model
    path up until before models/logs
"""


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
       
def play_testbed(agent, other, multiplier=1, both_colors=False):
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

            if both_colors:#If we want agent to play both colors
                result2=play_game(other, agent, board=b)
                if result2 == WHITE_WIN:
                    agent_wins  += 1
                elif result2 == BLACK_WIN:
                    agent_loss  += 1
                else:
                    agent_draws += 1
                games_played+=1

    return agent_wins, agent_loss, agent_draws, games_played

def model_score(AgentClass, OpponentClass, modeldir, multiplier=1):
    #ModelClass only supports Q_Agent for now
    print(modeldir)
    model = AgentClass(eps=0)
    model.import_model(modeldir)
    model.eval()
    other = OpponentClass() #Assuming it is fully deterministic
    w, _, _, g = play_testbed(model, other, multiplier)
    score = w/g

    return score

names = {
    "q": "qagent",
    "s": "sarsaagent",
    "r": "rand",
    "h": "heu",
}

def run_test_over_models(AgentClass, TrainerClass, OpponentClass, maxepisode=2000000, episodestep=5000):
    """
    agentname must be one of {'qagent', 'sarsaagent'} --> i.e. args.a must be "q" or "s"
    othername must be one of {'heu', 'rand'} --> i.e. args.t, and args.o must be "h" or "r"
    """
    indices = []
    scores  = []
    #need to check backslash or frontslash
    agentname = names[AgentClass]
    trainername = names[TrainerClass]
    opponentname = names[OpponentClass]

    dir=f'{args.s}/models/'+agentname+'/'+trainername+'/'
    fnames  = os.listdir(dir) 
    for idx in range(0,maxepisode+1, episodestep):
        """Cycle over maxepisode. We have a model at every episodestep episodes, but we don't need to sample that frequently"""
        fname = agentname+'_vs_'+trainername+'_'+str(idx)+'.pth'
        modeldir = dir+fname
        if fname not in fnames:
            print('FATAL ERROR, model not found', fname)
            exit()
        print('scoring ',modeldir)
        score = model_score(AgentClass, OpponentClass, modeldir)
        indices.append(idx)
        scores.append(score)
    indices = np.array(indices)
    scores  = np.array(scores)
    result=np.stack((indices, scores)).T

    outputdir = f'{args.s}/results/'
    outputfname = agentname+'_'+trainername+'_'+opponentname+'_scores.txt'
    np.savetxt(outputdir+outputfname, result)
    return indices, scores




run_test_over_models(args.a, args.t, args.o)

