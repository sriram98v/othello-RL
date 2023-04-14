from env import *
from agents import *
import tqdm
from torch.utils.tensorboard import SummaryWriter

NUM_EPISODES = 500000
ALPHA = 0.01
GAMMA = 1
EPS = 0.1

writer=SummaryWriter("./log_dir/train/rand")

board = Board()
agent = Q_Agent(alpha=ALPHA, gamma=GAMMA, eps=EPS)
other = Rand_Agent()
agent_color = BLACK
other_color = WHITE

pbar = tqdm.tqdm(total=NUM_EPISODES)

num_wins = 0
num_losses = 0
num_draws = 0

for _ in range(NUM_EPISODES): 
    board.reset()
    total_loss = 0
    num_states = 0
    episode = []



    while True:        
        # get agent current state and legal moves
        agent_current_state, agent_legal_moves = board.get_current_state(), board.get_valid_moves(agent_color)

        # if agent has legal moves, select agent move and play
        if len(agent_legal_moves) != 0:
            agent_move = agent.get_move(agent_current_state, agent_legal_moves)
            board.play(agent_move,agent_color)
            learn_state, learn_move = deepcopy(agent_current_state), deepcopy(agent_move)

        # get other current state and legal moves
        other_current_state, other_legal_moves = board.get_current_state(), board.get_valid_moves(other_color)
        
        # if other has legal moves, select agent move and play
        if len(other_legal_moves) != 0:
            other_move = other.get_move(board.get_current_state(), other_legal_moves)
            board.play(other_move,other_color)
        episode.append((agent_current_state, other_current_state))
    
        if board.game_ended():
            white_count, black_count, empty_count = board.count_stones()
            if black_count>white_count:
                loss = agent.learn(learn_state, learn_move, 1, board.get_current_state(), board.get_valid_moves(agent_color), is_terminal=True)
                num_wins +=1
            elif black_count==white_count:
                loss = agent.learn(learn_state, learn_move, 0.5, board.get_current_state(), board.get_valid_moves(agent_color), is_terminal=True)
                num_draws += 1
            else:
                num_losses+=1
                loss = agent.learn(learn_state, learn_move, 0, board.get_current_state(), board.get_valid_moves(agent_color), is_terminal=True)
            total_loss += loss
            break

        else:
            if len(board.get_valid_moves(agent_color))>0:
                loss = agent.learn(learn_state, learn_move, 0, board.get_current_state(), board.get_valid_moves(agent_color))
                total_loss += loss
                num_states+=1

    #board.print_board()
    agent.decay_eps_linear(num_episodes=NUM_EPISODES)
    pbar.update(1)
    # pbar.set_description(f"loss {total_loss/num_states}")
    win_percent = '{:.2f}'.format(num_wins*100/(_+1))
    pbar.set_description(f"wins: {num_wins} draws: {num_draws} losses:{num_losses} win%:{win_percent} diff:{num_wins-num_losses}")
    writer.add_scalar('training loss vs rand',
                            total_loss/(num_states+1),
                            _)
    writer.add_scalars('Cummulative score',
                            {'num_wins': num_wins,
                             'num_draws': num_draws,
                             'num_losses': num_losses},
                            _)
    if _%1000==0:
        agent.export_model(f"./models/qagents/q_agent_vs_rand_{_}.pth")
agent.export_model(f"./models/qagents/q_agent_vs_rand_"+str(NUM_EPISODES)+".pth")
agent.export_model(f"./models/qagents/q_agent_vs_rand_final.pth")

