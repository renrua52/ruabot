from chess.core.board import Board
from chess.game.move import Move, FullMove
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
    
    def getHistory(self):
        ret = ""
        move_idx = 0
        for fullmove in self.game_history:
            move_idx += 1
            ret += str(move_idx)+'. '
            if fullmove.moves['w'] is not None:
                ret += fullmove.moves['w'].notation + ' '
            if fullmove.moves['b'] is not None:
                ret += fullmove.moves['b'].notation + ' '
        return ret
    
    def checkoutMove(self, move_number, color):
        self.current_board = self.game_history[move_number-1].moves[color].position
    
    def printCurrentPosition(self):
        self.current_board.printGrid()

class InteractiveGame(Game):
    def __init__(self, white_player, black_player):
        super().__init__()
        self.players = {}
        self.players['w'] = white_player
        self.players['b'] = black_player

    def requestMove(self):
        return self.players[self.current_board.turn].generateMove(self.current_board)
    
    def default_terminate(g: Game) -> bool:
        if g.current_board.isCheckmate():
            if g.current_board.turn == 'w':
                return True, -1
            else:
                return True, 1
        if g.current_board.isStalemate():
            return True, 0
        return False, None
    
    def startInteractiveGame(self, terminate = default_terminate):
        move_idx = 0
        while True:
            move_idx += 1
            self.game_history.append(FullMove(move_idx))

            max_retries = 5
            retries = 0
            while retries < max_retries:
                try:
                    move = self.requestMove()
                    self.current_board.playMove(move)
                    break
                except:
                    print(f"Attempt {retries+1}/{max_retries} failed. Retrying...")
                    retries += 1
            else:
                print(f"Failed requesting move from {self.players[self.current_board.turn].player_name}.")
                raise ValueError
            self.game_history[-1].moves['w'] = Move(copy.deepcopy(self.current_board), move)

            flag, score = terminate(self)
            if flag:
                return score

            max_retries = 5
            retries = 0
            while retries < max_retries:
                try:
                    move = self.requestMove()
                    self.current_board.playMove(move)
                    break
                except:
                    print(f"Attempt {retries+1}/{max_retries} failed. Retrying...")
                    retries += 1
            else:
                print(f"Failed requesting move from {self.players[self.current_board.turn].player_name}.")
                raise ValueError
            self.game_history[-1].moves['b'] = Move(copy.deepcopy(self.current_board), move)

            flag, score = terminate(self)
            if flag:
                return score

class WeakBotGame(InteractiveGame): # A game that counts remaining pieces as score, because weak bots can hardly checkmate.
    def __init__(self, white_player, black_player):
        super().__init__(white_player, black_player)

    def startInteractiveGame(self, move_cap):
        def terminate(g: InteractiveGame) -> int:
            if g.current_board.isCheckmate():
                if g.current_board.turn == 'w':
                    return True, -100
                else:
                    return True, 100
            if (len(g.game_history) >= move_cap and g.current_board.turn == 'w') or g.current_board.isStalemate():
                white_value = len(g.current_board.pieces['w']['rook'])*5 + \
                    len(g.current_board.pieces['w']['queen'])*9 + \
                    len(g.current_board.pieces['w']['bishop'])*3 + \
                    len(g.current_board.pieces['w']['knight'])*3 + \
                    len(g.current_board.pieces['w']['pawn'])*1
                black_value = len(g.current_board.pieces['b']['rook'])*5 + \
                    len(g.current_board.pieces['b']['queen'])*9 + \
                    len(g.current_board.pieces['b']['bishop'])*3 + \
                    len(g.current_board.pieces['b']['knight'])*3 + \
                    len(g.current_board.pieces['b']['pawn'])*1
                return True, white_value-black_value
            else:
                return False, None
        return super().startInteractiveGame(terminate)

