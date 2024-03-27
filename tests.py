import random
import chess
import chess.engine
board = chess.Board()
board.legal_moves.count()
print(board)
for move in board.legal_moves:
    print(move)
# 1 = p, 2 = kn, 3 = b, 4 = r, 5 = q, 6 = k
# True = White, False = Black
squares = board.pieces(chess.PieceType(1), chess.Color(False))
print(len(squares))
for square in squares:
    # 0 - 63
    print(square)

print(board.attackers(True, 3))

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