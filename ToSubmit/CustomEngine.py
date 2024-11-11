import pygame
import chess
from random import choice
from data.classes.Board import Board
from EvaluationFunctions.Negmax.PST import ImprovedChessEngine as Engine

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board1 = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])
board2 = chess.Board()

mcts_engine = Engine()

my_col = choice(["white", "black"])


def draw(display):
    display.fill("white")
    board1.draw(display)
    pygame.display.update()


def is_promotion_move(board, move_uci):
    from_square = chess.parse_square(move_uci[:2])
    to_square = chess.parse_square(move_uci[2:4])
    piece = board.piece_at(from_square)

    if piece is None or piece.piece_type != chess.PAWN:
        return False

    to_rank = chess.square_rank(to_square)
    return (to_rank == 7 and board.turn == chess.WHITE) or (
        to_rank == 0 and board.turn == chess.BLACK
    )


if __name__ == "__main__":
    running = True
    while running:
        if board2.turn == (
            my_col == "white"
        ):  # Adjusted to ensure `board2.turn` matches `my_col`
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        move = board1.handle_click(mx, my)
                        if move is not None:
                            # Ensure move is valid in `board2`
                            if len(move) == 4:
                                if is_promotion_move(board2, move):
                                    move += (
                                        "q"  # Append 'q' for queen promotion if needed
                                    )
                                try:
                                    board2.push_uci(move)  # Push to board2
                                    board1.handle_click(
                                        mx, my
                                    )  # Update board1 to match
                                except ValueError:
                                    print("Invalid move")
        else:
            # Get move from MCTS engine
            engine_move = mcts_engine.get_move(board2)
            board2.push(engine_move)

            # Convert UCI move to board1 click coordinates
            init = engine_move.uci()[:2]
            final = engine_move.uci()[2:4]
            ix, iy = ord(init[0]) - 97, 8 - int(init[1])
            fx, fy = ord(final[0]) - 97, 8 - int(final[1])
            w = board1.tile_width
            h = board1.tile_height
            imx, imy = ix * w + w / 2, iy * h + h / 2
            fmx, fmy = fx * w + w / 2, fy * h + h / 2
            board1.handle_click(imx, imy)
            board1.handle_click(fmx, fmy)

        # Use `board2` for checking game-over conditions
        if board2.is_checkmate():
            print(
                f"{'White' if board2.turn == chess.BLACK else 'Black'} wins by checkmate!"
            )
            running = False
        elif board2.is_stalemate() or board2.is_insufficient_material():
            print("Game ends in a draw.")
            running = False

        draw(screen)
