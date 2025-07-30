import torch

def getModelInput(board):
    grid = board.getGrid()
    height, width = board.getSize()
    ret = torch.zeros(3, height, width)
    for i in range(height):
        for j in range(width):
            ret[grid[i][j]][i][j] = 1

    return ret.unsqueeze(0)

