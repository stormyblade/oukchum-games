import pygame
import math
from random import *
import pygame
import pickle
import pygame_textinput
from constantes import c

textinput = pygame_textinput.TextInput()
inputflag = False

size = 800

# run game
pygame.init()

# window
screen = pygame.display.set_mode((1000, 600))
background = pygame.image.load("./chumhunt/castlebackground.jpg")

# caption and icon
pygame.display.set_caption("Knight Hunt")
icon = pygame.image.load("./chumhunt/knighticon.png")
pygame.display.set_icon(icon)

# Countdown Timer
clock = pygame.time.Clock()
timer = 60
dt = 0

# Score
score_value = 0
scoreX = 10
scoreY = 10
font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over
font2 = pygame.font.Font('freesansbold.ttf', 64)
# Life
life= 10

# player
playerimg = pygame.image.load("./chumhunt/crossbow.png")
playerX = randint(0, 936)
playerY = 500
playerchgX = 0
playerchgY = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemychgX = []
enemychgY = []
num_enemy = 10

for i in range(num_enemy):
    enemyimg.append(pygame.image.load("./chumhunt/enemyknight.png"))
    enemyX.append(randint(0, 936))
    enemyY.append(randint(0, 150))
    enemychgX.append((0.5 + random() * (0.9 - 0.5)))
    enemychgY.append(50)

# arrow
arrowimg = pygame.image.load("./chumhunt/arrow.png")
arrowX = 0
arrowY = 500
arrowchgX = 0
arrowchgY = 3.3
arrowState = "ready"  # arrow is invisible , fire is visible

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameover_text():
    gameover = font2.render("GAME OVER", True, (255, 0, 0))
    screen.blit(gameover, (300, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))
    return player


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))
    return enemy


def fire_arrow(x, y):
    global arrowState
    arrowState = "fire"
    screen.blit(arrowimg, (x, y))
    # if event.type == pygame.KEYDOWN:
    # if event.key == pygame.K_SPACE:


def collisionarrow(enemyX, enemyY, arrowX, arrowY):
    distance = math.sqrt((math.pow(enemyX - arrowX, 2)) + (math.pow(enemyY - arrowY, 2)))
    if distance < 27:
        return True
    else:
        return False


def collisionplayer(enemyX, enemyY, playerX, playerY):
    distance2 = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if distance2 < 40:
        return True
    else:
        return False


# Game loop
running = True
inputflag = False
dico = (load_obj("./chumhunt/knighthunt_score.txt"))
while running:

    screen.fill((132, 56, 221))
    screen.blit(background, (0, 0))

    timer -= dt
    if timer <= 0:
        timer = 0
    dt = clock.tick(1000) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

            # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerchgX = -2
            elif event.key == pygame.K_RIGHT:
                playerchgX = 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerchgX = 0

                # if keystroke is pressed check whether its up or down
        #        if event.type == pygame.KEYDOWN:
        #            if event.key == pygame.K_UP:
        #                playerchgY = -0.3
        #            elif event.key == pygame.K_DOWN:
        #                playerchgY = 0.3
        #       if event.type==pygame.KEYUP:
        #            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #                playerchgY = 0

        # if keystroke is pressed put arrow in fire state
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if arrowState == "ready":
                    # get the current x of the bow
                    arrowX = playerX
                    fire_arrow(arrowX, arrowY)

    # location and boundaries for player
    playerX += playerchgX
    if playerX >= 936:
        playerX = 936
    elif playerX <= 0:
        playerX = 0
    # location and boundaries for enemy
    for i in range(num_enemy):
        collision2 = collisionplayer(enemyX[i], enemyY[i], playerX, playerY)
        if timer == 0:
            for j in range(num_enemy):
                enemyY[j] = 2000
            scoreX = 430
            scoreY = 310
            gameover_text()
            running = False

        if life == 0 or collision2:
            for j in range(num_enemy):
                enemyY[j] = 2000
            scoreX = 430
            scoreY = 310
            gameover_text()
            timer = 0
            running = False

        enemyX[i] += enemychgX[i]
        if enemyX[i] >= 936:
            enemychgX[i] = -(0.5 + random() * (0.9 - 0.5))
            enemyY[i] += enemychgY[i]
        elif enemyX[i] <= 0:
            enemychgX[i] = (0.5 + random() * (0.9 - 0.5))
            enemyY[i] += enemychgY[i]
        # collision
        collision1 = collisionarrow(enemyX[i], enemyY[i], arrowX, arrowY)
        if collision1:
            arrowY = 480
            arrowState = "ready"
            score_value += 1

            enemyX[i] = randint(0, 936)
            enemyY[i] = randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

    # arrow movement
    if arrowY <= -32 and life > 0:
        arrowY = 500
        arrowState = "ready"
        life -= 1
    if arrowState == "fire":
        fire_arrow(arrowX, arrowY)
        arrowY -= arrowchgY


    rest = font.render("Remaining lives: " + str(life), True, (255, 255, 255))
    txt = font.render("Time left: " + str(round(timer)), True, (255, 255, 255))
    screen.blit(txt, (800, 10))
    enemy(enemyX[i], enemyY[i], i)
    player(playerX, playerY)
    show_score(scoreX, scoreY)
    screen.blit(rest, (685, 560))
    pygame.display.update()

print("test")
inputflag = True
while inputflag:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Feed it with events every frame
    if textinput.update(events):
        name = textinput.get_text()
        print(dico)
        if name == "Sheesh":
            print("SHEEESH")
            pygame.mixer.music.load("assets/sheesh.wav")
            pygame.mixer.music.play(0)
        elif name == "Dior":
            print("Woo back baby")
            pygame.mixer.music.load("assets/dior.mp3")
            pygame.mixer.music.play(0)
        elif name != "":
            print("Text Output : ", name)
            screen.fill((0, 0, 0))
            pygame.display.update()
            try:
                if dico[name] < score_value:
                    dico[name] = score_value
            except:
                dico[name] = score_value
            save_obj(dico, "./chumhunt/knighthunt_score.txt")
            print(load_obj("./chumhunt/knighthunt_score.txt"))
            inputflag = False
    # Blit its surface onto the screen
    pygame.draw.rect(screen, c.white, (350,400,300,50))
    screen.blit(textinput.get_surface(), (360,410))

    pygame.display.update()
    clock.tick(30)
pygame.quit()
