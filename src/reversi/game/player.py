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
    
class GreedyPlayer(Player):
    def __init__(self, config):
        super().__init__("greedy")

    def generateMove(self, board):
        legal_moves = board.getAllLegalMoves()
        best_moves = []
        current_player = board.getTurn()

        best = -10000

        from copy import deepcopy
        for move in legal_moves:
            tmp = deepcopy(board)
            tmp.makeMove(move[0], move[1])
            b, w = tmp.getScores()
            adv = b - w if current_player == 1 else w - b
            if adv == best:
                best_moves.append(move)
            elif adv > best:
                best_moves = []
                best_moves.append(move)
                best = adv
        from random import choice
        return choice(best_moves)
    
class PolicyPlayer(Player):
    def __init__(self, config, weight_path=None):
        super().__init__("policy")
        from reversi.agents.pg.agent import PGAgent
        self.agent = PGAgent(config, False)
        if weight_path:
            self.agent.load_weights(weight_path)

    def generateMove(self, board):
        move, _ = self.agent.selectAction(board, do_sample=False)
        return move


class MinmaxPlayer(Player):
    def __init__(self, depth: int, eval_type: str = 'naive'):
        super().__init__("minmax")

        from reversi.agents.minmax.evaluator import NaiveEvaluator, BorderEvaluator
        from reversi.agents.minmax.minmax import MinmaxSearcher
        if eval_type == 'naive':
            evaluator = NaiveEvaluator()
        if eval_type == 'border':
            evaluator = BorderEvaluator()
            
        self.searcher = MinmaxSearcher(evaluator)
        self.depth = depth

    def generateMove(self, board):
        return self.searcher.bestMove(board, self.depth)