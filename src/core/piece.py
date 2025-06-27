def instantiatePiece(ch, x, y):
    if ch == 'K':
        piece = King('w', x, y)
    if ch == 'k':
        piece = King('b', x, y)
    if ch == 'B':
        piece = Bishop('w', x, y)
    if ch == 'b':
        piece = Bishop('b', x, y)
    if ch == 'R':
        piece = Rook('w', x, y)
    if ch == 'r':
        piece = Rook('b', x, y)
    if ch == 'P':
        piece = Pawn('w', x, y)
    if ch == 'p':
        piece = Pawn('b', x, y)
    if ch == 'Q':
        piece = Queen('w', x, y)
    if ch == 'q':
        piece = Queen('b', x, y)
    if ch == 'N':
        piece = Knight('w', x, y)
    if ch == 'n':
        piece = Knight('b', x, y)

    return piece


class Piece():
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    piece_type = None

class Pawn(Piece):
    piece_type = 'pawn'
    
class Rook(Piece):
    piece_type = 'rook' 

class Knight(Piece):
    piece_type = 'knight' 

class Bishop(Piece):
    piece_type = 'bishop' 

class Queen(Piece):
    piece_type = 'queen' 

class King(Piece):
    piece_type = 'king' 
