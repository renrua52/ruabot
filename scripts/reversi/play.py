from reversi.game.executor import GameExecutor
from reversi.game.player import HumanPlayer, DummyPlayer, PolicyPlayer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(6)

    p1 = PolicyPlayer(config, "runs/pg/6/policy_network_ckpt_10000.pth")
    p2 = DummyPlayer(config)

    score = {0:0, 1:0, 2:0}

    for game in range(500):
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

    