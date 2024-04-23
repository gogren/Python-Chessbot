import random
import time
from typing import List
import pygame
import chess
import heuristics as h
import searches as f
import gui as g
import chess.polyglot

pygame.init()
"""
color: "Black" or "White"
f: search function opponent will use
h: heuristic function
bin: Opening lookup table youre bot will use, input "" if you don't want to use one.
autobattle (Auto to false): True / False
f2: Only if autobattle is True, seach function you're autobattler will use
h2: ^^, heuristic your autobattler will use
"""
def play_game(color, f, h, depth_limit, bin,  autobattle = False, f2 = None, h2 = None):
    board = chess.Board()
    g.show(board.board_fen(), board)
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
                end = input('Enter "end" to be done: ')
                if end == "end":
                    break
                print()
            break
        if board.turn == side: # Your turn
            pickedBookMove = False
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
                    move = g.check_for_promotion(board, move)
                    g.show(board.board_fen(), board)
                    print(move)
                    # Check if move is valid
                    if move in l_moves:
                        break
                    else:
                        print("Illegal move, try again.")
            else: # Autobattle with chosen heuristic until game over
                print(f"Generating {you}'s next move...")
                binMoves = []
                with chess.polyglot.open_reader(f"polyglot-collection/{bin}") as reader:
                    for entry in reader.find_all(board):
                        binMoves.append(entry)
                        # print(entry.move, entry.weight, entry.learn)
                if len(binMoves) > 0:
                    print("Chose move from opening database")
                    time.sleep(1)
                    # Pick a random move from list of book moves MAYBE PICK WEIGHTED MOVE
                    rand_move = pick_weighted_move(binMoves)
                    print(f"Chose {rand_move} from book moves")
                    board.push(rand_move) 
                    pickedBookMove = True 
                else:  
                    move_pair = f2(board, h2, depth_limit, board.turn)
                    move = move_pair[0]
                    print('Your side chose', move.uci())
                    print("Your Position Score:", move_pair[1])
            if (not pickedBookMove):
                uci_move = chess.Move.from_uci(str(move))
                board.push(uci_move)
            print(board)
            num_of_moves += 1
            print("Number of Moves:")
            g.show(board.board_fen(), board)
        else: # Bot's turn
            binMoves = []
            print(f"Generating {opponent}'s next move...")
            with chess.polyglot.open_reader(f"polyglot-collection/{bin}") as reader:
                for entry in reader.find_all(board):
                    binMoves.append(entry)
                    # print(entry.move, entry.weight, entry.learn)
            if len(binMoves) > 0:
                print("Chose move from opening database")
                time.sleep(1)
                # Pick a random move from list of book moves MAYBE PICK WEIGHTED MOVE
                rand_move = pick_weighted_move(binMoves)
                print(f"Chose {rand_move} from book moves")
                board.push(rand_move)
            else:
                agents_move_pair = f(board, h, depth_limit, board.turn)
                agents_move = agents_move_pair[0]
                print(f"Opponent chose: {agents_move.uci()}")
                print("Opponent's Position Score:", agents_move_pair[1])
                board.push(agents_move)
            g.show(board.board_fen(), board)
            print(board)

####################################
########## Misc Functions ##########
####################################


def print_legal_moves(board):
    moves = []
    for move in board.legal_moves:
        moves.append(move.uci())
    print(moves)

# Pick a move semi randomly
def pick_weighted_move(entryList: List[chess.polyglot.Entry]):
    print(entryList)
    total = sum(entry.weight for entry in entryList)
    cumulative_probabilities = [entry.weight / total for entry in entryList]
    
    random_value = random.random()
    cumulative_probability_sum = 0
    for i, entry in enumerate(entryList):
        cumulative_probability_sum += cumulative_probabilities[i]
        if random_value <= cumulative_probability_sum:
            return entry.move









if __name__ == "__main__":
    # Example: 
    # The following function, the user's color is chosen as black, the agent opponent will use f.minimax and h.grants_heuristic
    # for generating its move using a depth of 3 in its searches, autobattle is set to true, so no user input for user's color
    # Optionally, f.random_legal_move is used here for the user's side's search, also a heuristic can also be added for user searching. 

    # play_game("Black", f.minimax, h.grants_heuristic, 3, True, f.random_legal_move, Nothing or anything)
    # Having a depth of 5 goes kinda hard but it takes mad long
    play_game("Black", f.abminimax, h.piece_sqaure_double_eval, 4, "codekiddy.bin")

# Stuff about the opening bins:
# Human.bin - agressive/fun - Nah this one is dumb asf it be puhing it's king and shit
# Titans.bin - Flavio Martin's games - Not too bad
# Book.bin - seem's pretty good idrk
# codekiddy.bin - largest one I think, seems good. 
# There's too many idk

