from reversi.core.board import Board

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, board: Board) -> float:
        pass

class NaiveEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        pass

    def evaluate(self, board: Board):
        b, w = board.getScores()
        return float(b-w)
    
class BorderEvaluator(Evaluator):
    def __init__(self):
        super().__init__()
        pass

    def evaluate(self, board: Board):
        b, w = board.getScores()
        eval = float(b-w)
        for x, y in [
            (0, 0),
            (0, board.width-1),
            (board.height-1, 0),
            (board.height-1, board.width-1)
        ]:
            if board.getPiece(x, y) == 1:
                eval += 2 * (board.height * board.width) ** 0.5
            if board.getPiece(x, y) == 2:
                eval -= 2 * (board.height * board.width) ** 0.5

        for x in [0, board.height-1]:
            for y in range(1, board.width-1):
                if board.getPiece(x, y) == 1:
                    eval += 4
                if board.getPiece(x, y) == 2:
                    eval -= 4

        for x in range(1, board.height-1):
            for y in [0, board.width-1]:
                if board.getPiece(x, y) == 1:
                    eval += 4
                if board.getPiece(x, y) == 2:
                    eval -= 4

        return eval