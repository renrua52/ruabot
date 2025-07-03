class Player:
    def __init__(self, name):
        self.player_name = name

    def generateMove(self, position):
        raise NotImplementedError

class HumanPlayer(Player):
    def __init__(self):
        super().__init__(input("Human Player Name: "))
    
    def generateMove(self, position):
        print("Your turn. Current Position:")
        print(position.getGrid())
        return input("Your move: ")

    
class PlayerEnsemble(Player):
    def __init__(self, player_list):
        self.player_list = player_list
        name = 'Ensemble: '
        for player in player_list:
            name += player.player_name + '+'
        super().__init__(name)

    def generateMove(self, position):
        from random import choice
        player = choice(self.player_list)
        return player.generateMove(position)