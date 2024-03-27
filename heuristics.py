import chess
import random 

# Ok at taking pieces, bad at seeing threats
# Fairly shit, beats random_legal_move consisantly tho so that's cool
def grants_heuristic(board: chess.Board, side):
    """
    Scoring:
    p = 1, kn = 3, b = 3, r = 5, q = 9, k = 0 (infinite)

    Add up all peices for white minus black peices and add to score DONE
    Check if being attacked if so is_attacked_by(chess.Color, chess.Square), then find attackers using attackers DONE

    If difference is zero but there is an attacker, check for a defender

    Check if defended, using is_attacked_by(), then evaulate defenders using attackers(chess.Color, chess.Square)
    Then Evaluate the value of the peice, its defenders adn attackers to come up with some value using and subtract from score

    Else if its not being attacked, check if its attacking a higer value peice

    Other helpdul methods:
    piece_at(square) / piece_type_at()
    color_at()
    Or look in core / Board or pieces for more

    Add + 1000 somethings if state is checkmate in your favor or - 1000 if checkmate in oppoenents favor
    """
    if board.is_game_over():
        # if board.is_checkmate():
            if board.outcome().winner == side:
                return 1000
            # Stalemate included (None)
            else:
                return -1000
    # Larger total is better
    total = 0
    values = [1, 3, 3, 5, 9, 0]
    for i in range(1,6):
        # Gets all the square for all the peices types of a given color
        squares = board.pieces(chess.PieceType(i), chess.Color(side))
        if i == 1:
            total += len(squares) # Count pawns
        elif i == 2 or i == 3:
            total += len(squares) * 3 # Count bishops / knights
        elif i == 4:
            total += len(squares) * 5 # Count Rooks
        elif i == 5:
            total += len(squares) * 9 # Count queens
        # Don't need to count king
            
        # Check if any opposing peices attack a square, if so
            # Subtract the largerst differences of the values of the peices
            # from the total

        for square in squares:
            attackers_squares = board.attackers(not side, square)
            if (len(attackers_squares) > 0):
                largest_difference = 0
                for attacter_square in attackers_squares:
                    attacker = board.piece_type_at(attacter_square)
                    attacker_value = values[attacker - 1]
                    difference = values[i - 1] - attacker_value
                    if (difference > largest_difference):
                        largest_difference = difference
                total -= largest_difference
                # If there is at least one attacker but difference is 0, check for defenders, if less defenders than attackers, subtract values
                # Also should check values of defenders
                if (largest_difference == 0):
                    # Thankfully pieces don't attack their own squares
                    defender_squares = board.attackers(side, square)
                    if (len(defender_squares) < len(attackers_squares)):
                        if (len(defender_squares) == 0): # Piece is hanging
                            total -= values[board.piece_type_at(square) - 1]
                        else:
                            tot_attacker_val = 0
                            tot_defender_val = 0
                            # Get total values of each defender and attackers, subtract difference from total
                            for attacker in attackers_squares:
                                tot_attacker_val += values[board.piece_type_at(attacker) - 1]
                            for defender in defender_squares:
                                tot_defender_val += values[board.piece_type_at(defender) - 1]
                            compare = tot_defender_val - tot_attacker_val
                            if compare > 0:
                                total -= compare
                # Check what you're currently attacking 
    return total