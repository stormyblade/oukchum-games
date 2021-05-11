import pygame
from random import *


#run game
pygame.init()

#window
screen= pygame.display.set_mode((1000,600))

#caption and icon
pygame.display.set_caption("duck")
icon= pygame.image.load("monkey.png")
pygame.display.set_icon(icon)

 
#player
playerimg= pygame.image.load("duck.png")
playerX = randint (0,1000)
playerY = 500
playerchgX = 0
playerchgY = 0

#enemy
enemyimg= pygame.image.load("enemyknight.png")
enemyX = randint(0,936)
enemyY = randint (0,150)
enemychgX = 0.3
enemychgY = 25


def player(x,y):
    screen.blit(playerimg, (x, y))
    return player


def enemy(x,y):
    screen.blit(enemyimg, (x, y))
    return enemy


# Game loop
running= True
while running:
   
    screen.fill((132,56 ,221 ))
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

     #if keystroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerchgX = -0.3
            if event.key == pygame.K_RIGHT:
                playerchgX = 0.3

        if event.type==pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerchgX = 0                

         # if keystroke is pressed check wheter its up or down              
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerchgY = -0.3
            if event.key == pygame.K_DOWN:
                playerchgY = 0.3
        if event.type==pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerchgY = 0



    #location and boundaries for player    
    playerX += playerchgX
    if playerX >= 936:
        playerX= 936
    elif playerX <= 0:
        playerX= 0

    playerY += playerchgY #to move it up and down    
    player(playerX,playerY)
    
    #location and boundaries for enemy
    enemyX += enemychgX
    if enemyX >= 936:
        enemychgX= -0.3
        enemyY+= enemychgY
    elif enemyX <= 0:
        enemychgX= 0.3
        enemyY+= enemychgY

    enemy(enemyX,enemyY)



    pygame.display.update()
