import chess
import random 

# Ok at taking pieces, bad at seeing threats
# Fairly shit, beats random_legal_move consisantly tho so that's cool
# Wait hold on it's not that bad
def grants_heuristic(board: chess.Board, side):
    """
    Scoring:
    p = 1, kn = 3, b = 3, r = 5, q = 9, k = 0 (infinite)

    Add up all peices for white minus black peices and add to score DONE
    Check if being attacked if so is_attacked_by(chess.Color, chess.Square), then find attackers using attackers DONE

    If difference is zero but there is an attacker, check for a defender DONE

    Check if defended, using is_attacked_by(), then evaulate defenders using attackers(chess.Color, chess.Square)
    Then Evaluate the value of the peice, its defenders adn attackers to come up with some value using and subtract from score DONE

    Else if its not being attacked, check if its attacking a higer value peice DONE?

    look in core / Board or pieces for more useful methods

    Add + 1000 somethings if state is checkmate in your favor or - 1000 if checkmate in oppoenents favor DONE

    Compare your material to opponent's material, if difference is greater than one, subtract one, so you don't always take pawns DONE
TODO
    FLAW ex: if a pawn attacks a knight but that knight has a pawns and a queen defending it doesn't care to move it
    
    FLAW: Check if a defender is pinned, there's a function for that, if so don't count it DONE

    REWARD DEVELOPMENT:
    Maybe if move count is between some values, and the peices_comparrison isn't that big, add some decimal value to total to encourage not just promoting pawns. 
    """
    if board.is_game_over():
        # if board.is_checkmate():
            if board.outcome().winner == side:
                return 100000
            # Stalemate included (None)
            else:
                return -100000
    # Larger total is better
    total = 0
    opposing_total = 0
    total_piece_value = 0
    values = [1, 3, 3, 5, 9, 0]
    for i in range(1,6):
        # Gets all the square for all the peices types of a given color
        squares = board.pieces(chess.PieceType(i), chess.Color(side))
        opponent_squares = board.pieces(chess.PieceType(i), chess.Color(not side))
        cur_piece_value = len(squares) * values[i-1]
        total+= cur_piece_value
        total_piece_value += cur_piece_value
        opposing_total += len(opponent_squares) * values[i-1]
        # Don't need to count king

        # Check if any opposing peices attack a square, if so
            # Subtract the largerst differences of the values of the peices
            # from the total

        for square in squares:
            attackers_squares = board.attackers(not side, square)
            # Checks if a piece of lesser value is attacking the piece... COULD HAVE ISSUES HERE
            if (len(attackers_squares) > 0):
                largest_difference = 0
                for attacter_square in attackers_squares:
                    attacker = board.piece_type_at(attacter_square)
                    attacker_value = values[attacker - 1]
                    difference = values[i - 1] - attacker_value
                    if (difference > largest_difference):
                        largest_difference = difference
                if largest_difference > 0:
                    # Add +2 penalty to having a piece being attacked by a piece of lower value
                    # Maybe even make throwing a piece away worse, in one case it threw away a bishop because I could promote to a queen,
                    # which in the few moves it saw is less of a "loss" than me getting a queen even through me getting a queen was inevetible
                    total -= (largest_difference + 2)
                # If there is at least one attacker but difference is 0, check for defenders, if less defenders than attackers, subtract values
                # Also should check values of defenders
                if (largest_difference == 0):
                    # Thankfully pieces don't attack their own squares
                    defender_squares = board.attackers(side, square)
                    if (len(defender_squares) < len(attackers_squares)):
                        if (len(defender_squares) == 0): # Piece is hanging, add aditional penalty
                            total -= values[board.piece_type_at(square) - 1] + 1
                        else:
                            tot_attacker_val = 0
                            tot_defender_val = 0
                            # Get total values of each defender and attackers, subtract difference from total
                            for attacker in attackers_squares:
                                if not board.is_pinned(not side, attacker):
                                    tot_attacker_val += values[board.piece_type_at(attacker) - 1]
                            for defender in defender_squares:
                                # Check if a defender is pinned, if so, don't count it, same above
                                if not board.is_pinned(side, defender):
                                    tot_defender_val += values[board.piece_type_at(defender) - 1]
                            compare = tot_defender_val - tot_attacker_val
                            if compare > 0:
                                total -= compare
    # Reward agent for having more peices than opponent, (-1 to not promote constantly trading pawns)?
    piece_comparison = total_piece_value - opposing_total
    if (piece_comparison >= 1):
        total += piece_comparison
    # If boards more than 5 moves have been made by both sides
        # Add small bonuses for devloping bishops and knights
    #if board.ply() > 10:

    # print(total_piece_value, opposing_total)
                # TODO Check what you're currently attacking and promote attacking higer value pieces 
                # Kind of already does that?
                # While having defenders defending that square to a <= value than the attackers attacking a square
                # Ex, a pawn moves up to attack a bishop, the bishop has no defenders but the pawn has one somewhere.
        
    return total


