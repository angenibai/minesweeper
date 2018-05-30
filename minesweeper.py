from board import Board

def checkInput(board, action, i, j):
    size = board.findSize()
    if action not in ('click', 'flag', 'unflag'):
        print("Invalid action. Please try again")
        return False
    if i < 0 or i >= size or j < 0 or j >= size:
        print("Coordinates are out of bounds. Please try again")
        return False
    return True


while True:
    size = int(input("How big would you like the board to be? "))
    if size > 26:
        print("Woah that's a bit too big.")
    else:
        break
print
board = Board(size)
board.createGame()
#board.printBoard()
safe = True

while board.findUnclicked() > board.findMinesLeft():
    print
    print(str(board.findMinesLeft()) + " mines left.")
    board.printState()
    print("Actions: ")
    print("   Click")
    print("   Flag")
    print("   Unflag")
    print("Specify square in format: letter number")
    print("   eg. Click square E6: Click E 6")
    print("   eg. Flag square C0: Flag C 0")
    print

    rawInput = raw_input("Make your move: ")
    action, j, i = rawInput.strip().split(" ")
    action = action.lower()
    j = ord(j.upper()) - 65
    i = int(i)
    if checkInput(board, action, i, j):
        if action == "click":
            if board.checkUnclicked(i, j):
                safe = board.click(i,j)
            else:
                print
                print("You are trying to click a square that has already been clicked")
        elif action == "flag":
            if board.findMinesLeft < 1:
                print("You have already marked all the mines that you can.")
            elif board.checkUnclicked(i,j):
                board.mark(i,j)
            else:
                print
                print("You are trying to mark a square that has already been clicked")
        elif action == "unflag":
            if board.checkMarked(i,j):
                board.unMark(i,j)
            else:
                print
                print("You are trying to unmark a square that hasn't been marked")
    if not safe:
        break

if safe:
    board.printBoard()
    print(":)")
else:
    board.printState()
    print(":(")
