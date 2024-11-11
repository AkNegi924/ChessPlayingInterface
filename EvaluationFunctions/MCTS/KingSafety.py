import chess
import math
import time
from random import choice
from EvaluationFunctions.Node import Node


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
        return self._evaluate_king_safety(board)

    def _evaluate_king_safety(self, board):
        """Evaluates king safety based on pawn shield, open files, and nearby threats."""
        score = 0

        # Helper function to count pawn shield
        def evaluate_pawn_shield(king_square, color, board):
            shield_score = 0
            rank = chess.square_rank(king_square)
            file = chess.square_file(king_square)

            # Define pawn shield squares relative to king
            shield_squares = []
            if color == chess.WHITE:
                # Check squares in front of king, only if we're not on the last rank
                if rank < 7:  # Added check to prevent going off the board
                    shield_squares = [
                        chess.square(f, rank + 1)
                        for f in range(max(0, file - 1), min(8, file + 2))
                        if 0 <= rank + 1 < 8  # Added rank boundary check
                    ]
            else:
                # Check squares in front of black king, only if we're not on the first rank
                if rank > 0:  # Added check to prevent going off the board
                    shield_squares = [
                        chess.square(f, rank - 1)
                        for f in range(max(0, file - 1), min(8, file + 2))
                        if 0 <= rank - 1 < 8  # Added rank boundary check
                    ]

            # Score each pawn in shield
            for square in shield_squares:
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN and piece.color == color:
                    shield_score += 1.0  # Point for each shield pawn

            return shield_score

        # Helper function to evaluate open files near king
        def evaluate_open_files(king_square, board):
            open_files_penalty = 0
            king_file = chess.square_file(king_square)

            # Check files adjacent to king
            for file in range(max(0, king_file - 1), min(8, king_file + 2)):
                has_pawn = False
                # Check entire file
                for rank in range(8):
                    square = chess.square(file, rank)
                    piece = board.piece_at(square)
                    if piece and piece.piece_type == chess.PAWN:
                        has_pawn = True
                        break
                if not has_pawn:
                    open_files_penalty += 1.0  # Penalty for each open file

            return open_files_penalty

        # Helper function to count attacking pieces near king
        def evaluate_king_attackers(king_square, king_color, board):
            attacker_score = 0
            rank = chess.square_rank(king_square)
            file = chess.square_file(king_square)

            # Check squares around king
            for r in range(max(0, rank - 2), min(8, rank + 3)):
                for f in range(max(0, file - 2), min(8, file + 3)):
                    square = chess.square(f, r)
                    piece = board.piece_at(square)
                    if piece and piece.color != king_color:
                        # Weight attackers by piece value
                        if piece.piece_type == chess.QUEEN:
                            attacker_score += 4.0
                        elif piece.piece_type == chess.ROOK:
                            attacker_score += 2.5
                        elif piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
                            attacker_score += 1.5
                        elif piece.piece_type == chess.PAWN:
                            attacker_score += 0.5

            return attacker_score

        # Evaluate both kings
        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)

        if white_king_square is not None:
            # White king evaluation
            white_shield = evaluate_pawn_shield(white_king_square, chess.WHITE, board)
            white_open_files = evaluate_open_files(white_king_square, board)
            white_attackers = evaluate_king_attackers(
                white_king_square, chess.WHITE, board
            )

            # Combine factors for white
            white_safety = (
                (white_shield * 1.0)
                - (white_open_files * 1.5)
                - (white_attackers * 2.0)
            )
            score += white_safety

        if black_king_square is not None:
            # Black king evaluation
            black_shield = evaluate_pawn_shield(black_king_square, chess.BLACK, board)
            black_open_files = evaluate_open_files(black_king_square, board)
            black_attackers = evaluate_king_attackers(
                black_king_square, chess.BLACK, board
            )

            # Combine factors for black
            black_safety = (
                (black_shield * 1.0)
                - (black_open_files * 1.5)
                - (black_attackers * 2.0)
            )
            score -= black_safety  # Subtract because negative score is bad for black

        # Adjust score based on game phase
        piece_count = len(board.piece_map())
        game_phase_multiplier = min(
            1.0, piece_count / 32.0
        )  # Reduces importance in endgame

        return score * game_phase_multiplier
