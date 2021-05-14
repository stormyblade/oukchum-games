from game import Game
from board import Board
import pygame

pygame.display.set_caption("Minesweeper")
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon)

size = (5, 5)
prob = 0.01
board = Board(size, prob)
screenSize = (740, 740)
game = Game(board, screenSize)
game.run()