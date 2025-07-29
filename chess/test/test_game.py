import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..', 'src'))
sys.path.append(src_dir)

from game.game import InteractiveGame
from game.player import DummyBot, HumanPlayer

if __name__ == '__main__':
    w = HumanPlayer()
    b = DummyBot()
    print('Game Start')
    ig = InteractiveGame(w, b)
    ig.startInteractiveGame()