import random
import chess
import chess.engine
board = chess.Board()

my_total = 39
opposing_total = 39
endgame = False
BASIC_VALUES = [1,3,3,5,9,0]
side = True
for i in range(1, 6):
        squares = board.pieces(chess.PieceType(i), chess.Color(side))
        print("SQUARES",squares)
        # for square in squares:
        #         print("SQUARE", square)
        cur_piece_value = len(squares) * BASIC_VALUES[i-1]
        my_total -= cur_piece_value
        opponent_squares = board.pieces(chess.PieceType(i), chess.Color(not side))
        opposing_total -= len(opponent_squares) * BASIC_VALUES[i-1]
print("White's total", my_total)
print("Black's total", opposing_total)

"""
        A dynamic list of legal moves.

        >>> import chess
        >>>
        >>> board = chess.Board()
        >>> board.legal_moves.count()
        20
        >>> bool(board.legal_moves)
        True
        >>> move = chess.Move.from_uci("g1f3")
        >>> move in board.legal_moves
        True

        Wraps :func:`~chess.Board.generate_legal_moves()` and
        :func:`~chess.Board.is_legal()`.
"""