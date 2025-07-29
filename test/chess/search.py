import sys
import os
import copy


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



from chess.core.board import Board

if __name__ == '__main__':
    board = Board(positionFEN="8/8/4k3/8/8/2K5/3R2R1/8 w - - 0 1")
    # print(search(board, 2))