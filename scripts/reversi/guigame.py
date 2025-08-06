from reversi.gui.gui import ReversiGUI
from reversi.game.player import HumanPlayer, DummyPlayer, GreedyPlayer, PolicyPlayer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(6)

    p1 = HumanPlayer(config)
    p2 = GreedyPlayer(config)
    # p1 = PolicyPlayer(config, "runs/pg/six/88.pth")

    gui = ReversiGUI(config, p1, p2)
    gui.run()

    