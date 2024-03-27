import random
import chess
import heuristics as h
import searches as f

"""
color: "Black" or "White"
f: search function
h: heuristic function
autobattle (Auto to false): True / False
"""
def play_game(color, f, h, depth_limit, autobattle = False):
    board = chess.Board()
    if color in "BlackblackFalsefalse":
        print("Chose Black")
        side = False
    else:
        print("Chose White")
        side = True
    num_of_moves = 0
    while True:
        if board.is_game_over():
            print("Game Over")
            print(board)
            print(board.outcome)
            print(num_of_moves, "Moves")
            if board.outcome().winner == False:
                print("Black Wins")
            elif board.outcome().winner == True:
                print("White Wins")
            break
        if board.turn == side: # Your turn
            if not autobattle:
                print("Your Turn!")
                val = h(board, side)
                print("Cur Board Rating:", val)
                print(f"{board}")
                l_moves =[]
                for move in board.legal_moves:
                    l_moves.append(move.uci())
                print(f"Legal Moves:\n {l_moves}")
                while True:
                    move = input("Enter Move: ")
                    if move in l_moves:
                        break
                    else:
                        print("Illegal move, try again.")
                print(board)
            else: # Autobattle with chosen heuristic until game over
                move = f(board, h, depth_limit, board.turn)[0]
                print('Your side chose', move.uci())
                print(board)
            uci_move = chess.Move.from_uci(str(move))
            board.push(uci_move)
            num_of_moves += 1
        else: # Bot's turn
            print("Generating opponent's next move")
            agents_move = f(board, h, depth_limit, board.turn)[0]
            # print_legal_moves(board)
            print(f"Opponent chose: {agents_move.uci()}")
            print("Opponent's cur pos rating", h(board, not side))
            board.push(agents_move)

####################################
########## Misc Functions ##########
####################################


def print_legal_moves(board):
    moves = []
    for move in board.legal_moves:
        moves.append(move.uci())
    print(moves)









if __name__ == "__main__":
    # Example: 
    # Color:
    # play_game(color, search_func, heuristic, depth_limit, autobattle?)
    play_game("Black", f.minimax, h.grants_heuristic, 3, True)
    '''
    board = chess.Board()
    for i in range(20):
        board.push(random_legal_move(board, 1,1))
    print(minimax(board,grants_heuristic,3, board.turn))
    print(board)
    moves = []
    for move in board.legal_moves:
        moves.append(move.uci())
    print(moves)
    '''