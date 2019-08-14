import numpy as np
import os
from IPython.display import display, clear_output
from ipywidgets import widgets, Layout
import time

class ToManyBombs(Exception):
    """Raised when there are too many bombs"""
    pass

class minesweeper:
    def __init__(self, width=8, height=21, bombs=34, record=False):
        if bombs > width*height:
            raise ToManyBombs
        self.width = width
        self.height = height
        self.bombs = bombs
        self.record = record
        self.isFrist = True
        self.gameRecord = {}
        self.gameboard = None
        self.visible = [["?" for i in range(width)] for j in range(height)]
        self.init_board()

    def init_board(self):
        self.board = np.zeros((self.width, self.height), dtype=int)
        while self.num_bombs() < self.bombs:
            randRow = np.random.randint(self.height)
            randCol = np.random.randint(self.width)
            """Since it is impossible for squares to have more than 8 surronding bombs we will say that 9 represents a bomb"""
            self.board[randCol, randRow] = 9
        surroundingSquares = np.zeros((self.board.shape[0] + 2, self.board.shape[1] + 2))
        surroundingSquares[1:self.board.shape[0] + 1, 1:self.board.shape[1] + 1] = (self.board==9)
        allSurroundingDirections = [surroundingSquares[:-2,:-2], surroundingSquares[1:-1,:-2], surroundingSquares[2:, :-2],
                                  surroundingSquares[2:, 1:-1], surroundingSquares[:-2, 1:-1],
                                  surroundingSquares[:-2, 2:], surroundingSquares[1:-1, 2:], surroundingSquares[2:, 2:]]

        newBoard = sum(allSurroundingDirections)
        newBoard[np.where(self.board==9)] = 9
        self.board = newBoard.T
        self.startTime = time.time()


    def getSurroundingSquares(self, cordinates):
        y, x = cordinates
        surrondingSquares = []
        onLeftSide, onRightSide, onTop, onBot = False, False, False, False
        if x == 0:
            onLeftSide = True
        if x == self.width - 1:
            onRightSide = True
        if y == 0:
            onTop = True
        if y == self.height - 1:
            onBot = True
        validSquares = [[True & (not onLeftSide) & (not onTop), True & (not onTop), True & (not onTop) & (not onRightSide)],
                             [True & (not onLeftSide), None, True & (not onRightSide)],
                             [True & (not onLeftSide) & (not onBot), True & (not onBot), True & (not onBot) & (not onRightSide)]]
        for r, row in enumerate(validSquares):
            for c, cell in enumerate(row):
                if cell:
                    surrondingSquares.append((y+r-1, x+c-1))
        return surrondingSquares

    def num_bombs(self):
        return np.sum(self.board == 9)

    def firstClick(self, coordinate):
        while self.board[coordinate] != 0:
            self.init_board()

    def clickCell(self, coordinate):
        if (self.isFrist):
            self.firstClick(coordinate)
            self.isFrist = False
        if (self.record):
            self.gameRecord[time.time() - self.startTime] = coordinate
        x, y = coordinate
        if self.visible[x][y] != "?":
            pass
        elif self.board[coordinate] == 0:
            self.visible[x][y] = "*"
            for cell in self.getSurroundingSquares(coordinate):
                self.clickCell(cell)
        elif self.board[coordinate] != 9:
            self.visible[x][y] = str(self.board[coordinate])
        else:
            self.loseGame()

    def clickCellCallback(self, button):
        coordinate = eval(button.tooltip)
        if (self.isFrist):
            self.firstClick(coordinate)
            self.isFrist = False
        if (self.record):
            self.gameRecord[time.time() - self.startTime] = coordinate
        x, y = coordinate
        if self.visible[x][y] != "?":
            pass
        elif self.board[coordinate] == 0:
            self.visible[x][y] = "*"
            button.description = ""
            button.disabled = True
            for cell in self.getSurroundingSquares(coordinate):
                self.gameboard[cell[0]][cell[1]].click()
        elif self.board[coordinate] != 9:
            self.visible[x][y] = str(self.board[coordinate])
            button.description = str(self.board[coordinate])
            button.disabled = True
        else:
            self.visible[x][y] = str(self.board[coordinate])
            button.description = str(self.board[coordinate])
            self.loseGame()
            button.style.button_color = "#F77"
            #clear_output()
            display(self.visible)
        if sum([sum([c == "?" for c in row]) for row in self.visible]) == self.bombs:
            self.winGame()
            #clear_output()
            display(self.visible)
        #self.playOnNoteBook()

    def winGame(self):
        if self.gameboard:
            for row in self.gameboard:
                for btn in row:
                    btn.disabled = True
        self.score = time.time() - self.startTime
        self.visible = "You have won!"

    def loseGame(self):
        if self.gameboard:
            for i, row in enumerate(self.gameboard):
                for j, btn in enumerate(row):
                    btn.description = str(self.board[(i, j)])
                    btn.disabled = True
        self.score = 10000
        self.visible = "You have lost"

    def getScore(self):
        self.score = time.time() - self.startTime
        return time.time() - self.startTime

    def pprint(self):
        for row in self.visible:
            for c in row:
                print(c, "\t", end="")
            print("\n")

    def flag(self, coordinate):
        x, y = coordinate
        self.visible[x][y] = "X"

    def play(self):
        while self.visible != "You have lost":
            os.system('clear')
            self.pprint()
            myinput = tuple(x.strip() for x in input("Where would you like to click?").split(','))
            if myinput[0] == "f":
                self.flag((int(myinput[1]), int(myinput[2])))
            else:
                self.clickCell((int(myinput[0]), int(myinput[1])))
        print(self.visible)

    def playOnNoteBook(self):
        if (self.visible != "You have lost" and self.visible != "You have won!"):
            clear_output(wait=True)
            self.readyToRefreshGameBoard = False;
            self.gameboard = []
            for r, row in enumerate(self.visible):
                gameRow = []
                for c, v in enumerate(row):
                    cord = (r,c)
                    buttonDisctiptions = str(int(float(v))) if (v!="?" and v!="*") else ""
                    buttonColor = "#DDD" if (v!="?") else "#AAA"
                    bToAdd = widgets.Button(description=buttonDisctiptions, tooltip = str(cord), layout=Layout(width='30px', height='30px', padding="0px", color=buttonColor), disabled=(v != "?"))
                    bToAdd.style.button_color = buttonColor
                    bToAdd.on_click(self.clickCellCallback)
                    gameRow.append(bToAdd)
                self.gameboard.append(gameRow)
            for row in self.gameboard:
                display(widgets.HBox(row))
        else:
            clear_output()
            display(self.visible)

    def solvePercent(self, percent):
        while sum([f=="?" for f in sum(self.visible, [])])/(self.width * self.height) > percent:
            randRow = np.random.randint(self.height)
            randCol = np.random.randint(self.width)
            coordinate = (randRow, randCol)
            if self.board[coordinate] != 9:
                self.clickCell(coordinate)
            else:
                self.visible[randRow][randCol] = 9.0
