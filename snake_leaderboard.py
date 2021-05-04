import pygame
import pickle
from constantes import c
print(c.test)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

largeur = c.largeur
hauteur = c.hauteur

win = pygame.display.set_mode((largeur,hauteur))
background = pygame.Surface((largeur,hauteur))
pygame.display.set_caption("Chum Games | Snake Leaderboard")

run = True
#h = open("score.txt", "r")
#best_score = (h.read())
dico = load_obj("score.txt")
font = pygame.font.SysFont('comicsans', 60)
text = font.render(str(dico), 1, c.white)
yourbest_w, yourbest_h = font.size(str(dico))
win.blit(text, ((largeur-yourbest_w)/2, (hauteur-yourbest_h)/2))

while run:
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            exec(open('menu.py').read())
            pygame.quit()
            quit()
