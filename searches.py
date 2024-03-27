import chess
import random 
# Format(can change): 
# func(board, heuristic) 

def random_legal_move(board: chess.Board, h, depth_limit):
    # No heuristic needed
    totMoves = []
    for move in board.legal_moves:
        totMoves.append(move)
    rand_move = random.choice(list(totMoves))
    chosen_move = chess.Move.from_uci(str(rand_move))
    return (chosen_move, 0)

def minimax(board: chess.Board, h, depth_limit, search_color, last_move = None):
    legal_moves = board.legal_moves 
    if depth_limit == 0 or board.is_game_over():
        return [chess.Move.from_uci(str(last_move)), h(board, search_color)]
    if board.turn == search_color: # Find best move for color
            max_eval = ["", -100000]
            for move in legal_moves:
                board.push(chess.Move.from_uci(str(move)))
                eval = minimax(board, h, depth_limit - 1, search_color, move)
                # move_val_pairs.append((move, minimax(board, h ,depth_limit - 1, search_color)))
                board.pop()
                eval[0] = chess.Move.from_uci(str(move))
                max_eval = find_max_pair([max_eval, eval])
            # print("max:",max_eval)
            return max_eval
    else: # Find worst move for color
            min_eval = ["", 100000]
            for move in legal_moves:
                board.push(chess.Move.from_uci(str(move)))
                eval = minimax(board, h, depth_limit - 1, search_color, move)
                # move_val_pairs.append((move, minimax(board, h ,depth_limit - 1, search_color)))
                board.pop()
                eval[0] = chess.Move.from_uci(str(move))
                min_eval = find_min_pair([min_eval, eval])
            # print("min",min_eval)
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
    # print("Max",max_pairs)
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
        # print("Equal", min_pairs)
        choice = random.choice(min_pairs)
        # print("Chose", choice)
        return choice
    else:
        return min_pairs[0]