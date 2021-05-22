import pygame
import pygame_textinput
import os
import pickle
import time
from time import sleep
from constantes import c

white = c.white
black = c.black

size = c.largeur


class Game():
    def __init__(self, board, screenSize):  #Initializing the attributes needed for project
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]  #The piece size is the width of the board // by nb of colums, and the height // by nb of rows
        self.loadImages()

    def run(self):
        pygame.init()
        font = pygame.font.SysFont('comicsans', int(round(3 / 25 * size)))
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        winSoundPlayed = False
        loseSoundPlayed = False
        loseScreenShow = False
        inputFlag = False
        textinput = pygame_textinput.TextInput()
        clock = pygame.time.Clock()

        dico = (load_obj("./pythonProject/minesweeper_score.txt"))

        print("Dico actuel : " + str(dico))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   #Quits the program if user quits
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:            #If user clicks anywhere on screen
                    position = pygame.mouse.get_pos()               #Getting the position
                    rightClick = pygame.mouse.get_pressed()[2]      #Checking if it was a right click, 2 is right click
                    self.handleClick(position, rightClick)          #Passes the position and rightClick information to this function

            self.draw()                                         #Draws the board
            pygame.display.flip()                               #Updates the screen
            if self.board.getLost() and not loseScreenShow :
                if not loseSoundPlayed:
                    sound = pygame.mixer.Sound("pythonProject/lose.wav")
                    sound.play()
                    loseSoundPlayed = True

                inputFlag = True

                while (inputFlag):
                    lose_text = font.render("You Lost!", True, c.black)
                    lose_text_w, lose_text_h = font.size("You Lost!")
                    self.screen.blit(lose_text, ((size - lose_text_w) / 2, size / 5))
                    pygame.display.update()
                    loseScreenShow = True
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()

            if self.board.getWon() and not winSoundPlayed:
                sound = pygame.mixer.Sound("pythonProject/win.wav")
                sound.play()

                if self.board.getWon():
                    finaltime = (pygame.time.get_ticks() // 1000)

                winSoundPlayed = True
                winScreenPlayed = False
                inputFlag = True
                while inputFlag == True:

                    win_text = font.render("You Win, Good job!", True, c.black)
                    win_text_w, win_text_h = font.size("You Win, Good Job!")
                    pygame.draw.rect(self.screen, white, (size / 5, 39 / 50 * size, 3 / 5 * size, 2 / 25 * size))
                    self.screen.blit(win_text, ((size - win_text_w) / 2, size / 5))

                    score_text = font.render("Your Time : " + str(finaltime) + "s", True, c.black)
                    score_text_w, score_text_h = font.size("Your Time : " + str(finaltime) + "s")
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
                            try:
                                if dico[name] > finaltime:
                                    dico[name] = finaltime
                            except:
                                dico[name] = finaltime
                            save_obj(dico, "./pythonProject/minesweeper_score.txt")
                            print(load_obj("./pythonProject/minesweeper_score.txt"))
                            inputFlag = False
                            pygame.quit()

                    self.screen.blit(textinput.get_surface(), (11 / 50 * size, 4 / 5 * size))
                    pygame.display.update()
                    clock.tick(30)
                sleep(5)


    def draw(self):                                                     #Function that draws the board
        topLeft = (0, 0)                                                #Starting from the top left corner
        for row in range(self.board.getSize()[0]):                      #Row in range [number of rows]
            for col in range(self.board.getSize()[1]):                  #Column in range [number of columns]
                piece = self.board.getPiece((row, col))                 #Getting the piece from the board by passing an index
                image = self.getImage(piece)                            #The image is the image based on the piece
                self.screen.blit(image, topLeft)                        #Printing image, starting top left
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]    #Updating the topLeft x-wise by adding the width of the piece size to its x coordinate, and keeping the y coordinate as it was
            topLeft = 0, topLeft [1] + self.pieceSize[1]                #Updating the topLeft y-wise by adding the height of the piece size to its y coordinate, and keeping the x coordinate as it was

    def loadImages(self):                                                          #Function that loads images
        self.images = {}                                                           #Dictionnary that maps the name of images and its image object
        for fileName in os.listdir("pythonProject/images"):
            if not fileName.endswith(".png"):                                      #Skips the function if not an image
                continue
            image = pygame.image.load(r"pythonProject/images/" + fileName)         #Loading the image and its filename
            image = pygame.transform.scale(image, self.pieceSize)                  #Transforming the image to the size we need
            self.images[fileName.split(".")[0]] = image                            #Setting image object as the image in the dictionnary as everything before ".png" is at index 0 in the dictionnary

    def getImage(self, piece):
        string = None
        if piece.getClicked():
            string = "icon" if piece.getHasBomb() else str(piece.getNumAround())    #When piece gets clicked, show the bomb image if it was a bomb, or show the image with the number of bombs around the piece
        else:                                                                       #If it was a left click
            string = "flag" if piece.getFlagged() else "empty-block"                #Flag the piece if the function is true, else show an empty block
        return self.images[string]                                                  #Index the resulting image in the dictionnary

    def handleClick(self, position, rightClick):
        if self.board.getLost():                            #If the user has lost
            return                                          #Just return, don't let user click anymore
        index = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]      #Index which piece user clicked by floor dividing the x or y position of the click by the x or y lenght of the piece
        piece = self.board.getPiece(index)                                              #Grab the piece from the board in the index
        self.board.handleClick(piece, rightClick)                                       #Pass the click of the piece information to the board


def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)