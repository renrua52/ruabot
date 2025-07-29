import sys
import os

from chess.game.game import Game


gamePGN = """[Event "casual bullet game"]
[Site "https://lichess.org/DWKFGKwu"]
[Date "2025.06.22"]
[White "Li_Ne_x"]
[Black "radiations"]
[Result "0-1"]
[GameId "DWKFGKwu"]
[UTCDate "2025.06.22"]
[UTCTime "18:30:36"]
[WhiteElo "1553"]
[BlackElo "1534"]
[Variant "Standard"]
[TimeControl "120+0"]
[ECO "A06"]
[Opening "Nimzo-Larsen Attack: Classical Variation"]
[Termination "Normal"]

1. Nf3 d5 2. b3 Nc6 3. Bb2 f6 4. e3 e5 5. c4 e4 6. Nd4 Nxd4 7. Bxd4 c6 8. Bb2 Bb4 9. a3 Bc5 10. b4 Bb6 11. c5 Bc7 12. Nc3 Be5 13. Be2 d4 14. exd4 Bxd4 15. Qc2 Be6 16. Qxe4 Bxc3 17. Bxc3 Qe7 18. Bg4 Bxg4 19. Qxe7+ Kxe7 20. h3 Be6 21. O-O Kd7 22. Rfe1 Ne7 23. Re3 Nd5 24. Rd3 Kc7 25. Bb2 Nf4 26. Re3 Bd5 27. Re7+ Kd8 28. Rae1 Nd3 0-1"""

if __name__ == '__main__':
    g = Game()
    g.loadPGN(gamePGN)
    # g.printHistory()
    g.checkoutMove(28, 'b')
    g.printCurrentPosition()
    print(g.metadata)