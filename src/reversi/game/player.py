class Player:
    def __init__(self, name):
        self.player_name = name

    def generateMove(self, board):
        raise NotImplementedError

class HumanPlayer(Player):
    def __init__(self, config):
        super().__init__(input("Human Player Name: "))
    
    def generateMove(self, board):
        print("Your turn. Current Position:")
        board.printGrid()
        move = tuple(map(int, input("Your move: ").split()))
        return move
    
class DummyPlayer(Player):
    def __init__(self, config):
        super().__init__("dummy")
    
    def generateMove(self, board):
        legal_moves = board.getAllLegalMoves()
        from random import choice
        return choice(legal_moves)
    
class PolicyPlayer(Player):
    def __init__(self, config, weight_path=None):
        super().__init__("policy")
        from reversi.agents.pg.agent import PGAgent
        self.agent = PGAgent(config, False)
        if weight_path:
            self.agent.load_weights(weight_path)

    def generateMove(self, board):
        move, _ = self.agent.selectAction(board)
        return move
