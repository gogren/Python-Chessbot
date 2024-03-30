import pygame
import chess
import random

screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("Chess Engine")
screen.fill("WHITE")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

chessboard = pygame.image.load('graph/chessboard.png').convert_alpha()
King = pygame.image.load('graph/WKing.png').convert_alpha()
king = pygame.image.load('graph/BKing.png').convert_alpha()
Knight = pygame.image.load('graph/WKnight.png').convert_alpha()
knight = pygame.image.load('graph/BKnight.png').convert_alpha()
Rook = pygame.image.load('graph/WRook.png').convert_alpha()
rook = pygame.image.load('graph/BRook.png').convert_alpha()
Queen = pygame.image.load('graph/WQueen.png').convert_alpha()
queen = pygame.image.load('graph/BQueen.png').convert_alpha()
Bishop = pygame.image.load('graph/WBishop.png').convert_alpha()
bishop = pygame.image.load('graph/BBishop.png').convert_alpha()
Pawn = pygame.image.load('graph/WPawn.png').convert_alpha()
pawn = pygame.image.load('graph/BPawn.png').convert_alpha()


def draw(fen, col, rank, board) :
    if fen == 'K' :
        if board.turn == chess.WHITE :
            if board.is_check() :
                pygame.draw.circle(screen, RED, (rank + 30, col + 30), 30)
        screen.blit(King, (rank, col))
    elif fen == 'k' :
        if board.turn == chess.BLACK :
            if board.is_check() :
                pygame.draw.circle(screen, RED, (rank + 30, col + 30), 30)
        screen.blit(king, (rank, col))
    elif fen == 'Q' :
        screen.blit(Queen, (rank, col))
    elif fen == 'q' :
        screen.blit(queen, (rank, col))
    elif fen == 'R' :
        screen.blit(Rook, (rank, col))
    elif fen == 'r' :
        screen.blit(rook, (rank, col))
    elif fen == 'N' :
        screen.blit(Knight, (rank, col))
    elif fen == 'n' :
        screen.blit(knight, (rank, col))
    elif fen == 'B' :
        screen.blit(Bishop, (rank, col))
    elif fen == 'b' :
        screen.blit(bishop, (rank, col))
    elif fen == 'P' :
        screen.blit(Pawn, (rank, col))
    elif fen == 'p' :
        screen.blit(pawn, (rank, col))

def show(FEN, board) :
        screen.blit(chessboard, (0, 0))
        col = 0
        rank = 0
        for fen in FEN :
            if fen == '/' :
                col = col + 1
                rank = 0
            elif fen in ('1', '2', '3', '4', '5', '6', '7', '8') :
                rank = rank + int(fen)
            elif fen in ('K', 'k', 'Q', 'q', 'R', 'r', 'N', 'n', 'B', 'b', 'P', 'p') :
                draw(fen, col*60, rank*60, board)
                rank = rank + 1
        pygame.display.update() 


# OUR OWN ADDED FUNCTIONS
        
YELLOW = (255, 255, 0)

def get_square(pos):
    square = ""
    x = pos[0]
    y = pos[1]
    if x <= 60:
        square += 'a'
    elif 60 < x <= 120:
        square += 'b'
    elif 120 < x <= 180:
        square += 'c'
    elif 180 < x <= 240:
        square += 'd'
    elif 240 < x <= 300:
        square += 'e'
    elif 300 < x <= 360:
        square += 'f'
    elif 360 < x <= 420:
        square += 'g'
    elif 420 < x <= 480:
        square += 'h'
    else:
        print('Click out of bounds')

    if y <= 60:
        square += '8'
    elif 60 < y <= 120:
        square += '7'
    elif 120 < y <= 180:
        square += '6'
    elif 180 < y <= 240:
        square += '5'
    elif 240 < y <= 300:
        square += '4'
    elif 300 < y <= 360:
        square += '3'
    elif 360 < y <= 420:
        square += '2'
    elif 420 < y <= 480:
        square += '1'
    else:
        print('Click out of bounds')
    
    return square

# Autopromote to a queen if piece is moving from 7 to 8 and is a pawn
def check_for_promotion(board: chess.Board, move):
    square = chess.parse_square(move[:2])
    if move[1] == "7" and move[3] == "8" and board.piece_type_at(square) == 1:
        return move + "q"
    return move

# Return coordinate value of sqaure
def parse_square(square: str):
    letter = square[0]
    num = square[1]
    y = 420 - (int(num) * 60 - 60)
    if letter == 'a':
        x = 0
    elif letter == 'b':
        x = 60
    elif letter == 'c':
        x = 120
    elif letter == 'd':
        x = 180
    elif letter == 'e':
        x = 240
    elif letter == 'f':
        x = 300
    elif letter == 'g':
        x = 360
    elif letter == 'h':
        x = 420
    else:
        print("Square parse error")
        return None
    print("Got", x, y)
    return x, y

 # Highlights the selected square and highlights the moves that square can make
def show_selected_moves(board: chess.Board, first_click):  
    objs = []
    draw_at = parse_square(first_click)
    objs.append(pygame.draw.rect(screen, YELLOW, pygame.Rect(draw_at[0], draw_at[1], 60, 60), 2))
    for move in board.legal_moves:
        to_uci = move.uci()
        if to_uci[:2] == first_click:
            draw_at = parse_square(to_uci[2:])
            objs.append(pygame.draw.rect(screen, YELLOW, pygame.Rect(draw_at[0], draw_at[1], 60, 60), 2))
    pygame.display.update() 
    return objs