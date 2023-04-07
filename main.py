from env import *
from agents import *
import tqdm
from torch.utils.tensorboard import SummaryWriter

NUM_EPISODES = 1000
ALPHA = 0.01
GAMMA = 1
EPS = 0.1

writer=SummaryWriter("./log_dir")

board = Board()
agent = Q_Agent(alpha=ALPHA, gamma=GAMMA, eps=EPS)
other = Rand_Agent()
agent_color = BLACK
other_color = WHITE

pbar = tqdm.tqdm(total=NUM_EPISODES)

num_wins = 0

for _ in range(NUM_EPISODES):
    board.reset()
    total_loss = 0
    num_states = 0

    while not board.game_ended(): 
        
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
        
        loss = agent.learn(agent_current_state, agent_move, 0, board.get_current_state())
        num_states+=1
        total_loss += loss
    
    white_count, black_count, empty_count = board.count_stones()
    if black_count>white_count:
        loss = agent.learn(agent_current_state, agent_move, 1, board.get_current_state())
    elif black_count==white_count:
        loss = agent.learn(agent_current_state, agent_move, 0, board.get_current_state())
    else:
        loss = agent.learn(agent_current_state, agent_move, -1, board.get_current_state())
    

    board.print_board()
    agent.decay_eps(num_episodes=NUM_EPISODES)
    pbar.update(1)
    pbar.set_description(f"loss {total_loss/num_states}")
    pbar.set_description(f"num wins {num_wins/(_+1)}")
    writer.add_scalar('training loss',
                            total_loss/num_states,
                            _)

    # if white_count > black_count:
    #     # pbar.write('agent win')
    # elif black_count > white_count:
    #     # pbar.write('other win')
    # else:
    #     # pbar.write('Draw game')