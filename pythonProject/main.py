from pythonProject.game import Game
from pythonProject.board import Board
from constantes import c
import pygame

pygame.display.set_caption("Minesweeper")                   #Title
icon = pygame.image.load('pythonProject/images/icon.png')   #Icon
pygame.display.set_icon(icon)

size = (10, 10)
prob = 0.1
board = Board(size, prob)
screenSize = (c.largeur, c.largeur)
game = Game(board, screenSize)

game.run()