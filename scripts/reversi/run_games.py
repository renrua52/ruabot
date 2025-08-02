from reversi.game.executor import GameExecutor
from reversi.game.player import HumanPlayer, DummyPlayer, PolicyPlayer
from reversi.core.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(4)

    w = DummyPlayer(config)
    b = PolicyPlayer(config)
    print(f'Game Started\n')

    g = GameExecutor(config, w, b, verbose=True)
    score = g.runGame()
    print(score)