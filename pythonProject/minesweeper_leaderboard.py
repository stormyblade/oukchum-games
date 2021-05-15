import pygame
import pickle
from constantes import c
print(c.test)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

largeur = c.largeur
size = c.moyenne
hauteur = c.hauteur

win = pygame.display.set_mode((largeur,hauteur))
background = pygame.Surface((largeur,hauteur))
pygame.display.set_caption("Chum Games | Minesweeper Leaderboard")

run = True

font = pygame.font.SysFont('comicsans', int(round(3/25*size)))

dico = load_obj("./pythonProject/minesweeper_score.txt")    #Importe le dico
print(dico)                     #Affiche le dico avant de le trier
sorted_dict = {}                #Trie le dico
result = []                     #Initialise une liste result
sorted_keys = sorted(dico, key=dico.get, reverse=False)  #Trie les clés

for w in sorted_keys:           #Réarrange le dico selon les clés triées
    sorted_dict[w] = dico[w]

print(sorted_dict)

text_w, text_h = font.size("Test")
margin = 1/10*size              #Marge juste pour un meilleur rendu visuel

for a in range(0,5):
    try:
        result.append(str(list(sorted_dict.keys())[a]) + " : " + str(list(sorted_dict.values())[a]))    #Ajoute les 5 premiers à la liste
        result_text = font.render(str(a+1)+". "+result[a]+"s", True, c.white)                                             #Imprime à chaque fois l'élément de la liste
        win.blit(result_text, ((margin,(3/31*size)*a+69/310*size)))
        pygame.display.update()
    except:
        None

lb_title = font.render("Minesweeper Leaderboard", True, c.red)
win.blit(lb_title, ((margin, margin)))
pygame.display.update()

while run:
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            exec(open('menu.py').read())
            pygame.quit()
            quit()