# Could make some mid heuristics for science

def piece_value_difference_only(board: chess.Board, side):
    if board.is_game_over():
        # if board.is_checkmate():
            if board.outcome().winner == side:
                return 100000
            # Stalemate included (None)
            else:
                return -100000
    values = [1, 3, 3, 5, 9, 0]
    total = 0
    opposing_total = 0
    for i in range(1, 6):
        squares = board.pieces(chess.PieceType(i), chess.Color(side))
        cur_piece_value = len(squares) * values[i-1]
        total+= cur_piece_value
        opponent_squares = board.pieces(chess.PieceType(i), chess.Color(not side))
        opposing_total += len(opponent_squares) * values[i-1]
    difference = total - opposing_total
    return difference


# Should play defensively since it only looks at maintaining own pieces
def piece_value_only(board: chess.Board, side):
    if board.is_game_over():
        # if board.is_checkmate():
            if board.outcome().winner == side:
                return 100000
            # Stalemate included (None)
            else:
                return -100000
    values = [1, 3, 3, 5, 9, 0]
    total = 0
    for i in range (1, 6):
        squares = board.pieces(chess.PieceType(i), chess.Color(side))
        cur_piece_value = len(squares) * values[i-1]
        total+= cur_piece_value
    return total


## Below are piece square tables ##
## (From pesto's eval function) ##
## Could chuck these in another file bc damn

# Use these instead of normla [1, 3, 3, 5, 9, 0]
MG_VALUES = [82, 337, 365, 477, 1025,  0] 
EG_VALUES = [94, 281, 297, 512,  936,  0]
BASIC_VALUES = [1, 3, 3, 5, 9, 0]

## White:
WHITE_MG_PAWN = [
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0 
]
WHITE_EG_PAWN = [
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
]
WHITE_MG_KNIGHT = [
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
]
WHITE_EG_KNIGHT = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
]
WHITE_MG_BISHOP = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
]
WHITE_EG_BISHOP = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
]
WHITE_MG_ROOK = [
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
]
WHITE_EG_ROOK = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
]
WHITE_MG_QUEEN = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
]
WHITE_EG_QUEEN = [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
]
WHITE_MG_KING = [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]
WHITE_EG_KING = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
]

WHITE_MG_TABLES = [
    WHITE_MG_PAWN,
    WHITE_EG_KNIGHT,
    WHITE_MG_BISHOP,
    WHITE_MG_ROOK,
    WHITE_MG_QUEEN,
    WHITE_MG_KING,
]
WHITE_EG_TABLES = [
    WHITE_EG_PAWN,
    WHITE_EG_KNIGHT,
    WHITE_EG_BISHOP,
    WHITE_EG_ROOK,
    WHITE_EG_QUEEN,
    WHITE_EG_KING
]

