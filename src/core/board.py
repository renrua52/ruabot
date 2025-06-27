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

            self.turn = elements[1]
            self.castle = elements[2]
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
                    if isEmpty(xt, yt) or not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
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
                    if isEmpty(xt, yt) or not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
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
                    if isEmpty(xt, yt) or not sameColor(xs, ys, xt, yt):
                        viable.append((xt, yt))
                        protecting.append((xt, yt))
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
                if inRange(xt, yt) and not isEmpty(xt, yt):
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
    
    def makeMoveFromNotation(self, notation):
        pc, target_sq, spec, castle = parseMove(notation)

        if castle is not None:
            raise NotImplementedError
        
        for p in self.pieces[self.turn][pc]:
            if meetSpecifier(p.x, p.y, spec) and square2xy(target_sq) in self.pieceMoves(p.x, p.y)[0]:
                xs, ys = p.x, p.y
                break
        else:
            raise ValueError("Illegal move.")
        
        xt, yt = square2xy(target_sq)
        self.makeMove(xs, ys, xt, yt)
    
    def isCheck(self):
        king = list(self.pieces[self.turn]['king'])[0]
        if (king.x, king.y) in self.protectedSquares(swapColor(self.turn)):
            return True
        return False
        
    def isCheckmate(self):
        king = list(self.pieces[self.turn]['king'])[0]
        return self.isCheck() and len(self.pieceMoves(king.x, king.y)[0]) == 0
    
    def isStalemate(self):
        king = list(self.pieces[self.turn]['king'])[0]
        return not self.isCheck() and len(self.pieceMoves(king.x, king.y)[0]) == 0

    
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

    def list_all_moves(self):
        ret = []
        for key, pcs in self.pieces[self.turn].items(): #TODO: check not dealed with.
            for p in pcs:
                moves = self.pieceMoves(p.x, p.y)[0]
                for move in moves:
                    ret.append(piece2letter(p)+xy2square(*move))
        return ret
        
if __name__ == '__main__':
    board = Board(positionFEN="2k1r3/3rbpp1/Q1p2n1p/2Pp4/8/1P2P2P/PB3PP1/R1R3K1 b - - 0 21")

    # print(board.legalMoves(0, 1))
    # board.makeMoveFromNotation('e4')
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

    board.printGrid()
    print(board.list_all_moves())
    # print(board.pieceMoves(4, 0, True)[1])
    print(board.protectedSquares('w'))
    print(board.isCheck())
    print(board.isCheckmate())
    print(board.isStalemate())