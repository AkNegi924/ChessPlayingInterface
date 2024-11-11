import chess
import math
import time
from random import choice
from EvaluationFunctions.Node import Node

"""Piece Square Tables (PSTs)"""


piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
    [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
    [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
    [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
    [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
    [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
    [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
    [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
]

bishop_scores = [
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
    [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
    [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
    [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
    [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
    [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
]

rook_scores = [
    [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25],
]

queen_scores = [
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
    [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
]

pawn_scores = [
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
    [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
    [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
    [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
    [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
    [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
    [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
    [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
]


class MCTSEngine:
    def __init__(self, search_depth=10):
        self.search_depth = search_depth
        self.iterations = 1000

    def get_move(self, board):
        root = Node(board)

        for _ in range(self.iterations):
            # Selection
            node = root
            while node.untried_moves == [] and node.children != []:
                node = max(node.children, key=lambda n: n.ucb1())

            # Expansion
            if node.untried_moves != []:
                node = node.expand()

            # Simulation + Evaluation
            result = self._simulate_and_evaluate(node.board)

            # Backpropagation with evaluation score
            while node is not None:
                node.visits += 1
                node.wins += result
                node = node.parent
                result = 1 - result  # Flip result for opponent's perspective

        # Choose best move based on win rate rather than just visits
        best_child = max(
            root.children, key=lambda n: n.wins / n.visits if n.visits > 0 else 0
        )
        return best_child.move

    def _simulate_and_evaluate(self, board):
        """Simulate game to fixed depth and evaluate final position."""
        board = board.copy()
        moves_played = 0

        # Play random moves until depth is reached or game is over
        while not board.is_game_over() and moves_played < self.search_depth:
            legal_moves = list(board.legal_moves)
            if not legal_moves:
                break
            move = choice(legal_moves)
            board.push(move)
            moves_played += 1

        # If game is over, return actual result
        if board.is_game_over():
            result = board.result()
            if result == "1-0":
                return 1.0
            elif result == "0-1":
                return 0.0
            return 0.5

        # Otherwise evaluate the position and normalize to [0,1]
        score = self.evaluate(board)
        # Convert score to probability using sigmoid-like function
        evaluation = 1 / (1 + 10 ** (-score / 10))

        # If it's black's turn, invert the score
        if not board.turn:
            evaluation = 1 - evaluation

        return evaluation

    def evaluate(self, board):
        """Public method to expose position evaluation."""
        return self._evaluate_position(board)

    def _evaluate_position(self, board):
        """Enhanced position evaluation using piece-square tables and material count."""
        score = 0
        piece_to_table = {
            chess.KNIGHT: knight_scores,
            chess.BISHOP: bishop_scores,
            chess.ROOK: rook_scores,
            chess.QUEEN: queen_scores,
            chess.PAWN: pawn_scores,
        }

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue

            # Get base piece value
            piece_value = piece_score.get(piece.symbol().upper(), 0)

            # Get square coordinates (0-7 for both rank and file)
            rank = chess.square_rank(square)
            file = chess.square_file(square)

            # For black pieces, we need to flip the rank index
            position_score = 0
            if piece.piece_type in piece_to_table:
                if piece.color == chess.BLACK:
                    position_score = piece_to_table[piece.piece_type][7 - rank][file]
                else:
                    position_score = piece_to_table[piece.piece_type][rank][file]

            # Combine material value with position bonus
            total_piece_score = piece_value + position_score

            # Add to total score (positive for white, negative for black)
            if piece.color == chess.WHITE:
                score += total_piece_score
            else:
                score -= total_piece_score

        return score
