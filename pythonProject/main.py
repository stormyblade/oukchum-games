from game import Game
from board import Board

import pygame


pygame.display.set_caption("Démineur ")
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon)

size = (9, 9)
prob = 0.1
board = Board(size, prob)
screenSize = (800, 800)
game = Game(board, screenSize)
game.run()