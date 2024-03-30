import pygame
import chess
from stockfish import Stockfish
from random import choice

from data.classes.Board import Board

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board1 = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])
board2 = chess.Board()

stockfish = Stockfish(
    "stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
)
stockfish.set_depth(20)
stockfish.set_skill_level(20)

my_col=choice(["white", "black"])

def draw(display):
    display.fill("white")
    board1.draw(display)
    pygame.display.update()


if __name__ == "__main__":
    running = True
    while running:
        if board1.turn == my_col:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # Quit the game if the user presses the close button
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the mouse is clicked
                    if event.button == 1:
                        move = board1.handle_click(mx, my)
                        if move != None:
                            board2.push_san(move)

        else:
            stockfish.set_fen_position(board2.fen())
            rec_move = stockfish.get_top_moves(1)[0]["Move"]
            board2.push_san(rec_move)
            init = rec_move[:2]
            final = rec_move[2:]
            ix, iy = ord(init[0]) - 97, 8 - int(init[1])
            fx, fy = ord(final[0]) - 97, 8 - int(final[1])
            w=board1.tile_width
            h=board1.tile_height
            imx, imy, fmx, fmy=ix*w+w/2, iy*h+h/2, fx*w+w/2, fy*h+h/2
            board1.handle_click(imx, imy)
            board1.handle_click(fmx,fmy)
        if board1.is_in_checkmate("black"):  # If black is in checkmate
            print("White wins!")
            running = False
        elif board1.is_in_checkmate("white"):  # If white is in checkmate
            print("Black wins!")
            running = False
        # Draw the board
        draw(screen)
