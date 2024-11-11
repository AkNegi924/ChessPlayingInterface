import math
import chess


class Node:
    def __init__(self, board=chess.Board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move  # Move that led to this node
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = list(board.legal_moves)

    def ucb1(self, c=1.41):
        if self.visits == 0:
            return float("inf")
        return (self.wins / self.visits) + c * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

    def is_terminal(self):
        return self.board.is_game_over()

    def expand(self):
        move = self.untried_moves.pop()
        new_board = self.board.copy()
        new_board.push(move)
        child_node = Node(new_board, parent=self, move=move)
        self.children.append(child_node)
        return child_node


# class Node:
#     def __init__(
#         self,
#         board: chess.Board,
#         parent: Optional["Node"] = None,
#         move: Optional[chess.Move] = None,
#     ):
#         self.board = board
#         self.parent = parent
#         self.move = move
#         self.wins = 0
#         self.visits = 0
#         self.children: List[Node] = []
#         self.untried_moves = list(board.legal_moves)
#         self.evaluation = 0.5  # Initialize with neutral evaluation

#     def expand(self) -> "Node":
#         move = self.untried_moves.pop()
#         new_board = self.board.copy()
#         new_board.push(move)
