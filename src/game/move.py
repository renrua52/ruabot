import copy

class Move:
    def __init__(self, board, notation, time_used=None):
        self.notation = notation
        self.time_used = time_used
        self.position = copy.deepcopy(board)

class FullMove:
    def __init__(self, move_number, white_move: Move = None, black_move: Move = None):
        self.move_number = move_number
        self.moves = {
            'w': white_move,
            'b': black_move
        }