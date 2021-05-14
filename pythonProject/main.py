from pythonProject.game import Game
from pythonProject.board import Board

import pygame


pygame.display.set_caption("Minesweeper")
icon = pygame.image.load('pythonProject/images/icon.png')
pygame.display.set_icon(icon)

size = (9, 9)
prob = 0.01
board = Board(size, prob)
screenSize = (740, 740)
game = Game(board, screenSize)
game.run()