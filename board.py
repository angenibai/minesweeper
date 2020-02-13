'''
Here's the code that sets up the Board class
and basically is the functioning logic that
generates all the mines.

Coded by Angeni Bai
'''


import random

class Board(object):
    '''
    When creating the game for the first time
        1. board = Board()
        2. board.createGame()
    '''

    # Needs checks to make sure not accessing beyond the board
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.board = [[0 for x in range(boardSize)] for x in range(boardSize)]
        self.visible = [['.' for x in range(boardSize)] for x in range(boardSize)]
        self.minesTotal = boardSize + 1
        self.mineLocations = set()
        self.minesFound = 0
        self.safeSquaresTotal = boardSize*boardSize - self.minesTotal

    def findSize(self):
        return self.boardSize

    def findMinesTotal(self):
        return self.minesTotal

    def findMinesLeft(self):
        return self.minesTotal - self.minesFound

    def findUnclicked(self):
        clicked = 0
        for row in self.visible:
            clicked += row.count('.')
        return clicked

    def findSafeSquares(self):
        return self.safeSquaresTotal

    # Returns set with coordinates of all the neighbours of the coordinate
    def findNeighbours(self, i, j):
        assert(i >= 0 and i < self.boardSize and j >= 0 and j < self.boardSize)
        neighbours = set()
        neighbours.add((max(0,i-1), max(0,j-1)))
        neighbours.add((max(0,i-1), j))
        neighbours.add((max(0,i-1), min(self.boardSize-1,j+1)))
        neighbours.add((i, max(0,j-1)))
        neighbours.add((i, min(self.boardSize-1,j+1)))
        neighbours.add((min(self.boardSize-1,i+1), max(0,j-1)))
        neighbours.add((min(self.boardSize-1,i+1), j))
        neighbours.add((min(self.boardSize-1,i+1), min(self.boardSize-1,j+1)))
        if (i,j) in neighbours:
            neighbours.remove((i,j))
        return neighbours

    # Creates the mines and adds them to the board
    def generateMines(self):
        # Place the mines
        minesLeft = self.minesTotal
        while minesLeft > 0:
            # Create a random coordinate
            i = random.randrange(self.boardSize)
            j = random.randrange(self.boardSize)
            # If it hasn't already been added, add it
            if (i,j) not in self.mineLocations:
                self.mineLocations.add((i,j))
                minesLeft -= 1
        # Marks the mines on the board
        for location in self.mineLocations:
            self.board[location[0]][location[1]] = 'X'
        # The mines have been placed

    # Figures out all the numbers
    def populate(self):
        for mineLocation in self.mineLocations:
            # Find the neighbours of every mine
            neighbours = self.findNeighbours(mineLocation[0],mineLocation[1])
            # For every neighbour, if it isn't a mine, add one to its value
            for location in neighbours:
                i = location[0]
                j = location[1]
                if isinstance(self.board[i][j], int):
                    self.board[i][j] += 1

    # Beginning a game
    def createGame(self):
        self.generateMines()
        self.populate()

    # Returns true if spot has not been clicked
    def checkUnclicked(self, i, j):
        return self.visible[i][j] == '.'

    # Returns true if spot has been marked
    def checkMarked(self, i, j):
        return self.visible[i][j] == 'F'

    # Clicking a spot the user believes to be free
    def click(self, i, j):
        successful = True
        if self.checkUnclicked(i,j):
            self.visible[i][j] = self.board[i][j]
            if self.board[i][j] == 'X':
                # Clicked a mine
                successful = False
            elif self.board[i][j] == 0:
                neighbours = self.findNeighbours(i,j)
                for location in neighbours:
                    a = location[0]
                    b = location[1]
                    self.click(a,b)
        return successful

    # Marking the site of a mine
    def mark(self, i, j):
        self.visible[i][j] = 'F'
        self.minesFound += 1

    # Unmark a previously marked square
    def unMark(self, i, j):
        assert(self.visible[i][j] == 'F')
        self.visible[i][j] = '.'
        self.minesFound -= 1

    # For debugging purposes, prints the full board
    def printBoard(self):
        alphabet = [chr(x) for x in range(97,97+self.boardSize)]
        alphabet = " ".join(alphabet)
        print("    " + alphabet)
        print("    " + " ".join('-' for i in range(self.boardSize)))
        for i in range(self.boardSize):
            row = " ".join(str(x) for x in self.board[i])
            print(str(i)+ " " + row)
        print

    # Prints what's visible to the player
    def printState(self):
        alphabet = [chr(x) for x in range(65,65+self.boardSize)]
        alphabet = " ".join(alphabet)
        print("    " + alphabet)
        print("    " + " ".join('-' for i in range(self.boardSize)))
        for i in range(self.boardSize):
            row = " ".join(str(x) for x in self.visible[i])
            print(str(i)+ " | " + row)
        print

def test():
    b = Board(4)
    b.createGame()
    print(b.findUnclicked())
