import random
import pygame
import pygame_textinput
import tkinter as tk
from tkinter import messagebox
from constantes import c

size = c.largeur

#Colors
white = c.white
gray = c.gray
lightgray = c.lightgray
black = c.black
red = c.red
green = c.green

#Text
textinput = pygame_textinput.TextInput()
inputflag = False

font = pygame.font.SysFont('comicsans', int(round(3/25*size)))
fontbig = pygame.font.SysFont('comicsans', int(round(4/25*size)))
fontsmall = pygame.font.SysFont('comicsans', int(round(2/25*size)))

gameover = c.gameoverstring
gameover_w, gameover_h = fontbig.size(gameover)
gameover_text = fontbig.render(gameover, True, white)
entername = c.enternamestring
entername_w, entername_h = fontsmall.size(entername)
entername_text = fontsmall.render(entername, True, white)
yourscore = c.yourscorestring
yourbest = c.yourbeststring

class cube(object):
    rows = 20
    w = size
    def __init__(self,start,dirnx=1,dirny=0,color=red):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self,dirnx,dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            center = dis//2
            radius = 3
            circleMiddle = (i*dis+center-radius,j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2,j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #rappelle la position où on s'est arrêté au dico

                if keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_UP] and self.dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_DOWN] and self.dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
        for i, c in enumerate(self.body):   #i index, c cube object
            p = c.pos[:]                    #grab position and see if it's in the turn list
            if p in self.turns:
                turn = self.turns[p]        
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)       #remove the last one from the list

            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)   #if it's the first cube, draw eyes
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (gray), (x,0), (x,w))
        pygame.draw.line(surface, (gray), (0,y), (w,y))

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack, speed
    speed = 10
    try:
        h = open("score.txt", "r")
        int(h.read())
    except:
        g = open("score.txt", "w")
        g.write(str(0))
        g.close()
    width = size
    rows = 20
    s = snake(red, (10,10))
    h = open("score.txt", "r")
    best_score = int(h.read())
    print("Best Score : ", best_score)
    
    win = pygame.display.set_mode((width, width))
    snack = cube(randomSnack(rows, s), color=(green))
    flag = True
    clock = pygame.time.Clock()
    
    while flag:
        score = len(s.body)-1
        pygame.display.set_caption('Snake | Best : '+str(best_score)+' | Score : '+str(score)+" | Speed : "+str(speed))
        pygame.time.delay(50)
        clock.tick(speed)
        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            if (score+1)%5==0 and score!=0:
                speed += 1
            snack = cube(randomSnack(rows, s), color=green)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body)-1)
                if score > best_score:
                    best_score = score
                    g = open("score.txt", "w")
                    g.write(str(best_score))
                    g.close()
                #message_box('You Lost!', 'Score: '+str(score)+'\nYour Best: '+str(best_score)+'\nPlay again...')
                inputflag = True
                while inputflag == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    
                    yourscore_text = font.render((yourscore+str(score)), True, white)
                    yourscore_w, yourscore_h = font.size(yourscore+str(score))
                    yourbest_text = fontsmall.render((yourbest+str(best_score)), True, white)
                    yourbest_w, yourbest_h = fontsmall.size(yourbest+str(best_score))
                    pygame.draw.rect(win, lightgray, (size/5, 39/50*size, 3/5*size, 2/25*size))
                    win.blit(gameover_text, ((size - gameover_w) / 2, size/5))
                    win.blit(entername_text, ((size - entername_w) / 2, 17/25*size))
                    win.blit(yourscore_text, ((size - yourscore_w) / 2, 9/25*size))
                    win.blit(yourbest_text, ((size - yourbest_w) / 2, 23/50*size))

                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            exit()

                    # Feed it with events every frame
                    if textinput.update(events):
                        textoutput = textinput.get_text()
                        if textoutput != "":
                            print("Text Output : ", textoutput)
                            win.fill((0, 0, 0))
                            pygame.display.update()
                            inputflag = False
                    # Blit its surface onto the screen
                    win.blit(textinput.get_surface(), (11/50*size, 4/5*size))

                    pygame.display.update()
                    clock.tick(30)

                s.reset((10,10))
                break
            
        redrawWindow(win)
        
    pass

main()
