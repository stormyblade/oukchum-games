import pygame
from constantes import c
print(c.test)

largeur = c.largeur
hauteur = c.hauteur

win = pygame.display.set_mode((largeur,hauteur))
background = pygame.Surface((largeur,hauteur))
pygame.display.set_caption("Chum Games | Snake Leaderboard")

run = True
h = open("score.txt", "r")
best_score = (h.read())
font = pygame.font.SysFont('comicsans', 60)
text = font.render(best_score, 1, c.white)
win.blit(text,(300,200))

while run:
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            exec(open('menu.py').read())
            pygame.quit()
            quit()