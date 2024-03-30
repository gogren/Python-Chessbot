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
                return 1000
            # Stalemate included (None)
            else:
                return -1000
    # Larger total is better
    total = 0
    opposing_total = 0
    total_piece_value = 0
    values = [1, 3, 3, 5, 9, 0]
    for i in range(1,6):
        # Gets all the square for all the peices types of a given color
        squares = board.pieces(chess.PieceType(i), chess.Color(side))
        opponent_squares = board.pieces(chess.PieceType(i), chess.Color(not side))
        if i == 1: # Could condense this using values[]
            total += len(squares) # Count pawns
            opposing_total += len(opponent_squares)
            total_piece_value += len(squares)
        elif i == 2 or i == 3:
            total += len(squares) * 3 # Count bishops / knights
            total_piece_value += len(squares) * 3
            opposing_total += len(opponent_squares) * 3
        elif i == 4:
            total += len(squares) * 5 # Count Rooks
            total_piece_value += len(squares) * 5
            opposing_total += len(opponent_squares) * 5
        elif i == 5:
            total += len(squares) * 9 # Count queens
            total_piece_value += len(squares) * 9
            opposing_total += len(opponent_squares) * 9
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
    # Reward agent for having more peices than opponent
    piece_comparison = total_piece_value - opposing_total
    if (piece_comparison >= 1):
        total += piece_comparison - 1
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