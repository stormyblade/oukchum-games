import math
import random
import os
import pygame
pygame.init()

largeur = 500
hauteur = 500

white = (255, 255, 0)
gray = (50, 50, 50)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 50)
lightgreen = (30, 255, 85)
blue = (0, 100, 200)
lightblue = (30, 170, 255)
cyan = (0,0,0)

win = pygame.display.set_mode((largeur,hauteur))
win.fill((255,255,255))

class button():
    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
           pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

def redrawWindow():
    win.fill((255,255,255))
    greenButton.draw(win, green)
    blueButton.draw(win, blue)

run = True

boutonlargeur = 250
boutonhauteur = 100

greenButton = button(green, largeur/2-boutonlargeur/2, 100, boutonlargeur, boutonhauteur, "Snake")
blueButton = button(blue, largeur/2-boutonlargeur/2, 300, boutonlargeur, boutonhauteur, "Ouk")
while run:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos):
                print("Clicked the button")
                exec(open('snakev3.py').read())
            if blueButton.isOver(pos):
                print("Cliqué sur le bouton")

        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = lightgreen
            elif blueButton.isOver(pos):
                blueButton.color = lightblue
            else:
                greenButton.color = green
                blueButton.color = blue