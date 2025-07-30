class Board:
    def __init__(self, width: int = 8, height: int = 8, configStr: str = "0000000000000000000000000001200000021000000000000000000000000000"):
        pass

    def setupFromConfigStr(self, configStr: str):
        """
        由表示当前局面的长度为 width * height 的字符串重置局面.
        0 表示空格, 1 表示白子, 2 表示黑子.
        """
        pass

    def setupFromConfig(self, config: list[list[int]]):
        """
        由表示当前局面的 width * height 二维数组重置局面.
        0 表示空格, 1 表示白子, 2 表示黑子.
        """
        pass

    def getConfigStr(self) -> str:
        """
        返回表示当前局面的长度为 width * height 的字符串.
        0 表示空格, 1 表示白子, 2 表示黑子.
        """
        pass

    def getConfig(self) -> list[list[int]]:
        """
        返回表示当前局面的 width * height 二维数组.
        0 表示空格, 1 表示白子, 2 表示黑子.
        """
        pass
    
    def getPiece(self, x: int, y: int) -> int:
        """
        坐标 1-indexed.
        0 表示空格, 1 表示白子, 2 表示黑子.
        """
        pass

    def makeMove(self, x: int, y: int):
        """
        坐标 1-indexed.
        """
        pass
    
    def makeEmptyMove(self):
        pass
    
    def getAllLegalMoves(self) -> list[tuple[int, int]]:
        """
        坐标 1-indexed.
        """
        pass

    def getScores(self) -> tuple[int, int]:
        """
        返回 (白方棋子数量, 黑方棋子数量).
        """
        pass

    def getWinner(self) -> int:
        """
        游戏未结束返回 -1, 平局返回 0, 白方胜返回 1, 黑方胜返回 2.
        """
        pass