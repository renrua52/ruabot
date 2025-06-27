def square2xy(square):
    x = ord(square[0])-ord('a')
    y = int(square[1])-1
    return x, y
def xy2square(x, y):
    file = chr(ord('a')+x)
    rank = str(y+1)
    return file+rank
swapColor = lambda color: 'w' if color == 'b' else 'b'

name2letter = {
    'king': 'k',
    'bishop': 'b',
    'knight': 'n',
    'rook': 'r',
    'pawn': 'p',
    'queen': 'q'
}

def piece2letter(p):
    ch = name2letter[p.piece_type]
    if p.color == 'w':
        ch = ch.upper()
    return ch

def parseMove(move):
    if move == 'O-O':
        return None, None, None, 'short'
    if move == 'O-O-O':
        return None, None, None, 'long'

    if 'a' <= move[0] <= 'e':
        piece = 'pawn'
    else:
        p = move[0]
        if p == 'K':
            piece = 'king'
        if p == 'N':
            piece = 'knight'
        if p == 'Q':
            piece = 'queen'
        if p == 'R':
            piece = 'rook'
        if p == 'B':
            piece = 'bishop'

        move = move[1:]

    if move[-1] == '+' or move[-1] == '#':
        move = move[:-1]

    specifier = move[:-2]
    target_square = move[-2:]

    return piece, target_square, specifier, None

def meetSpecifier(x, y, spec):
    if spec == "":
        return True
    
    if 'a' <= spec <= 'h':
        x_spec = ord(spec)-ord('a')
        return x == x_spec
    else:
        y_spec = ord(spec)-ord('1')
        return y == y_spec
    
if __name__ == '__main__':
    x, y = square2xy("g5")
    print(meetSpecifier(x, y, "5"))
    