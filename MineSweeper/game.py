import numpy as np

class ToManyBombs(Exception):
    """Raised when there are too many bombs"""
    pass

class minesweeper:
    def __init__(self, width=8, height=21, bombs=34):
        if bombs > width*height:
            raise ToManyBombs
        self.width = width
        self.height = height
        self.bombs = bombs
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
        self.board = newBoard

                    
    def getSurroundingSquares(self, cordinates):
        x, y = cordinates
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
                    surrondingSquares.append((x+c-1, y+r-1))
        return surrondingSquares
        
    def num_bombs(self):
        return np.sum(self.board == 9)
    
    def clickCell(self, coordinate):
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
            
    def loseGame(self):
        self.visible = "You have lost"
    
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
            self.pprint()
            myinput = tuple(x.strip() for x in input("Where would you like to click?").split(','))
            if myinput[0] == "f":
                self.flag((int(myinput[1]), int(myinput[2])))
            else:
                self.clickCell((int(myinput[0]), int(myinput[1])))
        print(self.visible)
        
        