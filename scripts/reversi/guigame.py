from reversi.gui.gui import ReversiGUI
from reversi.game.player import HumanPlayer, DummyPlayer, GreedyPlayer, PolicyPlayer, MinmaxPlayer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(8)

    p2 = HumanPlayer(config)
    # p2 = PolicyPlayer(config, "runs/pg/six/88.pth")
    p1 = MinmaxPlayer(depth=5, eval_type="border")

    gui = ReversiGUI(config, p1, p2)
    gui.run()

    