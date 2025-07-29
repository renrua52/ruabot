import sys
import os

from chess.game.game import InteractiveGame, WeakBotGame
from chess.game.player import HumanPlayer, PlayerEnsemble
from chess.bots import toy_bots

if __name__ == '__main__':
    # w = llm_bots.LLMBot("deepseek-r1")
    # w = toy_bots.DummyBot()
    w = toy_bots.DummyBot()
    b = toy_bots.Gourmand()
    f = open("runs/game_log.txt", "w")
    scoreline = 0
    f.write(f'White Player: {w.player_name}\n')
    f.write(f'Black Player: {b.player_name}\n')
    for i in range(1):
        f.write(f'Game {i+1} Started\n')
        ig = WeakBotGame(w, b)
        score = ig.startInteractiveGame(100)
        f.write(ig.getHistory())
        f.write('\n')
        scoreline += score
        f.write(f'Game {i+1} score:'+str(score)+'\n')
    f.write(f'Final scoreline: {scoreline}\n')