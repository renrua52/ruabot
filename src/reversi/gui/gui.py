import pygame
from reversi.game.utils import getDefaultConfig
from reversi.game.player import HumanPlayer
from reversi.core.board import Board
import sys

class ReversiGUI:
    def __init__(self, config, p1, p2):
        self.config = config
        self.board = Board(config)
        self.players = {
            1: p1,
            2: p2
        }

        pygame.init()
        self.CELL_SIZE = 100
        self.SCREEN_WIDTH = self.CELL_SIZE * self.config["width"]
        self.SCREEN_HEIGHT = self.CELL_SIZE * self.config["height"]
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.BLUE = (0, 0, 255)

        self.WIN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Reversi")

    def draw_grid(self):
        for x in range(0, self.SCREEN_WIDTH, self.CELL_SIZE):
            pygame.draw.line(self.WIN, self.GRAY, (x, 0), (x, self.SCREEN_HEIGHT), 1)
        for y in range(0, self.SCREEN_HEIGHT, self.CELL_SIZE):
            pygame.draw.line(self.WIN, self.GRAY, (0, y), (self.SCREEN_WIDTH, y), 1)

    def draw_pieces(self):
        for row in range(self.config["height"]):
            for col in range(self.config["width"]):
                cell_state = self.board.grid[row][col]
                if cell_state == 1:
                    pygame.draw.circle(self.WIN, self.BLACK, (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2 - 10)
                elif cell_state == 2:
                    pygame.draw.circle(self.WIN, self.GRAY, (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2 - 10)

    def get_board_position(self, x, y):
        return y // self.CELL_SIZE, x // self.CELL_SIZE

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self.WIN.fill(self.WHITE)
            self.draw_grid()
            self.draw_pieces()

            if len(self.board.getAllLegalMoves()) == 0:
                self.board.makeEmptyMove()
            current_player = self.players[self.board.getTurn()]
            if isinstance(current_player, HumanPlayer):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        row, col = self.get_board_position(x, y)
                        self.board.makeMove(row, col)
            else:
                move = current_player.generateMove(self.board)
                self.board.makeMove(move[0], move[1])

            pygame.display.flip()
            clock.tick(10)

        pygame.quit()
