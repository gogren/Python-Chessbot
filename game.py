import random
import pygame
import chess
import heuristics as h
import searches as f
import gui as g

pygame.init()
"""
color: "Black" or "White"
f: search function opponent will use
h: heuristic function
autobattle (Auto to false): True / False
f2: Only if autobattle is True, seach function you're autobattler will use
h2: ^^, heuristic your autobattler will use
"""
def play_game(color, f, h, depth_limit, autobattle = False, f2 = None, h2 = None):
    board = chess.Board()
    print(board)
    if color in "BlackblackFalsefalse":
        print("Chose Black")
        side = False
        opponent = "White"
        you = "Black"
    else:
        print("Chose White")
        side = True
        opponent = "Black"
        you = "White"
    num_of_moves = 0
    if autobattle and f2 == None:
        f2 = f
    if autobattle and h2 == None:
        h2 = h
    while True:
        g.show(board.board_fen(), board)
        # Checks for checkmate, stalemate, insuffecient material, 75 move rule, and five-fold repition 
        if board.is_game_over():
            print("Game Over")
            print(board)
            print(board.outcome())
            print(num_of_moves, "Moves")
            if board.outcome().winner == False:
                print("Black Wins")
            elif board.outcome().winner == True:
                print("White Wins")
            while True:
                end = input('Enter "end" to be done:')
                if end == "end":
                    break
                print()
            break
        if board.turn == side: # Your turn
            if not autobattle:
                print("Your Turn!")
                val = h(board, side)
                print("Cur Board Rating:", val)
                l_moves =[]
                for move in board.legal_moves:
                    l_moves.append(move.uci())
                print(f"Legal Moves:\n {l_moves}")
                while True:
                    move = ""
                    first_move = True
                    second_move = True
                    # Get first click
                    while first_move:
                        event_list = pygame.event.get()
                        for event in event_list:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                move += g.get_square(event.pos)
                                first_move = False
                                print(move)
                    # Get second click
                    ojbs = g.show_selected_moves(board, move)
                    while second_move:
                        event_list = pygame.event.get()
                        for event in event_list:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                move += g.get_square(event.pos)
                                second_move = False  
                    # Redraw everything to remove selected squares, can't figure out how to do transparent squares
                    g.show(board.board_fen(), board)
                    move = g.check_for_promotion(board, move)
                    print(move)
                    # Check if move is valid
                    if move in l_moves:
                        break
                    else:
                        print("Illegal move, try again.")
            else: # Autobattle with chosen heuristic until game over
                print(f"Generating {you}'s next move...")
                move_pair = f2(board, h2, depth_limit, board.turn)
                move = move_pair[0]
                print('Your side chose', move.uci())
                print("Your Position Score:", move_pair[1])
            uci_move = chess.Move.from_uci(str(move))
            board.push(uci_move)
            print(board)
            num_of_moves += 1
            print("Number of Moves:")
        else: # Bot's turn
            print(f"Generating {opponent}'s next move...")
            agents_move_pair = f(board, h, depth_limit, board.turn)
            agents_move = agents_move_pair[0]
            print(f"Opponent chose: {agents_move.uci()}")
            print("Opponent's Position Score:", agents_move_pair[1])
            board.push(agents_move)
            print(board)

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
    # The following function, the user's color is chosen as black, the agent opponent will use f.minimax and h.grants_heuristic
    # for generating its move using a depth of 3 in its searches, autobattle is set to true, so no user input for user's color
    # Optionally, f.random_legal_move is used here for the user's side's search, also a heuristic can also be added for user searching. 

    # play_game("Black", f.minimax, h.grants_heuristic, 3, True, f.random_legal_move, Nothing or anything)
    
    # Having a depth of 5 goes kinda hard but it takes mad long
    play_game("White", f.abminimax, h.grants_heuristic, 5)


