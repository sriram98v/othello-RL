from env import *
from agents import *

def play_game(black_agent, whtie_agent, board=None):
    if board==None:
        board=Board()
    
    while not board.game_ended(): 
        black_current_state, black_legal_moves = board.get_current_state(), board.get_valid_moves(BLACK)
        if len(black_legal_moves) != 0:
            black_move = black_agent.get_move(black_current_state, black_legal_moves)
            board.play(black_move, BLACK)
        
        white_current_state, white_legal_moves = board.get_current_state(), board.get_valid_moves(WHITE)
        if len(white_legal_moves) != 0:
            white_move = whtie_agent.get_move(white_current_state, white_legal_moves)
            board.play(white_move, WHITE)

        white_count, black_count, empty_count = board.count_stones()
        if black_count>white_count:
            pass
        elif black_count==white_count:
            pass
        else:
            pass







agent = Q_Agent()
agent.import_model()


