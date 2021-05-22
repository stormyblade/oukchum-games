from pythonProject.piece import Piece
from random import random
from pythonProject.game import Game

class Board():
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob                            #The probability that each piece is a bomb
        self.lost = False
        self.numClicked = 0
        self.numNonBombs = 0
        self.setBoard()

    def setBoard(self):
        self.board = []                             #The board is a list
        for row in range(self.size[0]):             #Iteration through the rows
            row = []                                #Row is a list, to be able to append and index it later
            for col in range(self.size[1]):         #Iteration through the columns
                hasBomb = random() < self.prob      #If a random float is smaller that the probability, hasBomb will be true
                if not hasBomb:                     #If the piece is not a bomb
                    self.numNonBombs +=1            #Add 1 to the number of pieces without a bomb
                piece = Piece(hasBomb)
                row.append(piece)                   #Appending a piece to each position
            self.board.append(row)                  #Adding the row list onto the board
        self.setNeighbors()                         #Defines the list of neighbors regarding one piece

    def setNeighbors(self):
        for row in range(self.size[0]):                             #Indexing the board
            for col in range(self.size[1]):
                piece = self.getPiece((row, col))
                neighbors = self.getListOfNeighbors((row, col))     #Gets and defines the list of neighbors of this piece
                piece.setNeighbors(neighbors)                       #Adding a list of neighbors to the piece

    def getListOfNeighbors(self, index):
        neighbors = []                                                                              #Defining the list of neighbors
        for row in range(index[0] - 1, index [0] + 2):                                              #Y wise, we start upper left of our piece, and we index through the piece above and the piece under
            for col in range(index[1] - 1, index[1] +2):                                            #X wise, we start upper left of our piece, and we index through the piece before and the piece after
                outOfBounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]      #Don't want to check out of the board, checking if piece is at the edges of board
                same = row == index[0] and col == index [1]                                         #Don't want to add our own piece to the list of neighbors
                if (same or outOfBounds):
                    continue
                neighbors.append(self.getPiece((row, col)))                                         #Adding the neighbors of our piece to the list of neighbors
        return neighbors


    def getSize(self):          #Function to get the size, x and y
        return self.size

    def getPiece(self, index):                  #Getting the piece from the index
        return self.board[index[0]][index[1]]   #Return from the array the index at the row and at the column

    def handleClick(self, piece, flag):                                     #When the user clicks
        if piece.getClicked() or (not flag and piece.getFlagged()):         #Don't do anything if the piece is already clicked or if user left-clicks on a flagged piece (flag is right-click)
            return
        if flag:                                                            #If user right-clicks
            piece.toggleFlag()                                              #Toggle the flag on the piece
            return
        piece.click()
        if piece.getHasBomb():                                              #If the piece was a bomb
            self.lost = True                                                #User loses
            return
        self.numClicked += 1                                                #If user clicked on a non-bomb, add 1 to the number of clicked non-bomb pieces
        if piece.getNumAround() != 0:                                       #For the recursive click (digging around piece when it has no bomb neighbors), if it does have neighbors just return
            return
        for neighbor in piece.getNeighbors():                                   #For each neighbor in the list of neighbors (called from piece)
            if not neighbor.getHasBomb() and not neighbor.getClicked():         #If it doesn't have a bomb and it's not already clicked
                self.handleClick(neighbor, False)                               #Click on it, passing the piece which is neighbor, we are not flagging it so False

    def getLost(self):
        return self.lost

    def getWon(self):
        return self.numNonBombs == self.numClicked      #If the number of non-bomb pieces = the number of pieces user clicked, user wins