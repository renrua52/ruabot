from reversi.game.executor import GameExecutor
from reversi.game.player import HumanPlayer, DummyPlayer, GreedyPlayer, PolicyPlayer, MinmaxPlayer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(6)

    # p1 = GreedyPlayer(config)
    # p2 = PolicyPlayer(config, "runs/pg/six/88.pth")
    p1 = MinmaxPlayer(depth=5, eval_type="naive")
    p2 = MinmaxPlayer(depth=5, eval_type="border")
    # p2 = GreedyPlayer(config)

    score = {0:0, 1:0, 2:0}

    for game in range(10):
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

    