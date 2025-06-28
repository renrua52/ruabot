from core.board import Board
from game.move import Move, FullMove
import copy
import re

class Game: #TODO: Starting from custom position not fully supported
    def __init__(self, initialFEN=None):
        self.initial_board = Board(positionFEN=initialFEN)
        self.current_board = self.initial_board
        self.game_history = []
        self.metadata = {"FromStart": initialFEN is None} #TODO: read metadata from PGN
    
    def loadPGN(self, gamePGN):
        pattern = re.compile(r'\[([^\[\]]+)\s+"([^"]+)"\]')
        matches = pattern.findall(gamePGN)
        for key, value in matches:
            self.metadata[key.strip()] = value.strip()

        gamePGN = re.sub(r'\[.*?\]', '', gamePGN)
        moves = gamePGN.split()

        if moves[-1] in ['1-0', '0-1', '1/2-1/2']:
            self.result = moves[-1]
            moves = moves[:-1]

        tmp = copy.deepcopy(self.initial_board)

        for s in moves:
            if s[-1] == '.':
                self.game_history.append(FullMove(int(s[:-1])))
            else:
                color = tmp.turn
                tmp.playMove(s)
                self.game_history[-1].moves[color] = Move(copy.deepcopy(tmp), s)
    
    def printHistory(self):
        move_idx = 0
        for fullmove in self.game_history:
            move_idx += 1
            print(str(move_idx)+'.', end=' ')
            if fullmove.moves['w'] is not None:
                print(fullmove.moves['w'].notation, end=' ')
            if fullmove.moves['b'] is not None:
                print(fullmove.moves['b'].notation, end=' ')
    
    def checkoutMove(self, move_number, color):
        self.current_board = self.game_history[move_number-1].moves[color].position
    
    def printCurrentPosition(self):
        self.current_board.printGrid()

class InteractiveGame(Game):
    def __init__(self, white_player, black_player):
        super(InteractiveGame, self).__init__()
        self.players = {}
        self.players['w'] = white_player
        self.players['b'] = black_player

    def requestMove(self):
        return self.players[self.current_board.turn].generateMove(self.current_board)
    
    def startInteractiveGame(self, move_cap = None):
        move_idx = 0
        while move_cap is None or move_idx < move_cap:
            move_idx += 1
            self.game_history.append(FullMove(move_idx))

            move = self.requestMove()
            self.current_board.playMove(move)
            self.game_history[-1].moves['w'] = Move(copy.deepcopy(self.current_board), move)

            if self.current_board.isCheckmate():
                print('Checkmate, 1-0.')
                break

            move = self.requestMove()
            self.current_board.playMove(move)
            self.game_history[-1].moves['b'] = Move(copy.deepcopy(self.current_board), move)

            if self.current_board.isCheckmate():
                print('Checkmate, 0-1.')
                break

