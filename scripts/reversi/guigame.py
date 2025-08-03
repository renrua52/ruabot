from reversi.gui.gui import ReversiGUI
from reversi.game.player import HumanPlayer, DummyPlayer, PolicyPlayer
from reversi.game.utils import getDefaultConfig

if __name__ == '__main__':
    config = getDefaultConfig(8)

    p1 = HumanPlayer(config)
    p2 = DummyPlayer(config)

    gui = ReversiGUI(config, p1, p2)
    gui.run()

    