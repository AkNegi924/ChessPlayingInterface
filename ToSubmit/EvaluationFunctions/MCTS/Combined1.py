import chess
from random import choice
import math
from typing import Optional, List, Dict, Tuple


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




class Node:
    def __init__(
        self,
        board: chess.Board,
        parent: Optional["Node"] = None,
        move: Optional[chess.Move] = None,
    ):
        self.board = board
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children: List[Node] = []
        self.untried_moves = list(board.legal_moves)
        self.evaluation = 0.5  # Initialize with neutral evaluation

    def expand(self) -> "Node":
        """Expand node by adding a child node for an untried move."""
        if not self.untried_moves:  # Safety check
            return self

        move = choice(self.untried_moves)  # Randomize move selection
        self.untried_moves.remove(move)

        new_board = self.board.copy()
        new_board.push(move)

        child_node = Node(new_board, parent=self, move=move)
        self.children.append(child_node)

        return child_node

    def ucb1(self, exploration: float = math.sqrt(2)) -> float:
        """Calculate UCB1 value for node selection."""
        if self.visits == 0:
            return float("inf")

        exploitation = self.wins / self.visits
        exploration_term = exploration * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

        return exploitation + exploration_term


class MCTSEngine:
    def __init__(self, search_depth=10):
        self.search_depth = search_depth
        self.iterations = 2000  # Increased iterations for better search
        self.transposition_table: Dict[str, Tuple[float, int]] = (
            {}
        )  # Cache for positions
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000,
        }

        # Endgame piece values
        self.endgame_piece_values = {
            chess.PAWN: 150,
            chess.KNIGHT: 280,
            chess.BISHOP: 350,
            chess.ROOK: 525,
            chess.QUEEN: 1000,
            chess.KING: 20000,
        }

    def get_move(self, board: chess.Board) -> chess.Move:
        """Get the best move for the current position."""
        # Handle single legal move case
        legal_moves = list(board.legal_moves)
        if len(legal_moves) == 1:
            return legal_moves[0]
        if not legal_moves:
            return None

        root = Node(board)
        temperature = 1.0

        # Main MCTS loop
        for iteration in range(self.iterations):
            # Gradually reduce exploration
            temperature = max(0.5, temperature * 0.9995)

            # Selection
            node = root
            while node.untried_moves == [] and node.children:
                node = self._select_child(node, temperature)

            # Expansion
            if node.untried_moves:
                node = node.expand()
                if node is None:  # Safety check
                    continue

            # Simulation and backpropagation
            if node:  # Additional safety check
                result = self._simulate_and_evaluate(node.board)
                self._backpropagate(node, result)

        # Select best move
        return self._select_best_move(root)

    def _backpropagate(self, node: Node, result: float) -> None:
        """Backpropagate the result through the tree."""
        while node is not None:
            node.visits += 1
            node.wins += result
            node.evaluation = node.evaluation * 0.95 + result * 0.05
            node = node.parent
            result = 1 - result

    def _select_child(self, node: Node, temperature: float) -> Node:
        """Select child node with temperature-adjusted UCB1."""
        if not node.children:  # Safety check
            return node

        return max(node.children, key=lambda n: self._ucb1(n, temperature))

    def _ucb1(self, node: Node, temperature: float) -> float:
        """Enhanced UCB1 formula with temperature control."""
        if node.visits == 0:
            return float("inf")

        exploitation = node.wins / node.visits
        exploration = math.sqrt(2 * math.log(node.parent.visits) / node.visits)
        position_bonus = node.evaluation * 0.1

        return exploitation + temperature * exploration + position_bonus

    def _select_best_move(self, root: Node) -> chess.Move:
        """Select best move using multiple criteria."""
        if not root.children:  # Safety check
            return choice(list(root.board.legal_moves))

        def move_score(node: Node) -> float:
            if node.visits == 0:
                return float("-inf")

            win_rate = node.wins / node.visits
            visit_weight = math.log(node.visits) / 100
            eval_bonus = node.evaluation * 0.2

            return win_rate + visit_weight + eval_bonus

        best_node = max(root.children, key=move_score)
        return best_node.move

    def _simulate_and_evaluate(self, board: chess.Board) -> float:
        """Simulation with quiescence search and evaluation."""
        if board is None:  # Safety check
            return 0.5

        board = board.copy()

        # Check transposition table
        board_hash = board.fen()
        if board_hash in self.transposition_table:
            cached_eval, cached_depth = self.transposition_table[board_hash]
            if cached_depth >= self.search_depth:
                return self._normalize_score(cached_eval)

        # Quiescence search for tactical positions
        if self._is_tactical_position(board):
            score = self._quiescence_search(board, float("-inf"), float("inf"), 3)
        else:
            score = self._evaluate_complete(board)

        # Cache the evaluation
        self.transposition_table[board_hash] = (score, 0)

        return self._normalize_score(score)

    def _is_tactical_position(self, board: chess.Board) -> bool:
        """Detect if position needs tactical evaluation."""
        # Check for checks, captures, and immediate threats
        return (
            board.is_check()
            or any(board.is_capture(move) for move in board.legal_moves)
            or self._has_immediate_threats(board)
        )

    def _has_immediate_threats(self, board: chess.Board) -> bool:
        """Check for immediate tactical threats."""
        for move in board.legal_moves:
            board.push(move)
            has_threat = board.is_check() or any(
                board.is_capture(m) for m in board.legal_moves
            )
            board.pop()
            if has_threat:
                return True
        return False

    def _quiescence_search(
        self, board: chess.Board, alpha: float, beta: float, depth: int
    ) -> float:
        """Quiescence search for tactical positions."""
        stand_pat = self._evaluate_complete(board)

        if depth == 0:
            return stand_pat

        if stand_pat >= beta:
            return beta

        alpha = max(alpha, stand_pat)

        for move in self._get_capturing_moves(board):
            board.push(move)
            score = -self._quiescence_search(board, -beta, -alpha, depth - 1)
            board.pop()

            if score >= beta:
                return beta
            alpha = max(alpha, score)

        return alpha

    def _get_capturing_moves(self, board: chess.Board) -> List[chess.Move]:
        """Get all capturing moves and checks."""
        return [
            move
            for move in board.legal_moves
            if board.is_capture(move) or board.gives_check(move)
        ]

    def _evaluate_complete(self, board: chess.Board) -> float:
        """Comprehensive position evaluation."""
        if board.is_game_over():
            if board.is_checkmate():
                return -20000 if board.turn else 20000
            return 0

        score = 0

        # Material evaluation with piece-square tables
        material_score = self._evaluate_material(board)
        position_score = self._evaluate_position(board)

        # Pawn structure evaluation
        pawn_score = self._evaluate_pawn_structure(board)

        # King safety evaluation
        king_safety_score = self._evaluate_king_safety(board)

        # Mobility evaluation
        mobility_score = self._evaluate_mobility(board)

        # Center control
        center_control = self._evaluate_center_control(board)

        # Combine all evaluations with weights
        score = (
            material_score * 1.0
            + position_score * 0.7
            + pawn_score * 0.5
            + king_safety_score * 0.8
            + mobility_score * 0.3
            + center_control * 0.4
        )

        return score if board.turn else -score

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


    def _evaluate_material(self, board: chess.Board) -> float:
        """Evaluate material balance with dynamic piece values."""
        score = 0
        # Determine game phase
        is_endgame = self._is_endgame(board)
        piece_values = self.endgame_piece_values if is_endgame else self.piece_values

        for piece_type in piece_values:
            score += (
                len(board.pieces(piece_type, chess.WHITE))
                - len(board.pieces(piece_type, chess.BLACK))
            ) * piece_values[piece_type]
        return score

    def _is_endgame(self, board: chess.Board) -> bool:
        """Determine if position is in endgame."""
        queens = len(
            board.pieces(chess.QUEEN, chess.WHITE)
            | board.pieces(chess.QUEEN, chess.BLACK)
        )
        pieces = len(
            board.pieces(chess.KNIGHT, chess.WHITE)
            | board.pieces(chess.KNIGHT, chess.BLACK)
            | board.pieces(chess.BISHOP, chess.WHITE)
            | board.pieces(chess.BISHOP, chess.BLACK)
            | board.pieces(chess.ROOK, chess.WHITE)
            | board.pieces(chess.ROOK, chess.BLACK)
        )
        return queens == 0 or (queens == 2 and pieces <= 4)

    def _evaluate_pawn_structure(self, board: chess.Board) -> float:
        """Evaluate pawn structure."""
        score = 0

        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        # Evaluate doubled, isolated, and passed pawns
        for color, pawns in [(chess.WHITE, white_pawns), (chess.BLACK, black_pawns)]:
            multiplier = 1 if color == chess.WHITE else -1

            for square in pawns:
                file = chess.square_file(square)
                rank = chess.square_rank(square)

                # Doubled pawns
                if len([s for s in pawns if chess.square_file(s) == file]) > 1:
                    score -= 30 * multiplier

                # Isolated pawns
                if not any(chess.square_file(s) in [file - 1, file + 1] for s in pawns):
                    score -= 20 * multiplier

                # Passed pawns
                opponent_pawns = black_pawns if color == chess.WHITE else white_pawns
                if not any(
                    chess.square_file(s) in [file - 1, file, file + 1]
                    and (
                        (color == chess.WHITE and chess.square_rank(s) > rank)
                        or (color == chess.BLACK and chess.square_rank(s) < rank)
                    )
                    for s in opponent_pawns
                ):
                    bonus = 50 + (rank if color == chess.WHITE else 7 - rank) * 10
                    score += bonus * multiplier

        return score

    def _evaluate_king_safety(self, board: chess.Board) -> float:
        """Evaluate king safety."""
        score = 0

        for color in [chess.WHITE, chess.BLACK]:
            multiplier = 1 if color == chess.WHITE else -1
            king_square = board.king(color)
            if king_square is None:
                continue

            # King pawn shield
            pawn_shield_score = self._evaluate_pawn_shield(board, king_square, color)

            # King attackers
            attackers = len(board.attackers(not color, king_square))

            # Open files near king
            king_file = chess.square_file(king_square)
            open_files = sum(
                1
                for f in range(max(0, king_file - 1), min(8, king_file + 2))
                if not any(
                    board.piece_at(chess.square(f, r)) == chess.PAWN for r in range(8)
                )
            )

            score += (pawn_shield_score - attackers * 20 - open_files * 15) * multiplier

        return score

    def _evaluate_pawn_shield(
        self, board: chess.Board, king_square: chess.Square, color: chess.Color
    ) -> float:
        """Evaluate pawn shield in front of king."""
        score = 0
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)

        # Check pawns in front of king
        pawn_ranks = range(
            king_rank + (1 if color == chess.WHITE else -1),
            king_rank + (3 if color == chess.WHITE else -3),
            1 if color == chess.WHITE else -1,
        )

        for f in range(max(0, king_file - 1), min(8, king_file + 2)):
            for r in pawn_ranks:
                if 0 <= r < 8:
                    if board.piece_at(chess.square(f, r)) == chess.PAWN:
                        score += 10

        return score

    def _evaluate_mobility(self, board: chess.Board) -> float:
        """Evaluate piece mobility."""
        score = 0
        for color in [chess.WHITE, chess.BLACK]:
            multiplier = 1 if color == chess.WHITE else -1
            mobility = 0

            # Save current turn
            original_turn = board.turn
            board.turn = color

            # Count legal moves for each piece
            for move in board.legal_moves:
                piece = board.piece_at(move.from_square)
                if piece is not None:
                    if piece.piece_type == chess.PAWN:
                        mobility += 1
                    elif piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                        mobility += 2
                    elif piece.piece_type == chess.ROOK:
                        mobility += 3
                    elif piece.piece_type == chess.QUEEN:
                        mobility += 4

            # Restore original turn
            board.turn = original_turn

            score += mobility * multiplier

        return score

    def _evaluate_center_control(self, board: chess.Board) -> float:
        """Evaluate control of center squares."""
        center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
        score = 0

        for square in center_squares:
            # Count attackers for both sides
            white_attackers = len(board.attackers(chess.WHITE, square))
            black_attackers = len(board.attackers(chess.BLACK, square))

            # Bonus for piece placement in center
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    score += 20
                else:
                    score -= 20

            # Bonus for control of center squares
            score += (white_attackers - black_attackers) * 10

        return score

    def _normalize_score(self, score: float) -> float:
        """Normalize evaluation score to [0,1] range."""
        return 1 / (1 + math.exp(-score / 400))  # Adjusted sigmoid function
