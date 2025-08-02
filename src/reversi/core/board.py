class Board:
    def __init__(self, config: dict, configstr: str = None):
        default_config = {
            (4, 4): "0000021001200000 0 0",
            (6, 6): "000000000000002100001200000000000000 0 0",
            (8, 8): "0000000000000000000000000002100000012000000000000000000000000000 0 0"
        }
        if configstr is None:
            board_shape = (config["height"], config["width"])
            assert board_shape in default_config
            configstr = default_config[board_shape]

        splitted = configstr.split()
        if len(splitted) != 3:
            raise Exception("Invalid configstr.")
        try:
            self.height = config["height"]
            self.width = config["width"]
            self.steps = int(splitted[1])
            self.emptyMoves = int(splitted[2])
        except ValueError:
            raise Exception("Invalid configstr.")
        if not (1 <= self.height <= 100 and 1 <= self.width <= 100):
            raise Exception("Invalid board size.")
        if self.steps < 0 or not (0 <= self.emptyMoves <= 2) or len(splitted[0]) != self.height * self.width:
            raise Exception("Invalid configstr.")
        self.bScore = 0
        self.wScore = 0
        self.grid = [[0] * self.width for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                c = splitted[0][i * self.width + j]
                if c == "1":
                    self.bScore += 1
                    self.grid[i][j] = 1
                elif c == "2":
                    self.wScore += 1
                    self.grid[i][j] = 2
                elif c != "0":
                    raise Exception("Invalid configstr.")

    def getSize(self) -> tuple[int, int]:
        return (self.height, self.width)
    
    def getSteps(self) -> int:
        return self.steps

    def getTurn(self) -> int:
        return 1 if self.steps % 2 == 0 else 2

    def getGrid(self) -> list[list[int]]:
        return self.grid
    
    def validCoordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def safelyGetPiece(self, x: int, y: int) -> int:
        if not self.validCoordinates(x, y):
            return -1
        return self.grid[x][y]
    
    def getPiece(self, x: int, y: int) -> int:
        if not self.validCoordinates(x, y):
            raise Exception("Invalid coordinates.")
        return self.grid[x][y]

    def changePiece(self, x: int, y: int, c: int):
        if not self.validCoordinates(x, y):
            raise Exception("Invalid coordinates.")
        if not (0 <= c <= 2):
            raise Exception("Invalid piece.")
        if self.grid[x][y] == 1:
            self.bScore -= 1
        elif self.grid[x][y] == 2:
            self.wScore -= 1
        self.grid[x][y] = c
        if c == 1:
            self.bScore += 1
        elif c == 2:
            self.wScore += 1

    def getConfigstr(self) -> str:
        ret = str(self.height) + "/" + str(self.width) + "/" + str(self.steps) + "/" + str(self.emptyMoves) + "/"
        for i in range(self.height):
            for j in range(self.width):
                ret += str(self.grid[i][j])
        return ret

    def makeMove(self, x: int, y: int):
        # if x == -1 and y == -1:
        #     self.makeEmptyMove()
        #     return
        if self.getResult() >= 0:
            raise Exception("Game is over.")
        if not self.validCoordinates(x, y):
            raise Exception("Invalid coordinates.")
        if self.grid[x][y] != 0:
            raise Exception("Invalid move.")
        turn = self.getTurn()
        valid = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.safelyGetPiece(nx, ny) != 3 - turn:
                    continue
                while self.safelyGetPiece(nx, ny) == 3 - turn:
                    nx += dx
                    ny += dy
                if self.safelyGetPiece(nx, ny) != turn:
                    continue
                valid += 1
                while nx != x or ny != y:
                    self.changePiece(nx, ny, turn)
                    nx -= dx
                    ny -= dy
        if valid == 0:
            raise Exception("Invalid move.")
        self.changePiece(x, y, turn)
        self.steps += 1
        self.emptyMoves = 0
    
    def makeEmptyMove(self):
        if self.getResult() >= 0:
            raise Exception("Game is over.")
        self.steps += 1
        self.emptyMoves += 1
    
    def getAllLegalMoves(self) -> list[tuple[int, int]]:
        if self.getResult() >= 0:
            raise Exception("Game is over.")
        turn = self.getTurn()
        ret = []
        for x in range(self.height):
            for y in range(self.width):
                if self.grid[x][y] != 0:
                    continue
                valid = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if self.safelyGetPiece(nx, ny) != 3 - turn:
                            continue
                        while self.safelyGetPiece(nx, ny) == 3 - turn:
                            nx += dx
                            ny += dy
                        if self.safelyGetPiece(nx, ny) != turn:
                            continue
                        valid = 1
                        break
                    if valid == 1:
                        break
                if valid == 1:
                    ret.append((x, y))
        return ret

    def getScores(self) -> tuple[int, int]:
        return (self.bScore, self.wScore)

    def getResult(self) -> int:
        if self.emptyMoves < 2:
            return -1
        b, w = self.getScores()
        if b == w:
            return 0
        if b > w:
            return 1
        return 2
    
    def printGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.grid[i][j], end='')
                pass
            print()
