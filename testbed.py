from env import *
from agents import *
from starts import * 

def play_game(black_agent, white_agent, board=None):
    if board==None:
        board=Board()
    board=deepcopy(board)
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


            result2=play_game(other, agent, board=b)
            if result2 == WHITE_WIN:
                agent_wins  += 1
            elif result2 == BLACK_WIN:
                agent_loss  += 1
            else:
                agent_draws += 1
            games_played+=1

    return agent_wins, agent_loss, agent_draws, games_played


#result = play_testbed(Rand_Agent(), Rand_Agent())
result = play_testbed(Human(), Human())

print(result)
