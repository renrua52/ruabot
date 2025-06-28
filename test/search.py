import sys
import os
import copy


current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.append(src_dir)

def search(board, depth: int) -> int:
    if depth == 0:
        return 1
    moves = board.list_all_moves()
    ret = 0
    for move in moves:
        # if depth == 2:
        #     print(move)

        tmp = copy.deepcopy(board)
        tmp.makeMoveFromNotation(move)
        tmp.switchTurn()

        res = search(tmp, depth-1)
        ret += res

        # if depth == 2:
        #     print(res)
    return ret



from core.board import Board

if __name__ == '__main__':
    board = Board(positionFEN="r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/5Q1p/PPPBBPPP/RN2K2R b KQkq - 0 1")
    # print(search(board, 2))
    # board.makeMoveFromNotation('b3')
    # board.switchTurn()
    # board.makeMoveFromNotation('Nb1')
    # board.switchTurn()

    board.printGrid()
    # print(board.list_all_moves())
    print(search(board, 2))

#     std = """b4b3: 50
# g6g5: 48
# c7c6: 50
# d7d6: 48
# c7c5: 50
# h3g2: 47
# e6d5: 48
# b6a4: 48
# b6c4: 46
# b6d5: 48
# b6c8: 49
# f6e4: 51
# f6g4: 48
# f6d5: 49
# f6h5: 50
# f6h7: 50
# f6g8: 50
# a6e2: 42
# a6d3: 44
# a6c4: 46
# a6b5: 48
# a6b7: 49
# a6c8: 49
# g7h6: 49
# g7f8: 49
# a8b8: 49
# a8c8: 49
# a8d8: 49
# h8h4: 49
# h8h5: 49
# h8h6: 49
# h8h7: 49
# h8f8: 49
# h8g8: 49
# e7c5: 49
# e7d6: 48
# e7d8: 49
# e7f8: 49
# e8d8: 49
# e8f8: 49
# e8g8: 49
# e8c8: 49"""

#     sp = std.split()
#     # print(len(sp))

#     for i in range(len(sp)//2):
#         move = sp[i*2][:-1]
#         cnt = sp[i*2+1]
#         tmp = copy.deepcopy(board)
#         tmp.makeMoveFromNotation(move)
#         tmp.switchTurn()
#         print(move)
#         print(search(tmp, 1))


