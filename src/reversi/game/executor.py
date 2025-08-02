from reversi.core.board import Board

class GameExecutor:
    def __init__(self, config, black_player, white_player, verbose=False):
        self.config = config
        self.board = Board(config)
        self.players = {
            1: black_player,
            2: white_player
        }
        self.verbose = verbose

    def step(self):
        if len(self.board.getAllLegalMoves()) == 0:
            self.board.makeEmptyMove()
            return
        move = self.players[self.board.getTurn()].generateMove(self.board)
        self.board.makeMove(move[0], move[1])

    def runGame(self):
        while self.board.getResult() == -1:
            self.step()
            if self.verbose:
                print("="*self.config["width"])
                print(f"Move {self.board.getSteps()}")
                self.board.printGrid()
                print("="*self.config["width"])

        return self.board.getResult()