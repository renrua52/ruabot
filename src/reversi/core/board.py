class Board:
    def __init__(self, configstr: str = "8/8/1/0000000000000000000000000001200000021000000000000000000000000000"):
        pass

    def getSize(self) -> tuple[int, int]:
        pass

    def getTurn(self) -> int:
        pass

    def getGrid(self) -> list[list[int]]:
        pass

    def getPiece(self, x: int, y: int) -> int:
        pass

    def getConfigstr(self) -> str:
        pass

    def makeMove(self, x: int, y: int):
        pass
    
    def makeEmptyMove(self):
        pass
    
    def getAllLegalMoves(self) -> list[tuple[int, int]]:
        pass

    def getScores(self) -> tuple[int, int]:
        pass

    def getResult(self) -> int:
        pass
