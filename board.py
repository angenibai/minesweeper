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
        self.totalMines = boardSize + 1
        self.mines = set()

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
        minesLeft = self.totalMines
        while minesLeft > 0:
            # Create a random coordinate
            i = random.randrange(self.boardSize)
            j = random.randrange(self.boardSize)
            # If it hasn't already been added, add it
            if (i,j) not in self.mines:
                self.mines.add((i,j))
                minesLeft -= 1
        # Marks the mines on the board
        for location in self.mines:
            self.board[location[0]][location[1]] = 'X'
        # The mines have been placed

    # Figures out all the numbers
    def populate(self):
        for mineLocation in self.mines:
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
    def checkMove(self, i, j):
        return self.visible[i][j] == '.'

    # Clicking a spot the user believes to be free
    def click(self, i, j):
        successful = True
        if self.checkMove(i,j):
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
        self.visible[i][j] = '!'

    # Unmark a previously marked square
    def unMark(self, i, j):
        assert(self.visible[i][j] == '!')
        self.visible[i][j] = '.'

    # For debugging purposes, prints the full board
    def printBoard(self):
        alphabet = [chr(x) for x in range(97,97+self.boardSize)]
        alphabet = " ".join(alphabet)
        print("  " + alphabet)
        for i in range(self.boardSize):
            row = " ".join(str(x) for x in self.board[i])
            print(str(i)+ " " + row)
        print

    # Prints what's visible to the player
    def printState(self):
        alphabet = [chr(x) for x in range(97,97+self.boardSize)]
        alphabet = " ".join(alphabet)
        print("  " + alphabet)
        for i in range(self.boardSize):
            row = " ".join(str(x) for x in self.visible[i])
            print(str(i)+ " " + row)
        print


b = Board(9)
b.createGame()
b.printBoard()
b.printState()
print("Mark 5, 8")
b.mark(5,8)
b.printState()
if b.checkMove(5,8):
    print("Click 5, 8")
    b.click(5,8)
    b.printState()
if b.checkMove(4,8):
    print("Click 4, 8")
    b.click(4,8)
    b.printState()
if b.checkMove(3,8):
    print("Mark 3, 8")
    b.mark(3,8)
    b.printState()
print("Unmark 5, 8")
b.unMark(5,8)
b.printState()
