from game.player import Player
from random import choice

class DummyBot(Player): # Randomly selects a legal move
    def __init__(self):
        super().__init__('Dummy Bot')
    
    def generateMove(self, position):
        available = position.allLegalMoves()
        return choice(available)
    
class Gourmand(Player): # Prioritizes capturing
    def __init__(self):
        super().__init__('Gourmand')

    def generateMove(self, position):
        from copy import deepcopy

        available = position.allLegalMoves()
        capturing = []

        for move in available:
            temp = deepcopy(position)
            if temp.makeMoveFromNotation(move):
                capturing.append(move)
        if len(capturing) > 0:
            return choice(capturing)
        return choice(available)
    
class Berserker(Player): # Prioritizes checking
    def __init__(self):
        super().__init__('Berserker')

    def generateMove(self, position):
        from copy import deepcopy

        available = position.allLegalMoves()
        checking = []

        for move in available:
            temp = deepcopy(position)
            temp.playMove(move)
            if temp.isCheck():
                checking.append(move)

        if len(checking) > 0:
            return choice(checking)
        return choice(available)