## Black:
# I don't want to make them look all pretty
BLACK_MG_PAWN = [
    0, 0, 0, 0, 0, 0, 0, 0, 
    -22, 38, 24, -15, -23, -20, -1, -35,
      -12, 33, 3, 3, -10, -4, -4, -26,
        -25, 10, 6, 17, 12, -5, -2, -27,
          -23, 17, 12, 23, 21, 6, 13, -14,
            -20, 25, 56, 65, 31, 26, 7, -6,
              -11, 34, 126, 68, 95, 61, 134, 98,
                0, 0, 0, 0, 0, 0, 0, 0, 
]
BLACK_EG_PAWN = [
0, 0, 0, 0, 0, 0, 0, 0, -7, 2, 0, 13, 10, 8, 8, 13, -8, -1, -5, 0, 1, -6, 7, 4, -1, 3, -8, -7, -7, -3, 9, 13, 17, 17, 4, -2, 5, 13, 24, 32, 84, 82, 53, 56, 67, 85, 100, 94, 187, 165, 132, 147, 134, 158, 173, 178, 0, 0, 0, 0, 0, 0, 0, 0,
]
BLACK_MG_BISHOP = [
-21, -39, -12, -13, -21, -14, -3, -33, 1, 33, 21, 7, 0, 16, 15, 4, 10, 18, 27, 14, 15, 15, 15, 0, 4, 10, 12, 34, 26, 13, 13, -6, -2, 7, 37, 37, 50, 19, 5, -4, -2, 37, 50, 35, 40, 43, 37, -16, -47, 18, 59, 30, -13, -18, 16, -26, -8, 7, -42, -25, -37, -82, 4, -29, 
]
BLACK_EG_BISHOP = [
-17, -5, -16, -9, -5, -23, -9, -23, -27, -15, -9, 4, -1, -7, -18, -14, -15, -7, 3, 13, 10, 8, -3, -12, -9, -3, 10, 7, 19, 13, 3, -6, 2, 3, 10, 14, 9, 12, 9, -3, 4, 0, 6, -2, -1, 0, -8, 2, -14, -4, -13, -3, -12, 7, -4, -8, -24, -17, -9, -7, -8, -11, -21, -14, 
]
BLACK_MG_KNIGHT = [
-23, -19, -28, -17, -33, -58, -21, -105, -19, -14, 18, -1, -3, -12, -53, -29, -16, 25, 17, 19, 10, 12, -9, -23, -8, 21, 19, 28, 13, 16, 4, -13, 22, 18, 69, 37, 53, 19, 17, -9, 44, 73, 129, 84, 65, 37, 60, -47, -17, 7, 62, 23, 36, 72, -41, -73, -107, -15, -97, 61, -49, -34, -89, -167,   
]
BLACK_EG_KNIGHT = [
-64, -50, -18, -22, -15, -23, -51, -29, -44, -23, -20, -2, -5, -10, -20, -42, -22, -20, -3, 10, 15, -1, -3, -23, -18, 4, 17, 16, 25, 16, -6, -18, -18, 8, 11, 22, 22, 22, 3, -17, -41, -19, -9, -1, 9, 10, -20, -24, -52, -24, -25, -9, -2, -25, -8, -25, -99, -63, -27, -31, -28, -13, -38, -58, 
]
BLACK_MG_ROOK = [
-26, -37, 7, 16, 17, 1, -13, -19, -71, -6, 11, -1, -9, -20, -16, -44, -33, -5, 0, 3, -17, -16, -25, -45, -23, 6, -7, 9, -1, -12, -26, -36, -20, -8, 35, 24, 26, 7, -11, -24, 16, 61, 45, 17, 36, 26, 19, -5, 44, 26, 67, 80, 62, 58, 32, 27, 43, 31, 9, 63, 51, 32, 42, 32,
]
BLACK_EG_ROOK = [
-20, 4, -13, -5, -1, 3, 2, -9, -3, -11, -9, -9, 2, 0, -6, -6, -16, -8, -12, -7, -1, -5, 0, -4, -11, -8, -6, -5, 4, 8, 5, 3, 2, -1, 1, 2, 1, 13, 3, 4, -3, -5, -3, 4, 5, 7, 7, 7, 3, 8, 3, -3, 11, 13, 13, 11, 5, 8, 12, 12, 15, 18, 10, 13, 
]
BLACK_MG_QUEEN = [
-50, -31, -25, -15, 10, -9, -18, -1, 1, -3, 15, 8, 2, 11, -8, -35, 5, 14, 2, -5, -2, -11, 2, -14, -3, 3, -4, -2, -10, -9, -26, -9, 1, -2, 17, -1, -16, -16, -27, -27, 57, 47, 56, 29, 8, 7, -17, -13, 54, 28, 57, -16, 1, -5, -39, -24, 45, 43, 44, 59, 12, 29, 0, -28, 
]
BLACK_EG_QUEEN = [
-41, -20, -32, -5, -43, -22, -28, -33, -32, -36, -23, -16, -16, -30, -23, -22, 5, 10, 17, 9, 6, 15, -27, -16, 23, 39, 34, 31, 47, 19, 28, -18, 36, 57, 40, 57, 45, 24, 22, 3, 9, 19, 35, 47, 49, 9, 6, -20, 0, 30, 25, 58, 41, 32, 20, -17, 20, 10, 19, 27, 27, 22, 22, -9,
]
BLACK_MG_KING = [
14, 24, -28, 8, -54, 12, 36, -15, 8, 9, -16, -43, -64, -8, 7, 1, -27, -15, -30, -44, -46, -22, -14, -14, -51, -33, -44, -46, -39, -27, -1, -49, -36, -14, -25, -30, -27, -12, -20, -17, -22, 22, 6, -20, -16, 2, 24, -9, -29, -38, -4, -8, -7, -20, -1, 29, 13, 2, -34, -56, -15, 16, 23, -65, 
]
BLACK_EG_KING = [
-43, -24, -14, -28, -11, -21, -34, -53, -17, -5, 4, 14, 13, 4, -11, -27, -9, 7, 16, 23, 21, 11, -3, -19, -11, 9, 23, 27, 24, 21, -4, -18, 3, 26, 33, 26, 27, 24, 22, -8, 13, 44, 45, 20, 15, 23, 17, 10, 11, 23, 38, 17, 17, 14, 17, -12, -17, 4, 15, -11, -18, -18, -35, -74,     
]

