import pygame
from constantes import c
pygame.init()

largeur = c.largeur
hauteur = c.hauteur

win = pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("Chum Games")
win.fill(c.background)

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
    win.fill(c.background)
    greenButton.draw(win, c.green)
    blueButton.draw(win, c.blue)
    redButton.draw(win, c.red)
    greenButton2.draw(win, c.green)
    blueButton2.draw(win, c.blue)
    redButton2.draw(win, c.red)

run = True

boutonlargeur = 250
boutonhauteur = 100
gap = boutonhauteur/2
marginx = largeur/2-(boutonlargeur+gap+boutonhauteur)/2
marginy = hauteur/2-boutonhauteur/2-gap-boutonhauteur

greenButton = button(c.green, marginx, marginy, boutonlargeur, boutonhauteur, "Snake")
greenButton2 = button(c.green, largeur-marginx-boutonhauteur, marginy, boutonhauteur, boutonhauteur, "#")
blueButton = button(c.blue, marginx, hauteur/2-boutonhauteur/2, boutonlargeur, boutonhauteur, "2")
blueButton2 = button(c.blue, largeur-marginx-boutonhauteur, hauteur/2-boutonhauteur/2, boutonhauteur, boutonhauteur, "#")
redButton = button(c.red, marginx, hauteur-marginy-boutonhauteur, boutonlargeur, boutonhauteur, "3")
redButton2 = button(c.red, largeur-marginx-boutonhauteur, hauteur-marginy-boutonhauteur, boutonhauteur, boutonhauteur, "#")


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
            if greenButton2.isOver(pos):
                exec(open('leaderboard.py').read())

        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = c.lightgreen
            elif greenButton2.isOver(pos):
                greenButton2.color = c.lightgreen
            elif blueButton.isOver(pos):
                blueButton.color = c.lightblue
            elif blueButton2.isOver(pos):
                blueButton2.color = c.lightblue
            elif redButton.isOver(pos):
                redButton.color = c.lightred
            elif redButton2.isOver(pos):
                redButton2.color = c.lightred
            else:
                greenButton.color = c.green
                greenButton2.color = c.green
                blueButton.color = c.blue
                blueButton2.color = c.blue
                redButton.color = c.red
                redButton2.color = c.red