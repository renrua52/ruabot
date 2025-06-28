class Player:
    def __init__(self, name):
        self.player_name = name

    def generateMove(self, position):
        raise NotImplementedError

class DummyBot(Player):
    def __init__(self):
        super().__init__('Dummy Bot')
    
    def generateMove(self, position):
        available = position.allLegalMoves()
        from random import choice
        return choice(available)

class HumanPlayer(Player):
    def __init__(self):
        super().__init__(input("Human Player Name: "))
    
    def generateMove(self, position):
        print("Your turn. Current Position:")
        position.printGrid()
        return input("Your move: ")