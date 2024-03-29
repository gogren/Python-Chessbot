import chess
import random 
import math


def random_legal_move(board: chess.Board, h, depth_limit, search_color):
    # No heuristic needed
    totMoves = []
    for move in board.legal_moves:
        totMoves.append(move)
    rand_move = random.choice(list(totMoves))
    chosen_move = chess.Move.from_uci(str(rand_move))
    return (chosen_move, 0)

def minimax(board: chess.Board, h, depth_limit, search_color, last_move = None):
    if depth_limit == 0 or board.is_game_over():
        return [chess.Move.from_uci(str(last_move)), h(board, search_color)]
    legal_moves = board.legal_moves 
    if board.turn == search_color: # Find best move for color
            max_eval = ["", -100000]
            for move in legal_moves:
                board.push(chess.Move.from_uci(str(move)))
                eval = minimax(board, h, depth_limit - 1, search_color, move)                
                board.pop()
                eval[0] = chess.Move.from_uci(str(move))
                max_eval = find_max_pair([max_eval, eval])        
            return max_eval
    else: # Find worst move for color
            min_eval = ["", 100000]
            for move in legal_moves:
                board.push(chess.Move.from_uci(str(move)))
                eval = minimax(board, h, depth_limit - 1, search_color, move)                
                board.pop()
                eval[0] = chess.Move.from_uci(str(move))
                min_eval = find_min_pair([min_eval, eval])
            return min_eval
    
    
def abminimax(board: chess.Board, h, depth_limit, search_color):
     if depth_limit == 0 or board.is_game_over():
          print("Bad depth limit / Game is over")
          return None
     legal_moves = board.legal_moves     
     max_eval = ["", -math.inf]
     for move in legal_moves:
        # Maximize here
        board.push(chess.Move.from_uci(str(move)))
        eval = abminimax_help(board, h, depth_limit - 1, search_color, move, -math.inf, math.inf)            
        board.pop()
        move_uci = chess.Move.from_uci(str(move))
        max_eval = find_max_pair([max_eval, [chess.Move.from_uci(str(move)), eval]])
     print(max_eval)
     return max_eval

# Might do this with regular minimax too
def abminimax_help(board: chess.Board, h, depth_limit, search_color, last_move, alpha, beta):
    if depth_limit == 0 or board.is_game_over():
        return h(board, search_color)
    legal_moves = board.legal_moves 
    if board.turn == search_color: # Find best move for color
            max_eval = -math.inf
            for move in legal_moves:
                board.push(chess.Move.from_uci(str(move)))
                eval = abminimax_help(board, h, depth_limit - 1, search_color, last_move, alpha, beta)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                     break
            return max_eval
    else: # Find worst move for color
            min_eval = math.inf
            for move in legal_moves:
                board.push(chess.Move.from_uci(str(move)))
                eval = abminimax_help(board, h, depth_limit - 1, search_color, last_move, alpha, beta)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                     break
            return min_eval   


### HELPER FUNCTIONS ###
# Finds max pair from (move, value) pairs, if multple maxes, choses a random one
def find_max_pair(pairs):
    max = -1000000
    max_pairs = []
    for pair in pairs:
        if pair[1] > max:
            max_pairs = [pair]
            max = pair[1]
        elif pair[1] == max:
            max_pairs.append(pair)
    if len(max_pairs) == 0:
        print("find_max_pair has length 0")
    elif len(max_pairs) > 1:
        choice = random.choice(max_pairs)
        return choice
    else:
        return max_pairs[0]
    
# Finds min pair from (move, value) pairs, if multple mins, choses a random one
def find_min_pair(pairs):
    min = 1000000
    min_pairs = []
    for pair in pairs:
        if pair[1] < min:
            min_pairs = [pair]
            min = pair[1]
        elif pair[1] == min:
            min_pairs.append(pair)
    if len(min_pairs) == 0:
        print("find_max_pair has length 0")
    elif len(min_pairs) > 1:        
        choice = random.choice(min_pairs)        
        return choice
    else:
        return min_pairs[0]