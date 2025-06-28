from core.board import Board
import copy
import re

class Game:
    def __init__(self, startingFEN=None):
        self.board = Board(positionFEN=startingFEN)
        self.game_history = []
        self.metadata = {} #TODO

    def executeMove(self, notation):
        self.board.makeMoveFromNotation(notation)
        self.board.switchTurn()
    
    def loadPGN(self, gamePGN):
        gamePGN = re.sub(r'\[.*?\]', '', gamePGN)
        moves = gamePGN.split()

        if moves[-1] in ['1-0', '0-1', '1/2-1/2']:
            self.result = moves[-1]
            moves = moves[:-1]

        move_idx = 0
        for s in moves:
            # print(s)
            if s[-1] == '.':
                move_idx += 1
            else:
                self.executeMove(s)
                b = copy.deepcopy(self.board)
                self.game_history.append(b)
    
    def printHistory(self):
        i = 2
        for b in self.game_history:
            print(f'Move {i//2},', 'White' if i%2==0 else 'Black')
            i += 1
            b.printGrid()
            print()