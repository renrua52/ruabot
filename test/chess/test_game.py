import sys
import os

from chess.game.game import InteractiveGame
from chess.game.player import DummyBot, HumanPlayer

if __name__ == '__main__':
    w = HumanPlayer()
    b = DummyBot()
    print('Game Start')
    ig = InteractiveGame(w, b)
    ig.startInteractiveGame()