BLACK_MG_TABLES = [
    BLACK_MG_PAWN,
    BLACK_EG_KNIGHT,
    BLACK_MG_BISHOP,
    BLACK_MG_ROOK,
    BLACK_MG_QUEEN,
    BLACK_MG_KING,
]
BLACK_EG_TABLES = [
    BLACK_EG_PAWN,
    BLACK_EG_KNIGHT,
    BLACK_EG_BISHOP,
    BLACK_EG_ROOK,
    BLACK_EG_QUEEN,
    BLACK_EG_KING
]
# Instead of subtracting opponent's piece values, could subtract a sub eval of opponents position
# Ie: total -= piece_sqaure_subeval(board, not side) where each eval only goes through the value's of their own side
# Could lead to making moves that worsens your opponents position

def piece_sqaure_eval(board: chess.Board, side) :
    if board.is_game_over():
        # if board.is_checkmate():
            if board.outcome().winner == side:
                return 100000 - board.fullmove_number * 2
            # Stalemate included (None)
            else:
                return -100000 + board.fullmove_number * 2
    
    # Determine if it's endgame or not 
    # (well just say if 18 points of material have been taken by either side)
    my_total = 39
    opposing_total = 39
    endgame = False
    for i in range(1, 6):
        squares = board.pieces(chess.PieceType(i), chess.Color(side))
        cur_piece_value = len(squares) * BASIC_VALUES[i-1]
        my_total -= cur_piece_value
        opponent_squares = board.pieces(chess.PieceType(i), chess.Color(not side))
        opposing_total -= len(opponent_squares) * BASIC_VALUES[i-1]
    if my_total >= 18 or opposing_total >= 18:
        endgame = True
    total = 1000 # Try to keep it from going negative
    total -= board.fullmove_number
    if not endgame: # Still in mid game
        for i in range(1, 7):
            squares = board.pieces(chess.PieceType(i), chess.Color(side))
            for square in squares:
                if side:
                    total += WHITE_MG_TABLES[i-1][(7  -  square // 8) * 8 + (square % 8)]
                else:
                    total += BLACK_MG_TABLES[i-1][(7  -  square // 8) * 8 + (square % 8)]
            cur_piece_value = len(squares) * MG_VALUES[i-1]
            total += cur_piece_value
            opponent_squares = board.pieces(chess.PieceType(i), chess.Color(not side))
            total -= len(opponent_squares) * MG_VALUES[i-1]
    else: # In endgame
        for i in range(1, 7):
            squares = board.pieces(chess.PieceType(i), chess.Color(side))
            for square in squares:
                if side:
                    total += WHITE_EG_TABLES[i-1][(7  -  square // 8) * 8 + (square % 8)]
                else:
                    total += BLACK_EG_TABLES[i-1][(7  -  square // 8) * 8 + (square % 8)]
            cur_piece_value = len(squares) * EG_VALUES[i-1]
            total += cur_piece_value
            opponent_squares = board.pieces(chess.PieceType(i), chess.Color(not side))
            total -= len(opponent_squares) * EG_VALUES[i-1] 
             
    return total

def main():
    return

if __name__ == "__main__":
    main()