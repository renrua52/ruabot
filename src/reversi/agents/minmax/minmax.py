from reversi.core.board import Board
from copy import deepcopy
from reversi.agents.minmax.evaluator import Evaluator

class MinmaxSearcher:
    def __init__(self, evaluator: Evaluator):
        self.evaluator = evaluator

    def minmaxMove(self, board: Board, depth: int, role: int) -> tuple[tuple[int, int], float]:
        '''
        Generates the best move in terms of minimizing/maximizing evaluation in given depth. \\
        **Args**: role: 1 for max and -1 for min
        '''
        if depth == 0 or board.getResult() >= 0:
            return None, self.evaluator.evaluate(board)

        moves = board.getAllLegalMoves()

        best = -float('inf')
        best_move = None

        if len(moves) == 0:
            next_board = deepcopy(board)
            next_board.makeEmptyMove()
            _, eval = self.minmaxMove(next_board, depth-1, -role)
            return None, eval

        for move in moves:
            next_board = deepcopy(board)
            next_board.makeMove(move[0], move[1])
            _, eval = self.minmaxMove(next_board, depth-1, -role)
            if eval*role > best:
                best_move = move
                best = eval*role
        
        return best_move, best*role
    
    def bestMove(self, board: Board, depth: int):
        assert len(board.getAllLegalMoves()) != 0

        if board.getTurn() == 1:
            move, eval = self.minmaxMove(board, depth, 1)
        else:
            move, eval = self.minmaxMove(board, depth, -1)
        return move