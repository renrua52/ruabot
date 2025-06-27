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

def parseMove(move: str):
    move = move.replace('x', '')
    if move[-1] == '+' or move[-1] == '#':
        move = move[:-1]

    if move == 'O-O':
        return None, None, None, move
    if move == 'O-O-O':
        return None, None, None, move
    
    flag = None
    if move[-2] == '=':
        flag = move[-1]
        move = move[:-2]


    if 'a' <= move[0] <= 'h':
        move = 'P'+move

    # Now move is in the format: piece + (specifier) + target square

    p = move[0]
    if p == 'P':
        piece = 'pawn'
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

    specifier = move[:-2]
    target_square = move[-2:]

    return piece, target_square, specifier, flag

def meetSpecifier(x, y, spec):
    if spec == "":
        return True
    if len(spec) == 1:
        if 'a' <= spec <= 'h':
            x_spec = ord(spec)-ord('a')
            return x == x_spec
        else:
            y_spec = ord(spec)-ord('1')
            return y == y_spec
    if len(spec) == 2:
        return (x, y) == square2xy(spec)
    raise ValueError("Illegal move format: wrong specifier.")
    
    