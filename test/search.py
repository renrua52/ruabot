import sys
import os
import copy


current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.append(src_dir)

def search(board, depth: int) -> int:
    if depth == 0:
        return 1
    moves = board.allLegalMoves()
    ret = 0
    for move in moves:
        tmp = copy.deepcopy(board)
        tmp.makeMoveFromNotation(move)
        tmp.switchTurn()

        res = search(tmp, depth-1)
        ret += res
    return ret



from core.board import Board

if __name__ == '__main__':
    board = Board(positionFEN="8/8/4k3/8/8/2K5/3R2R1/8 w - - 0 1")
    # print(search(board, 2))