import chess
from random import choice
from EvaluationFunctions.Node import Node

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
        """Comprehensive position evaluation combining material, position, king safety, pawns and mobility."""
        if board.is_game_over():
            if board.is_checkmate():
                return -10000 if board.turn else 10000
            return 0  # Draw
            
        score = 0
        
        # 1. Material and Piece-Square Tables Evaluation
        piece_to_table = {
            chess.KNIGHT: knight_scores,
            chess.BISHOP: bishop_scores,
            chess.ROOK: rook_scores,
            chess.QUEEN: queen_scores,
            chess.PAWN: pawn_scores,
        }
        
        # Cache commonly used values
        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)
        
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
                
            # Base material and position scoring
            piece_value = piece_score.get(piece.symbol().upper(), 0)
            
            # Get square coordinates
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            
            # Position score from PST
            position_score = 0
            if piece.piece_type in piece_to_table:
                if piece.color == chess.BLACK:
                    position_score = piece_to_table[piece.piece_type][7 - rank][file]
                else:
                    position_score = piece_to_table[piece.piece_type][rank][file]
            
            # Combine material and position
            total_piece_score = piece_value + position_score
            
            # 2. King Safety Evaluation
            if piece.piece_type == chess.KING:
                king_safety = 0
                if piece.color == chess.WHITE:
                    # Penalize exposed king
                    if len(white_pawns) < 3:  # Endgame
                        king_safety = 0.3  # Encourage king activity in endgame
                    else:  # Middlegame
                        # Penalize exposed king file
                        if not any(sq & 7 == file for sq in white_pawns):
                            king_safety -= 0.5
                        # Penalize king in center
                        if 2 <= file <= 5 and rank > 0:
                            king_safety -= 0.3
                else:
                    if len(black_pawns) < 3:
                        king_safety = 0.3
                    else:
                        if not any(sq & 7 == file for sq in black_pawns):
                            king_safety -= 0.5
                        if 2 <= file <= 5 and rank < 7:
                            king_safety -= 0.3
                total_piece_score += king_safety
            
            # 3. Pawn Structure Evaluation
            if piece.piece_type == chess.PAWN:
                pawn_score = 0
                
                # Doubled pawns penalty
                if piece.color == chess.WHITE:
                    for sq in white_pawns:
                        if chess.square_file(sq) == file and chess.square_rank(sq) != rank:
                            pawn_score -= 0.5
                    # Isolated pawns penalty
                    if not any(chess.square_file(sq) == file - 1 for sq in white_pawns) and \
                      not any(chess.square_file(sq) == file + 1 for sq in white_pawns):
                        pawn_score -= 0.3
                else:
                    for sq in black_pawns:
                        if chess.square_file(sq) == file and chess.square_rank(sq) != rank:
                            pawn_score -= 0.5
                    if not any(chess.square_file(sq) == file - 1 for sq in black_pawns) and \
                      not any(chess.square_file(sq) == file + 1 for sq in black_pawns):
                        pawn_score -= 0.3
                        
                # Passed pawn bonus
                if piece.color == chess.WHITE:
                    if not any(chess.square_file(sq) == file and chess.square_rank(sq) > rank 
                              for sq in black_pawns):
                        pawn_score += 0.6 + rank * 0.1  # More bonus as pawn advances
                else:
                    if not any(chess.square_file(sq) == file and chess.square_rank(sq) < rank 
                              for sq in white_pawns):
                        pawn_score += 0.6 + (7 - rank) * 0.1
                        
                total_piece_score += pawn_score
            
            # 4. Mobility Contribution
            mobility_score = 0
            if piece.color == board.turn:  # Only calculate mobility for the side to move
                legal_moves = len([move for move in board.legal_moves 
                                if move.from_square == square])
                mobility_score = 0.1 * legal_moves  # Small bonus for each available move
                
            total_piece_score += mobility_score
            
            # Add to total score (positive for white, negative for black)
            if piece.color == chess.WHITE:
                score += total_piece_score
            else:
                score -= total_piece_score
        
        return score