import chess
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
        return self._evaluate_position(board)

    def _evaluate_position(self, board):
        """Basic position evaluation based on material count."""
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            value = piece_values.get(piece.piece_type, 0)
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        return score
