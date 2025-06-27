from board import Board
import copy
import re

class Game:
    def __init__(self, startingFEN=None):
        self.board = Board(positionFEN=startingFEN)
        self.game_history = []
        self.metadata = {} #TODO

    def executeMove(self, notation):
        self.board.makeMoveFromNotation(notation)
        self.board.switchTurn()
    
    def loadPGN(self, gamePGN):
        gamePGN = re.sub(r'\[.*?\]', '', gamePGN)
        moves = gamePGN.split()

        if moves[-1] in ['1-0', '0-1', '1/2-1/2']:
            self.result = moves[-1]
            moves = moves[:-1]

        move_idx = 0
        for s in moves:
            # print(s)
            if s[-1] == '.':
                move_idx += 1
            else:
                self.executeMove(s)
                b = copy.deepcopy(self.board)
                self.game_history.append(b)
    
    def printHistory(self):
        i = 2
        for b in self.game_history:
            print(f'Move {i//2},', 'White' if i%2==0 else 'Black')
            i += 1
            b.printGrid()
            print()
    
if __name__ == '__main__':
    demo_game = """[Event "casual bullet game"]
[Site "https://lichess.org/iaZNeC9F"]
[Date "2025.06.22"]
[White "Li_Ne_x"]
[Black "Effidi98"]
[Result "1-0"]
[GameId "iaZNeC9F"]
[UTCDate "2025.06.22"]
[UTCTime "18:12:16"]
[WhiteElo "1553"]
[BlackElo "1603"]
[Variant "Standard"]
[TimeControl "30+0"]
[ECO "A04"]
[Opening "Zukertort Opening: The Walrus"]
[Termination "Time forfeit"]

1. Nf3 e5 2. Nxe5 Nc6 3. Nxc6 dxc6 4. b3 Nf6 5. Bb2 Be7 6. g3 O-O 7. Bg2 Qd6 8. O-O Be6 9. f4 Rfd8 10. Be5 Qd5 11. Bxd5 Bxd5 12. Bxf6 Bxf6 13. c4 Bxa1 14. cxd5 cxd5 15. Nc3 Bxc3 16. dxc3 d4 17. cxd4 Rd7 18. e3 Rad8 19. Qc2 c5 20. Qxc5 b6 21. Qc6 Rd6 22. Qc7 R6d7 23. Qc3 f6 24. Qd3 g5 25. Rc1 gxf4 26. gxf4 Rg7+ 27. Kf2 Re8 28. Rg1 Kh8 29. Rxg7 Kxg7 30. Qf5 Kf7 31. Qd7+ Re7 32. Qxe7+ Kxe7 33. Kf3 Kd6 34. Ke4 f5+ 35. Kxf5 Kc6 36. Kf6 Kb5 37. Kg7 Kb4 38. Kxh7 Kc3 39. Kg6 Kd2 40. h4 Kxe3 41. h5 Ke2 42. h6 Kd2 43. h7 Kc2 44. h8=Q Kb2 45. Qd8 Kc2 46. Qb8 Kb2 47. Qxa7 Kc3 48. Qxb6 Kc2 49. Qc6+ Kb2 50. Qb5 Kc2 51. Qf1 Kd2 52. b4 Ke3 53. Qg2 Kxd4 54. f5 Kc3 55. Qf3+ Kxb4 56. f6 1-0



"""
    g = Game()
    g.loadPGN(demo_game)
    g.printHistory()