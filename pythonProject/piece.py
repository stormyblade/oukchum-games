class Piece():
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb      #Boolean to know if piece has a bomb or not
        self.clicked = False        #Initially nothing is clicked
        self.flagged = False        #Initially nothing is flagged

    def getHasBomb(self):           #Checks which piece has a bomb
        return self.hasBomb

    def getClicked(self):           #Checks which piece got clicked
        return self.clicked

    def getFlagged(self):           #Checks which piece got flagged
        return self.flagged

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        self.setNumAround()

    def setNumAround(self):
        self.numAround = 0                  #Counts the number of bombs around a piece
        for piece in self.neighbors:        #Iterate through the list of neighbors of the piece
            if (piece.getHasBomb()):        #If neighbor has bomb
                self.numAround += 1         #Add 1 to the number of the piece

    def getNumAround(self):         #Detects the number of bombs around each piece
        return self.numAround

    def toggleFlag(self):                           #Function to toggle the flag on and off
        self.flagged = not self.flagged             #When piece not flagged, flag it, when flagged, remove the flag

    def click(self):
        self.clicked = True

    def getNeighbors(self):
        return self.neighbors               #Return the list of neighbors when this function is called