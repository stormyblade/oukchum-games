import pygame
import pygame_textinput
import os
import time
from time import sleep
from constantes import c

white = c.white
black = c.black

size = c.largeur

class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]
        self.loadImages()

    def run(self):
        pygame.init()
        font = pygame.font.SysFont('comicsans', int(round(3 / 25 * size)))
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        winSoundPlayed = False
        inputFlag = False
        textinput = pygame_textinput.TextInput()
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)
            self.draw()
            pygame.display.flip()
            if (self.board.getWon() and not winSoundPlayed):
                sound = pygame.mixer.Sound("./win.wav")
                sound.play()
                winSoundPlayed = True
                winScreenPlayed = False
                inputFlag = True
                while inputFlag == True:

                    win_text = font.render("You Win, Good job!", True, c.black)
                    win_text_w, win_text_h = font.size("You Win, Good Job!")
                    pygame.draw.rect(self.screen, white, (size / 5, 39 / 50 * size, 3 / 5 * size, 2 / 25 * size))
                    self.screen.blit(win_text, ((size - win_text_w) / 2, size / 5))

                    if self.board.getWon():
                        finaltime = (pygame.time.get_ticks() // 1000)
                    score_text = font.render("Your Score : " + str(finaltime), True, c.black)
                    score_text_w, score_text_h = font.size("Your Score : " + str(finaltime))
                    if not winScreenPlayed:
                        self.screen.blit(score_text, ((size - score_text_w) / 2, size / 3))
                    winScreenPlayed = True

                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    if textinput.update(events):
                        name = textinput.get_text()
                        if name != "":
                            print("Text Output : ", name)
                            self.screen.fill((0, 0, 0))
                            pygame.display.update()
                            inputFlag = False
                            pygame.quit()

                    self.screen.blit(textinput.get_surface(), (11 / 50 * size, 4 / 5 * size))
                    pygame.display.update()
                    clock.tick(30)
                sleep(5)


    def draw(self):
        topLeft = (0, 0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = 0, topLeft [1] + self.pieceSize[1]

    def loadImages(self):
        self.images = {}
        for fileName in os.listdir("./images"):
            if (not fileName.endswith(".png")):
                continue
            image = pygame.image.load(r"./images/" + fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    def getImage(self, piece):
        string = None
        if(piece.getClicked()):
            string = "icon" if piece.getHasBomb() else str(piece.getNumAround())
        else:
            string = "flag" if piece.getFlagged() else "empty-block"
        return self.images[string]

    def handleClick(self, position, rightClick):
        if (self.board.getLost()):
            return
        index = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]
        piece = self.board.getPiece(index)
        self.board.handleClick(piece, rightClick)