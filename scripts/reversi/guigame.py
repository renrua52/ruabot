from reversi.gui.gui import ReversiGUI
from reversi.game.player import HumanPlayer, DummyPlayer, PolicyPlayer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(6)

    p1 = HumanPlayer(config)
    p2 = PolicyPlayer(config, "runs/pg/policy_network_ckpt_20000.pth")

    gui = ReversiGUI(config, p1, p2)
    gui.run()

    