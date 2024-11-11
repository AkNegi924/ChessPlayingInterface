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
        return self._evaluate_pawn_structure(board)

    def _evaluate_pawn_structure(self, board):
        """Evaluates pawn structure including isolated, doubled, backward pawns, and chains."""
        score = 0

        # Helper function to get all pawns of a given color
        def get_pawns(color):
            pawns = []
            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN and piece.color == color:
                    pawns.append(square)
            return pawns

        # Helper function to check if a pawn is isolated
        def is_isolated_pawn(square, color):
            file = chess.square_file(square)
            for adjacent_file in [file - 1, file + 1]:
                if adjacent_file < 0 or adjacent_file > 7:
                    continue
                # Check entire adjacent files for friendly pawns
                for rank in range(8):
                    adj_square = chess.square(adjacent_file, rank)
                    piece = board.piece_at(adj_square)
                    if (
                        piece
                        and piece.piece_type == chess.PAWN
                        and piece.color == color
                    ):
                        return False
            return True

        # Helper function to check if a pawn is doubled
        def is_doubled_pawn(square, color, pawns):
            file = chess.square_file(square)
            count = 0
            for pawn_square in pawns:
                if chess.square_file(pawn_square) == file:
                    count += 1
            return count > 1

        # Helper function to check if a pawn is backward
        def is_backward_pawn(square, color):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            # Direction of pawn movement
            direction = 1 if color == chess.WHITE else -1

            # Check if pawn can be supported by adjacent pawns
            can_be_supported = False
            for adj_file in [file - 1, file + 1]:
                if adj_file < 0 or adj_file > 7:
                    continue

                # Check supporting pawns
                support_rank = rank - direction
                while 0 <= support_rank <= 7:
                    support_square = chess.square(adj_file, support_rank)
                    piece = board.piece_at(support_square)
                    if (
                        piece
                        and piece.piece_type == chess.PAWN
                        and piece.color == color
                    ):
                        can_be_supported = True
                        break
                    support_rank -= direction

            # Check if pawn is blocked from advancing by enemy pawns
            is_blocked = False
            check_rank = rank + direction
            while 0 <= check_rank <= 7:
                block_square = chess.square(file, check_rank)
                piece = board.piece_at(block_square)
                if piece and piece.piece_type == chess.PAWN and piece.color != color:
                    is_blocked = True
                    break
                check_rank += direction

            return is_blocked and not can_be_supported

        # Helper function to evaluate pawn chains
        def evaluate_pawn_chain(square, color, pawns):
            chain_score = 0
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            # Check diagonal connections (pawn protection)
            for adj_file in [file - 1, file + 1]:
                if adj_file < 0 or adj_file > 7:
                    continue

                protecting_rank = rank - (1 if color == chess.WHITE else -1)
                if 0 <= protecting_rank <= 7:
                    protect_square = chess.square(adj_file, protecting_rank)
                    piece = board.piece_at(protect_square)
                    if (
                        piece
                        and piece.piece_type == chess.PAWN
                        and piece.color == color
                    ):
                        chain_score += 0.5  # Bonus for each pawn protection

            return chain_score

        # Helper function to evaluate passed pawns
        def is_passed_pawn(square, color):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            # Check path to promotion
            direction = 1 if color == chess.WHITE else -1
            end_rank = 7 if color == chess.WHITE else 0

            # Check files (current and adjacent)
            for check_file in [file - 1, file, file + 1]:
                if check_file < 0 or check_file > 7:
                    continue

                # Check squares until promotion square
                check_rank = rank + direction
                while check_rank != end_rank + direction:
                    check_square = chess.square(check_file, check_rank)
                    piece = board.piece_at(check_square)
                    if (
                        piece
                        and piece.piece_type == chess.PAWN
                        and piece.color != color
                    ):
                        return False
                    check_rank += direction

            return True

        # Evaluate pawns for both colors
        for color in [chess.WHITE, chess.BLACK]:
            pawns = get_pawns(color)
            color_score = 0

            for pawn_square in pawns:
                # Penalize isolated pawns
                if is_isolated_pawn(pawn_square, color):
                    color_score -= 0.5

                # Penalize doubled pawns
                if is_doubled_pawn(pawn_square, color, pawns):
                    color_score -= 0.5

                # Penalize backward pawns
                if is_backward_pawn(pawn_square, color):
                    color_score -= 0.3

                # Reward pawn chains
                color_score += evaluate_pawn_chain(pawn_square, color, pawns)

                # Reward passed pawns
                if is_passed_pawn(pawn_square, color):
                    rank = chess.square_rank(pawn_square)
                    # More points for pawns closer to promotion
                    bonus = 0.5 + (0.1 * (rank if color == chess.WHITE else 7 - rank))
                    color_score += bonus

            # Add to total score (positive for white, negative for black)
            score += color_score if color == chess.WHITE else -color_score

        return score
