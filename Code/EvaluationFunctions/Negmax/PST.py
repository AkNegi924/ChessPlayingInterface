import chess
from random import choice
import math

# Keep the same piece scores and position tables from original code
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


class ImprovedChessEngine:
    def __init__(self, depth=3):
        self.DEPTH = depth
        self.CHECKMATE = 1000
        self.STALEMATE = 0
        self.next_move = None
        
    def get_move(self, board):
        """Main method to get the best move using negamax with alpha-beta pruning"""
        valid_moves = list(board.legal_moves)
        self.find_best_move_negamax(board, valid_moves)
        return self.next_move
        
    def find_best_move_negamax(self, board, valid_moves):
        """Find the best move using negamax algorithm with alpha-beta pruning"""
        self.next_move = None
        # Randomize move order for better alpha-beta pruning
        valid_moves = list(valid_moves)
        choice(valid_moves)
        
        self.find_move_negamax_alpha_beta(
            board, valid_moves, self.DEPTH, 
            -self.CHECKMATE, self.CHECKMATE,
            1 if board.turn else -1
        )
        
        return self.next_move

    def find_move_negamax_alpha_beta(self, board, valid_moves, depth, alpha, beta, turn_multiplier):
        """Negamax implementation with alpha-beta pruning"""
        if depth == 0:
            return turn_multiplier * self.evaluate_position(board)

        max_score = -self.CHECKMATE
        for move in valid_moves:
            board.push(move)
            next_moves = list(board.legal_moves)
            score = -self.find_move_negamax_alpha_beta(
                board, next_moves, depth - 1,
                -beta, -alpha, -turn_multiplier
            )
            board.pop()

            if score > max_score:
                max_score = score
                if depth == self.DEPTH:
                    self.next_move = move

            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break

        return max_score

    def evaluate_position(self, board):
        """Evaluate the board position"""
        if board.is_checkmate():
            if board.turn:  # White to move
                return -self.CHECKMATE
            else:
                return self.CHECKMATE
        elif board.is_stalemate():
            return self.STALEMATE

        score = 0
        
        # Evaluate each piece on the board
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue

            piece_value = piece_score.get(piece.symbol().upper(), 0)
            
            # Get position score based on piece type and color
            position_score = 0
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            
            # Map piece types to their position score tables
            if piece.piece_type == chess.PAWN:
                position_table = pawn_scores
            elif piece.piece_type == chess.KNIGHT:
                position_table = knight_scores
            elif piece.piece_type == chess.BISHOP:
                position_table = bishop_scores
            elif piece.piece_type == chess.ROOK:
                position_table = rook_scores
            elif piece.piece_type == chess.QUEEN:
                position_table = queen_scores
            else:  # King
                continue  # Skip position scoring for king
                
            # Flip board for black pieces
            if piece.color == chess.BLACK:
                position_score = position_table[7 - rank][file]
            else:
                position_score = position_table[rank][file]

            # Calculate final piece score
            piece_final_score = piece_value + position_score
            
            # Add to total score (positive for white, negative for black)
            if piece.color == chess.WHITE:
                score += piece_final_score
            else:
                score -= piece_final_score

        return score

    def _additional_positional_factors(self, board):
        """Calculate additional positional factors"""
        score = 0
        
        # Bonus for controlling center squares
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        for square in center_squares:
            if board.is_attacked_by(chess.WHITE, square):
                score += 0.1
            if board.is_attacked_by(chess.BLACK, square):
                score -= 0.1

        # Penalty for isolated pawns
        for file in range(8):
            white_pawns = 0
            black_pawns = 0
            for rank in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN:
                    if piece.color == chess.WHITE:
                        white_pawns += 1
                    else:
                        black_pawns += 1
            
            # Check adjacent files for isolation
            adjacent_files = []
            if file > 0:
                adjacent_files.append(file - 1)
            if file < 7:
                adjacent_files.append(file + 1)
                
            for adj_file in adjacent_files:
                for rank in range(8):
                    square = chess.square(adj_file, rank)
                    piece = board.piece_at(square)
                    if piece and piece.piece_type == chess.PAWN:
                        if piece.color == chess.WHITE:
                            white_pawns += 1
                        else:
                            black_pawns += 1
            
            if white_pawns == 1:  # Isolated white pawn
                score -= 0.2
            if black_pawns == 1:  # Isolated black pawn
                score += 0.2

        return score