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
        return self._evaluate_mobility(board)

    def _evaluate_mobility(self, board):
        """Evaluates piece mobility considering legal moves, piece control, and potential threats."""
        score = 0

        # Piece mobility weights (how valuable each piece's mobility is)
        mobility_weights = {
            chess.PAWN: 0.1,  # Pawn mobility less important
            chess.KNIGHT: 0.3,  # Knights need good squares
            chess.BISHOP: 0.3,  # Bishops need open diagonals
            chess.ROOK: 0.35,  # Rooks need open files
            chess.QUEEN: 0.4,  # Queen mobility critical
        }

        # Helper function to count piece's legal moves
        def count_piece_moves(square, piece, color):
            moves = 0
            attack_value = 0
            center_control = 0

            # Create a copy of the board to generate legal moves
            temp_board = board.copy()

            # Get all legal moves for this piece
            for move in temp_board.legal_moves:
                if move.from_square == square:
                    moves += 1

                    # Extra points for controlling central squares
                    to_file = chess.square_file(move.to_square)
                    to_rank = chess.square_rank(move.to_square)
                    if 2 <= to_file <= 5 and 2 <= to_rank <= 5:
                        center_control += 0.1

                    # Points for attacking enemy pieces
                    target_piece = board.piece_at(move.to_square)
                    if target_piece and target_piece.color != color:
                        # Value of attacked piece relative to attacking piece
                        attacker_value = mobility_weights.get(piece.piece_type, 0)
                        target_value = mobility_weights.get(target_piece.piece_type, 0)
                        attack_value += max(0, target_value - attacker_value)

            return moves, attack_value, center_control

        # Helper function to evaluate piece development
        def evaluate_development(square, piece, color):
            development_score = 0

            # Check if piece has moved from starting position
            starting_rank = 1 if color == chess.WHITE else 6
            if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                if chess.square_rank(square) != starting_rank:
                    development_score += 0.2

            return development_score

        # Helper function to evaluate control of open files and diagonals
        def evaluate_line_control(square, piece, color):
            control_score = 0

            if piece.piece_type in [chess.ROOK, chess.QUEEN]:
                # Check for control of open files
                file = chess.square_file(square)
                file_is_open = True
                for rank in range(8):
                    check_square = chess.square(file, rank)
                    if check_square != square:
                        check_piece = board.piece_at(check_square)
                        if check_piece and check_piece.piece_type == chess.PAWN:
                            file_is_open = False
                            break
                if file_is_open:
                    control_score += 0.3

            if piece.piece_type in [chess.BISHOP, chess.QUEEN]:
                # Count squares controlled on main diagonals
                diagonal_squares = 0
                for offset in range(-7, 8):
                    file = chess.square_file(square) + offset
                    rank = chess.square_rank(square) + offset
                    if 0 <= file <= 7 and 0 <= rank <= 7:
                        diagonal_squares += 1
                control_score += 0.02 * diagonal_squares

            return control_score

        # Evaluate mobility for both colors
        for color in [chess.WHITE, chess.BLACK]:
            color_score = 0

            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece and piece.color == color:
                    # Skip king - mobility less relevant
                    if piece.piece_type == chess.KING:
                        continue

                    # Get base mobility score
                    moves, attack_value, center_control = count_piece_moves(
                        square, piece, color
                    )

                    # Weight the moves by piece importance
                    weight = mobility_weights.get(piece.piece_type, 0)
                    mobility_score = moves * weight

                    # Add various components
                    development_score = evaluate_development(square, piece, color)
                    line_control = evaluate_line_control(square, piece, color)

                    # Combine all factors
                    piece_score = (
                        mobility_score
                        + attack_value
                        + center_control
                        + development_score
                        + line_control
                    )

                    color_score += piece_score

            # Add to total score (positive for white, negative for black)
            score += color_score if color == chess.WHITE else -color_score

        # Scale the final score to be comparable with other evaluation components
        return score * 0.1
