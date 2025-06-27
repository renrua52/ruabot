from piece import instantiatePiece

from utils import square2xy, xy2square, parseMove, meetSpecifier, piece2letter, swapColor

import re

defaultFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class Board:
    def __init__(self, board_width=8, board_height=8, positionFEN=defaultFEN):
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
                # if len(ranks[i]) != self.width:
                #     raise Exception('Invalid FEN format')

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

            #TODO: maintain these features
            self.turn = elements[1]
            self.castle = list(elements[2])
            self.enpassant = elements[3]
            self.fifty_count = int(elements[4])
            self.move_count = int(elements[5])

        except Exception as e:
            print(f'Error: {e}')

    def generateFEN():
        raise NotImplementedError
    
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

    def pieceMoves(self, xs: int, ys: int, protection_only: bool=False) -> tuple:
        '''
        first ret: true 'legal' target squares\\
        second ret: squares that opponent king cannot step into, due to the existence of this piece
        '''
        p = self.getPiece(xs, ys)
        if p is None:
            return None
        
        inRange = lambda x, y: 0 <= x < self.width and 0 <= y < self.height
        isEmpty = lambda x, y: self.grid[x][y] is None
        sameColor = lambda x1, y1, x2, y2: self.grid[x1][y1].color == self.grid[x2][y2].color
        
        viable = []
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
                if isEmpty(xt, yt) or not sameColor(xs, ys, xt, yt):
                    viable.append((xt, yt))
                    protecting.append((xt, yt))
                elif sameColor(xs, ys, xt, yt):
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
                    if isEmpty(xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
                    elif not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
                        break
                    elif sameColor(xs, ys, xt, yt):
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
                    if isEmpty(xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
                    elif not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
                        break
                    elif sameColor(xs, ys, xt, yt):
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
                    if isEmpty(xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
                    elif not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
                        break
                    elif sameColor(xs, ys, xt, yt):
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
                # print(xt, yt)
                # print(isEmpty(xt, yt))
                if isEmpty(xt, yt) or not sameColor(xs, ys, xt, yt):
                    if protection_only:
                        protecting.append((xt, yt))
                    else:
                        if (xt, yt) in self.protectedSquares(swapColor(self.turn)):
                            # print(xt, yt)
                            protecting.append((xt, yt))
                        else:
                            viable.append((xt, yt))
                            protecting.append((xt, yt))
                elif sameColor(xs, ys, xt, yt):
                    protecting.append((xt, yt))

        if p.piece_type == 'pawn':
            step = 1 if p.color == 'w' else -1
            orig = (p.color == 'w' and ys == 1) or (p.color == 'b' and ys == self.height-1-1)
            queening = (p.color == 'w' and ys == self.height-1-1) or (p.color == 'b' and ys == 1)

            if self.grid[xs][ys+step] is None:
                viable.append((xs, ys+step))
                if orig and self.grid[xs][ys+step*2] is None and not queening:
                    viable.append((xs, ys+step*2))
            
            for xt, yt in [
                (xs+1, ys+step),
                (xs-1, ys+step)
            ]:
                if inRange(xt, yt):
                    if isEmpty(xt, yt):
                        protecting.append((xt, yt))
                    else:
                        if self.grid[xt][yt].color != p.color:
                            viable.append((xt, yt))
                            protecting.append((xt, yt))
                        elif sameColor(xs, ys, xt, yt):
                            protecting.append((xt, yt))

        return viable, protecting

    def protectedSquares(self, color):
        ret = set()
        for key, pcs in self.pieces[color].items():
            for p in pcs:
                _, protected = self.pieceMoves(p.x, p.y, protection_only=True)
                if (4, 4) in protected:
                    print(p.x, p.y)
                ret = ret.union(set(protected))
        return ret

    def makeMove(self, xs, ys, xt, yt):
        if self.grid[xs][ys] is None:
            raise ValueError("Illegal call: empty start square.")
        
        if self.grid[xt][yt] is not None and self.grid[xt][yt].piece_type == 'king':
            raise ValueError("Illegal move: king capture.")

        is_capture = 0
        if self.grid[xt][yt] is not None:
            is_capture = 1
            self.clearSquare(xt, yt)
        
        self.grid[xt][yt] = self.grid[xs][ys]
        self.grid[xt][yt].x, self.grid[xt][yt].y = xt, yt

        self.grid[xs][ys] = None

        return is_capture
    
    def canCastle(self, ch):
        color = 'w' if ch == ch.upper() else 'b'
        if not ch in self.castle:
            return False
        isEmpty = lambda x, y: self.grid[x][y] is None
        if ch == 'K':
            if not isEmpty(*square2xy('f1')) or \
            not isEmpty(*square2xy('g1')):
                return False
            if square2xy('f1') in self.protectedSquares(swapColor(color)) or \
            square2xy('g1') in self.protectedSquares(swapColor(color)):
                return False
        if ch == 'k':
            if not isEmpty(*square2xy('f8')) or \
            not isEmpty(*square2xy('g8')):
                return False
            if square2xy('f8') in self.protectedSquares(swapColor(color)) or \
            square2xy('g8') in self.protectedSquares(swapColor(color)):
                return False
        if ch == 'Q':
            if not isEmpty(*square2xy('c1')) or \
            not isEmpty(*square2xy('d1')):
                return False
            if square2xy('c1') in self.protectedSquares(swapColor(color)) or \
            square2xy('d1') in self.protectedSquares(swapColor(color)):
                return False
        if ch == 'q':
            if not isEmpty(*square2xy('c8')) or \
            not isEmpty(*square2xy('d8')):
                return False
            if square2xy('c8') in self.protectedSquares(swapColor(color)) or \
            square2xy('d8') in self.protectedSquares(swapColor(color)):
                return False
        return True
    
    def makeMoveFromNotation(self, notation):
        pc, target_sq, spec, flag = parseMove(notation)

        if flag in ['O-O', 'O-O-O']:
            if flag == 'O-O':
                ch = 'K' if self.turn == 'w' else 'k'
            elif flag == 'O-O-O':
                ch = 'Q' if self.turn == 'w' else 'q'
            if not self.canCastle(ch):
                raise ValueError(f"Illegal castle {flag}.")
            
            if ch == 'K':
                self.makeMove(4, 0, 6, 0)
                self.makeMove(7, 0, 5, 0)
            if ch == 'k':
                self.makeMove(4, 7, 6, 7)
                self.makeMove(7, 7, 5, 7)
            if ch == 'Q':
                self.makeMove(4, 0, 2, 0)
                self.makeMove(0, 0, 3, 0)
            if ch == 'q':
                self.makeMove(4, 7, 2, 7)
                self.makeMove(0, 7, 3, 7)

            return
            
        for p in self.pieces[self.turn][pc]:
            if meetSpecifier(p.x, p.y, spec) and square2xy(target_sq) in self.pieceMoves(p.x, p.y)[0]:
                xs, ys = p.x, p.y
                break
        else:
            p = list(self.pieces['b']['king'])[0]
            print(self.printPieces())
            print(self.protectedSquares('w'))
            raise ValueError(f"Illegal move: {notation}")
        xt, yt = square2xy(target_sq)
        self.makeMove(xs, ys, xt, yt)
        if flag is not None:
            self.clearSquare(xt, yt)
            flag = flag.upper() if self.turn == 'w' else flag.lower()
            pr = instantiatePiece(flag, xt, yt)
            self.grid[xt][yt] = pr
            if pr.color == 'w':
                self.pieces['w'][pr.piece_type].add(pr)
            if pr.color == 'b':
                self.pieces['b'][pr.piece_type].add(pr)
    
    def isCheck(self):
        king = list(self.pieces[self.turn]['king'])[0]
        if (king.x, king.y) in self.protectedSquares(swapColor(self.turn)):
            return True
        return False
        
    def isCheckmate(self): # Not working yet because list_all_moves does not force check dodge.
        king = list(self.pieces[self.turn]['king'])[0]
        return self.isCheck() and len(self.list_all_moves()) == 0
    
    def isStalemate(self):
        king = list(self.pieces[self.turn]['king'])[0]
        return not self.isCheck() and len(self.list_all_moves()) == 0
    
    def switchTurn(self):
        self.turn = swapColor(self.turn)
    
    def printGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                x = j
                y = self.height-i-1
                if self.grid[x][y] is None:
                    print('*', end=' ')
                else:
                    ch = piece2letter(self.grid[x][y])
                    print(ch, end=' ')
            print()
    
    def printPieces(self):
        print('===== White Pieces =====')
        for key, pcs in self.pieces['w'].items(): 
            for p in pcs:
                print(key, 'at', xy2square(p.x, p.y))
        print('===== Black Pieces =====')
        for key, pcs in self.pieces['b'].items(): 
            for p in pcs:
                print(key, 'at', xy2square(p.x, p.y))

    def list_all_moves(self):
        ret = []
        for key, pcs in self.pieces[self.turn].items(): #TODO: check not dealed with.
            for p in pcs:
                moves = self.pieceMoves(p.x, p.y)[0]
                for move in moves:
                    ret.append(piece2letter(p)+xy2square(*move))
        return ret
        
if __name__ == '__main__':
    board = Board(positionFEN="8/7p/4pkp1/R2p1p2/7P/1P3KP1/P2r4/8 b - - 0 36")

    board.printGrid()

    # print(board.legalMoves(0, 1))
    # board.makeMoveFromNotation('O-O')
    # board.switchTurn()
    # board.makeMoveFromNotation('e5')
    # board.switchTurn()
    # board.makeMoveFromNotation('Bc4')
    # board.switchTurn()
    # board.makeMoveFromNotation('Nf6')
    # board.switchTurn()
    # board.makeMoveFromNotation('Qh5')
    # board.switchTurn()
    # board.makeMoveFromNotation('b6')
    # board.switchTurn()
    # board.makeMoveFromNotation('d4')
    # board.switchTurn()
    # board.makeMoveFromNotation('Ba6')
    # board.switchTurn()
    print()
    board.printGrid()
    board.printPieces()
    print(board.list_all_moves())
    # print(board.pieceMoves(4, 0, True)[1])
    print(board.protectedSquares('b'))
    # print(board.isCheck())
    # print(board.isCheckmate())
    # print(board.isStalemate())