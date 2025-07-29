from chess.core.piece import instantiatePiece
from chess.core.utils import square2xy, xy2square, parseNotation, meetSpecifier, piece2letter, swapColor

import copy
import re

class Board:
    def __init__(self, positionFEN=None, board_width=8, board_height=8, ):
        if positionFEN is None:
            positionFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.width = board_width
        self.height = board_height
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.pieces = {
            'w': {
                'king': set(),
                'knight': set(),
                'bishop': set(),
                'pawn': set(),
                'rook': set(),
                'queen': set()
            },
            'b': {
                'king': set(),
                'knight': set(),
                'bishop': set(),
                'pawn': set(),
                'rook': set(),
                'queen': set()
            }
        }

        self.setupFromFEN(positionFEN)

    def setupFromFEN(self, FEN):
        try:
            elements = FEN.split(" ")
            ranks = elements[0].split("/")
            ranks = ranks[::-1]
            if len(elements) != 6 or len(ranks) != self.height:
                raise Exception('Invalid FEN format')
           
            for i in range(len(ranks)):
                ranks[i] = re.sub(r'\d+', lambda match: '-'*int(match.group(0)), ranks[i])

                for j in range(len(ranks[i])):
                    if ranks[i][j] == '-':
                        self.grid[j][i] = None
                    else:
                        p = instantiatePiece(ranks[i][j], j, i)
                        self.grid[j][i] = p
                        if p.color == 'w':
                            self.pieces['w'][p.piece_type].add(p)
                        if p.color == 'b':
                            self.pieces['b'][p.piece_type].add(p)

            
            self.turn = elements[1]
            self.castle = elements[2]
            self.enpassant = elements[3]
            #TODO: maintain features below
            self.fifty_count = int(elements[4])
            self.move_count = int(elements[5])

        except Exception as e:
            print(f'Error: {e}')

    def generateFEN(self): # Haven't been immensely tested.
        retFEN = ""
        for i in range(self.height):
            empty = 0
            for j in range(self.width):
                x, y = j, self.height-i-1
                if self.grid[x][y] == None:
                    empty += 1
                else:
                    if empty:
                        retFEN += str(empty)
                        empty = 0
                    retFEN += piece2letter(self.grid[x][y])
            if empty:
                retFEN += str(empty)
            if i < self.height-1:
                retFEN += "/"
        
        retFEN += " " + self.turn
        retFEN += " " + self.castle
        retFEN += " " + self.enpassant
        retFEN += " " + str(self.fifty_count)
        retFEN += " " + str(self.move_count)
        
        return retFEN
    
    def getPiece(self, x, y):
        return self.grid[x][y]
    
    def getPieceFromSquare(self, square):
        x, y = square2xy(square)
        return self.getPiece(x, y)
    
    def clearSquare(self, x, y):
        p = self.grid[x][y]
        if p is None:
            return
        self.pieces[p.color][p.piece_type].remove(p)
        self.grid[x][y] = None

    def legalMoves(self, xs: int, ys: int) -> tuple:
        p = self.getPiece(xs, ys)
        if p is None:
            return None
        
        inRange = lambda x, y: 0 <= x < self.width and 0 <= y < self.height
        isEmpty = lambda x, y: self.grid[x][y] is None
        sameColor = lambda x1, y1, x2, y2: self.grid[x1][y1].color == self.grid[x2][y2].color
        
        viable = []

        if p.piece_type == 'knight':
            candidate_moves = [
                (xs+1, ys+2),
                (xs+1, ys-2),
                (xs-1, ys+2),
                (xs-1, ys-2),
                (xs+2, ys+1),
                (xs+2, ys-1),
                (xs-2, ys+1),
                (xs-2, ys-1)
            ]
            for xt, yt in candidate_moves:
                if not inRange(xt, yt):
                    continue
                if isEmpty(xt, yt) or not sameColor(xs, ys, xt, yt):
                    viable.append((xt, yt))

        if p.piece_type == 'rook':
            steps = [
                lambda x, y: (x+1, y),
                lambda x, y: (x-1, y),
                lambda x, y: (x, y+1),
                lambda x, y: (x, y-1),
            ]
            for step in steps:
                xt, yt = xs, ys
                while True:
                    xt, yt = step(xt, yt)
                    if not inRange(xt, yt):
                        break
                    if isEmpty(xt, yt):
                        viable.append((xt, yt))
                    elif not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        break
                    elif sameColor(xs, ys, xt, yt):
                        break
        if p.piece_type == 'bishop':
            steps = [
                lambda x, y: (x+1, y+1),
                lambda x, y: (x-1, y+1),
                lambda x, y: (x-1, y-1),
                lambda x, y: (x+1, y-1),
            ]
            for step in steps:
                xt, yt = xs, ys
                while True:
                    xt, yt = step(xt, yt)
                    if not inRange(xt, yt):
                        break
                    if isEmpty(xt, yt):
                        viable.append((xt, yt))
                    elif not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        break
                    elif sameColor(xs, ys, xt, yt):
                        break
                
        if p.piece_type == 'queen':
            steps = [
                lambda x, y: (x+1, y),
                lambda x, y: (x-1, y),
                lambda x, y: (x, y+1),
                lambda x, y: (x, y-1),
                lambda x, y: (x+1, y+1),
                lambda x, y: (x-1, y+1),
                lambda x, y: (x-1, y-1),
                lambda x, y: (x+1, y-1),
            ]
            for step in steps:
                xt, yt = xs, ys
                while True:
                    xt, yt = step(xt, yt)
                    if not inRange(xt, yt):
                        break
                    if isEmpty(xt, yt):
                        viable.append((xt, yt))
                    elif not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        break
                    elif sameColor(xs, ys, xt, yt):
                        break

        if p.piece_type == 'king':
            candidate_moves = [
                (xs+1, ys),
                (xs-1, ys),
                (xs, ys+1),
                (xs, ys-1),
                (xs+1, ys+1),
                (xs-1, ys+1),
                (xs-1, ys-1),
                (xs+1, ys-1),
            ]
            for xt, yt in candidate_moves:
                if not inRange(xt, yt):
                    continue
                if isEmpty(xt, yt) or not sameColor(xs, ys, xt, yt):
                    viable.append((xt, yt))

        enp_move = None
        if p.piece_type == 'pawn':
            step = 1 if p.color == 'w' else -1
            orig = (p.color == 'w' and ys == 1) or (p.color == 'b' and ys == self.height-1-1)
            queening = (p.color == 'w' and ys == self.height-1-1) or (p.color == 'b' and ys == 1)

            if self.grid[xs][ys+step] is None:
                viable.append((xs, ys+step))
                # First pawn move
                if orig and self.grid[xs][ys+step*2] is None and not queening:
                    viable.append((xs, ys+step*2))
            # Pawn capture
            for xt, yt in [
                (xs+1, ys+step),
                (xs-1, ys+step)
            ]:
                if inRange(xt, yt):
                    if self.enpassant == xy2square(xt, yt):
                        # assert isEmpty(xt, yt)
                        # temp = copy.deepcopy(self)
                        # assert temp.getPiece(xt, ys).piece_type == 'pawn'
                        # temp.clearSquare(xt, ys)
                        # temp.movePiece(xs, ys, xt, yt)
                        # if not temp.isCheck():
                        enp_move = (xt, yt)
                    elif not isEmpty(xt, yt) and self.grid[xt][yt].color != p.color:
                        viable.append((xt, yt))

        moves = []
        for (xt, yt) in viable:
            temp = copy.deepcopy(self)
            temp.movePiece(xs, ys, xt, yt)
            if not temp.isCheck():
                moves.append((xt, yt))
        if enp_move is not None:
            moves.append(enp_move)

        return moves

    def protectingSquares(self, xs, ys):
        p = self.getPiece(xs, ys)
        if p is None:
            return None
        
        inRange = lambda x, y: 0 <= x < self.width and 0 <= y < self.height
        isEmpty = lambda x, y: self.grid[x][y] is None
        sameColor = lambda x1, y1, x2, y2: self.grid[x1][y1].color == self.grid[x2][y2].color
        
        protecting = []

        if p.piece_type == 'knight':
            candidate_moves = [
                (xs+1, ys+2),
                (xs+1, ys-2),
                (xs-1, ys+2),
                (xs-1, ys-2),
                (xs+2, ys+1),
                (xs+2, ys-1),
                (xs-2, ys+1),
                (xs-2, ys-1)
            ]
            for xt, yt in candidate_moves:
                if not inRange(xt, yt):
                    continue
                protecting.append((xt, yt))

        if p.piece_type == 'rook':
            steps = [
                lambda x, y: (x+1, y),
                lambda x, y: (x-1, y),
                lambda x, y: (x, y+1),
                lambda x, y: (x, y-1),
            ]
            for step in steps:
                xt, yt = xs, ys
                while True:
                    xt, yt = step(xt, yt)
                    if not inRange(xt, yt):
                        break
                    elif isEmpty(xt, yt):
                        protecting.append((xt, yt))
                    else:
                        protecting.append((xt, yt))
                        break
        if p.piece_type == 'bishop':
            steps = [
                lambda x, y: (x+1, y+1),
                lambda x, y: (x-1, y+1),
                lambda x, y: (x-1, y-1),
                lambda x, y: (x+1, y-1),
            ]
            for step in steps:
                xt, yt = xs, ys
                while True:
                    xt, yt = step(xt, yt)
                    if not inRange(xt, yt):
                        break
                    elif isEmpty(xt, yt):
                        protecting.append((xt, yt))
                    else:
                        protecting.append((xt, yt))
                        break
                
        if p.piece_type == 'queen':
            steps = [
                lambda x, y: (x+1, y),
                lambda x, y: (x-1, y),
                lambda x, y: (x, y+1),
                lambda x, y: (x, y-1),
                lambda x, y: (x+1, y+1),
                lambda x, y: (x-1, y+1),
                lambda x, y: (x-1, y-1),
                lambda x, y: (x+1, y-1),
            ]
            for step in steps:
                xt, yt = xs, ys
                while True:
                    xt, yt = step(xt, yt)
                    if not inRange(xt, yt):
                        break
                    elif isEmpty(xt, yt):
                        protecting.append((xt, yt))
                    else:
                        protecting.append((xt, yt))
                        break

        if p.piece_type == 'king':
            candidate_moves = [
                (xs+1, ys),
                (xs-1, ys),
                (xs, ys+1),
                (xs, ys-1),
                (xs+1, ys+1),
                (xs-1, ys+1),
                (xs-1, ys-1),
                (xs+1, ys-1),
            ]
            for xt, yt in candidate_moves:
                if not inRange(xt, yt):
                    continue
                protecting.append((xt, yt))

        if p.piece_type == 'pawn':
            step = 1 if p.color == 'w' else -1
            # Pawn capture
            for xt, yt in [
                (xs+1, ys+step),
                (xs-1, ys+step)
            ]:
                if inRange(xt, yt):
                    protecting.append((xt, yt))

        return protecting

    def protectedSquares(self, color):
        ret = set()
        for key, pcs in self.pieces[color].items():
            for p in pcs:
                protected = self.protectingSquares(p.x, p.y)
                ret = ret.union(set(protected))
        return ret

    def canCastle(self, flag):
        if flag == 'O-O':
            ch = 'K' if self.turn == 'w' else 'k'
        elif flag == 'O-O-O':
            ch = 'Q' if self.turn == 'w' else 'q'
        else:
            raise ValueError("Invalid method call: canCastle().")

        if not ch in self.castle:
            return False
        if self.isCheck():
            return False

        isEmpty = lambda x, y: self.grid[x][y] is None
        if ch == 'K':
            if not isEmpty(*square2xy('f1')) or \
            not isEmpty(*square2xy('g1')):
                return False
            if square2xy('f1') in self.protectedSquares(swapColor(self.turn)) or \
            square2xy('g1') in self.protectedSquares(swapColor(self.turn)):
                return False
        if ch == 'k':
            if not isEmpty(*square2xy('f8')) or \
            not isEmpty(*square2xy('g8')):
                return False
            if square2xy('f8') in self.protectedSquares(swapColor(self.turn)) or \
            square2xy('g8') in self.protectedSquares(swapColor(self.turn)):
                return False
        if ch == 'Q':
            if not isEmpty(*square2xy('b1')) or \
            not isEmpty(*square2xy('c1')) or \
            not isEmpty(*square2xy('d1')):
                return False
            if square2xy('c1') in self.protectedSquares(swapColor(self.turn)) or \
            square2xy('d1') in self.protectedSquares(swapColor(self.turn)):
                return False
        if ch == 'q':
            if not isEmpty(*square2xy('b8')) or \
            not isEmpty(*square2xy('c8')) or \
            not isEmpty(*square2xy('d8')):
                return False
            if square2xy('c8') in self.protectedSquares(swapColor(self.turn)) or \
            square2xy('d8') in self.protectedSquares(swapColor(self.turn)):
                return False
        return True
    

    def movePiece(self, xs, ys, xt, yt):
        '''
        Brings the piece at (xs, ys) to (xt, yt), eliminating the one in target square. \\
        **Return**: False for no capture, True for capture.
        '''
        if self.grid[xs][ys] is None:
            raise ValueError("Illegal call: empty start square.")
        
        if self.grid[xt][yt] is not None and self.grid[xt][yt].piece_type == 'king':
            raise ValueError("Illegal move: king capture.")

        is_capture = False
        if self.grid[xt][yt] is not None:
            is_capture = True
            self.clearSquare(xt, yt)
        
        self.grid[xt][yt] = self.grid[xs][ys]
        self.grid[xt][yt].x, self.grid[xt][yt].y = xt, yt

        self.grid[xs][ys] = None

        return is_capture
    

    def makeMoveFromNotation(self, notation): #TODO: also support a1-b2 format
        pc, target_sq, spec, flag = parseNotation(notation)

        # Castling
        if flag in ['O-O', 'O-O-O']:
            if flag == 'O-O':
                ch = 'K' if self.turn == 'w' else 'k'
            elif flag == 'O-O-O':
                ch = 'Q' if self.turn == 'w' else 'q'
            if not self.canCastle(flag):
                raise ValueError(f"Illegal castle {flag}.")
            
            if ch == 'K':
                self.movePiece(4, 0, 6, 0)
                self.movePiece(7, 0, 5, 0)
            if ch == 'k':
                self.movePiece(4, 7, 6, 7)
                self.movePiece(7, 7, 5, 7)
            if ch == 'Q':
                self.movePiece(4, 0, 2, 0)
                self.movePiece(0, 0, 3, 0)
            if ch == 'q':
                self.movePiece(4, 7, 2, 7)
                self.movePiece(0, 7, 3, 7)

            if self.turn == 'w':
                self.castle = self.castle.replace('K', '')
                self.castle = self.castle.replace('Q', '')
            else:
                self.castle = self.castle.replace('k', '')
                self.castle = self.castle.replace('q', '')

            self.enpassant = '-'
            return False
        
        candidate_pieces = []
            
        for p in self.pieces[self.turn][pc]:
            if meetSpecifier(p.x, p.y, spec) and square2xy(target_sq) in self.legalMoves(p.x, p.y):
                candidate_pieces.append(p)

        if len(candidate_pieces) == 0:
            raise ValueError(f"Illegal move: {notation}")
        if len(candidate_pieces) > 1:
            raise ValueError(f"Ambiguous move: {notation}")

        xs, ys = candidate_pieces[0].x, candidate_pieces[0].y
        xt, yt = square2xy(target_sq)

        # Set enpassant
        enp = self.enpassant
        self.enpassant = '-'
        if pc == 'pawn':
            if self.turn == 'w' and ys == 1 and yt == 3:
                for xp in [xt-1, xt+1]:
                    if 0 <= xp < self.width and self.grid[xp][yt] is not None:
                        p = self.grid[xp][yt]
                        if p.piece_type == 'pawn' and p.color != self.turn:
                            temp = copy.deepcopy(self)
                            temp.clearSquare(xs, ys)
                            temp.movePiece(p.x, p.y, xt, yt-1)
                            temp.switchTurn()
                            if not temp.isCheck():
                                self.enpassant = xy2square(xt, yt-1)
            elif self.turn == 'b' and ys == 6 and yt == 4:
                for xp in [xt-1, xt+1]:
                    if 0 <= xp < self.width and self.grid[xp][yt] is not None:
                        p = self.grid[xp][yt]
                        if p.piece_type == 'pawn' and p.color != self.turn:
                            temp = copy.deepcopy(self)
                            temp.clearSquare(xs, ys)
                            temp.movePiece(p.x, p.y, xt, yt+1)
                            temp.switchTurn()
                            if not temp.isCheck():
                                self.enpassant = xy2square(xt, yt+1)

        # Negate castle rights
        if (xs, ys) == square2xy('e1'):
            self.castle = self.castle.replace('K', '')
            self.castle = self.castle.replace('Q', '')
        if (xs, ys) == square2xy('e8'):
            self.castle = self.castle.replace('k', '')
            self.castle = self.castle.replace('q', '')
        if (xs, ys) == square2xy('a1') or (xt, yt) == square2xy('a1'):
            self.castle = self.castle.replace('Q', '')
        if (xs, ys) == square2xy('a8') or (xt, yt) == square2xy('a8'):
            self.castle = self.castle.replace('q', '')
        if (xs, ys) == square2xy('h1') or (xt, yt) == square2xy('h1'):
            self.castle = self.castle.replace('K', '')
        if (xs, ys) == square2xy('h8') or (xt, yt) == square2xy('h8'):
            self.castle = self.castle.replace('k', '')

        # En-passant
        if enp == xy2square(xt, yt) and self.grid[xs][ys].piece_type == 'pawn':
            assert self.grid[xt][yt] is None
            if self.turn == 'w':
                assert self.getPiece(xt, yt-1).piece_type == 'pawn'
                self.clearSquare(xt, yt-1)
            else:
                assert self.getPiece(xt, yt+1).piece_type == 'pawn'
                self.clearSquare(xt, yt+1)
            self.movePiece(xs, ys, xt, yt)
            return True

        ret = self.movePiece(xs, ys, xt, yt)

        # Promotion
        if flag is not None:
            self.clearSquare(xt, yt)
            flag = flag.upper() if self.turn == 'w' else flag.lower()
            pr = instantiatePiece(flag, xt, yt)
            self.grid[xt][yt] = pr
            if pr.color == 'w':
                self.pieces['w'][pr.piece_type].add(pr)
            if pr.color == 'b':
                self.pieces['b'][pr.piece_type].add(pr)
        
        return ret
    
    def isCheck(self):
        king = list(self.pieces[self.turn]['king'])[0]
        if (king.x, king.y) in self.protectedSquares(swapColor(self.turn)):
            return True
        return False
        
    def isCheckmate(self):
        return self.isCheck() and len(self.allLegalMoves()) == 0
    
    def isStalemate(self):
        return not self.isCheck() and len(self.allLegalMoves()) == 0
    
    def switchTurn(self):
        self.turn = swapColor(self.turn)
    
    def getGrid(self):
        ret = ""
        for i in range(self.height):
            for j in range(self.width):
                x = j
                y = self.height-i-1
                if self.grid[x][y] is None:
                    ret += '* '
                    # print('*', end=' ')
                else:
                    ret += piece2letter(self.grid[x][y]) + ' '
            ret += "\n"
        return ret
    
    # def printPieces(self):
    #     print('===== White Pieces =====')
    #     for key, pcs in self.pieces['w'].items(): 
    #         for p in pcs:
    #             print(key, 'at', xy2square(p.x, p.y))
    #     print('===== Black Pieces =====')
    #     for key, pcs in self.pieces['b'].items(): 
    #         for p in pcs:
    #             print(key, 'at', xy2square(p.x, p.y))

    def allLegalMoves(self):
        ret = []
        for key, pcs in self.pieces[self.turn].items():
            for p in pcs:
                moves = self.legalMoves(p.x, p.y)
                for move in moves:
                    if p.piece_type == 'pawn' and \
                    ((p.color == 'w' and p.y == self.height-1-1) or (p.color == 'b' and p.y == 1)):
                        # promotion
                        for promotion in ['Q', 'R', 'B', 'N']:
                            ret.append(piece2letter(p).upper()+xy2square(p.x, p.y)+xy2square(*move)+'='+promotion)
                    else:
                        ret.append(piece2letter(p).upper()+xy2square(p.x, p.y)+xy2square(*move))
        if self.canCastle('O-O'):
            ret.append('O-O')
        if self.canCastle('O-O-O'):
            ret.append('O-O-O')

        return ret

    def playMove(self, move):
        self.makeMoveFromNotation(move)
        self.switchTurn()
