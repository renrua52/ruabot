from reversi.game.executor import GameExecutor
from reversi.game.player import HumanPlayer, DummyPlayer, GreedyPlayer, PolicyPlayer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(8)

    p1 = GreedyPlayer(config)
    p2 = DummyPlayer(config)

    score = {0:0, 1:0, 2:0}

    for game in range(400):
        print(f'Game {game+1} Started')
        if game % 2 == 0:
            g = GameExecutor(config, p1, p2, verbose=False)
            res = g.runGame()
            print(f'Winner: {res}')
            score[res] += 1
        else:
            g = GameExecutor(config, p2, p1, verbose=False)
            res = g.runGame()
            if res != 0:
                res = 3-res
            print(f'Winner: {res}')
            score[res] += 1

    print(score)

    