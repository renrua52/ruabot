from board import Board
import copy

class Game:
    def __init__(self, gamePGN = None):
        self.board = Board()
    
if __name__ == '__main__':
    demo_game = """1. d4 d5 2. e3 Bf5 3. Bd3 Bg6 4. Ne2 e6 5. O-O c5 6. c3 Nc6 7. Ng3 Bxd3 8. Qxd3 g6 9. Qb5 a6 10. Qxb7 Qc8 11. Qxc8+ Rxc8 12. e4 Bg7 13. e5 cxd4 14. cxd4 Nxd4 15. Bf4 Ne7 16. Nc3 Nef5 17. Nxf5 Nxf5 18. Rac1 O-O 19. Na4 Ne7 20. Nb6 Rxc1 21. Rxc1 Rb8 22. Be3 Nf5 23. Bc5 Bxe5 24. f4 Bxf4 25. Rb1 Be3+ 26. Bxe3 Nxe3 27. Kf2 Rxb6 28. Kxe3 Rb4 29. b3 f5 30. g3 Kf7 31. Rc1 Kf6 32. Rc6 Re4+ 33. Kf3 a5 34. Ra6 Rd4 35. Rxa5 Rd2 36. h4 Ke5 37. b4 Rb2 38. b5 Kd4 39. Ra4+ Kc5 40. Ra7 Rxb5 41. Rxh7 Ra5 42. Rh6 Ra3+ 43. Kf4 Ra4+ 44. Kg5 Rg4+ 45. Kf6 Rxg3 46. Kxe6 d4 47. h5 d3 48. hxg6 d2 49. Rh1 Rxg6+ 50. Kxf5 Rd6 51. Rd1 Kc4 52. Ke4 Kc3 53. Kf4 Kc2 54. Ra1 d1=Q 55. Rxd1 Rxd1 56. a4 Ra1 57. Ke3 Rxa4"""
    game = demo_game.split()

    b = Board()

    for i in range(57):
        move_num = int(game[i*3][:-1])
        print("Move", move_num)

        b.makeMoveFromNotation(game[i*3+1])
        b.switchTurn()
        b.printGrid()
        print()
        b.makeMoveFromNotation(game[i*3+2])
        b.switchTurn()
        b.printGrid()
        print()
