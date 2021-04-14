from Pathway import *
from Cell import *

class PuzzleBoard():
    STATE_UNSOLVED = 0
    STATE_SOLVED = 1
    STATE_INVALID = -1
    __DEFAULT_NUM_ROWS = 8
    __DEFAULT_NUM_COLS = 8

    # Constructor
    # If given, the 'size' parameter is a tuple,
    # specifying the number of rows and the number of columns
    # If given, the 'puzzleData' parameter can either be just
    # the puzzle definition, or it can be a tuple specifying
    # both the puzzle definition and the solution information
    # If neither parameter is specified, then a default
    # 8X8 empty board is created
    #
    def __init__(self, size = None, puzzleData = None):
        self.state = PuzzleBoard.STATE_UNSOLVED

        if ((size == None) and (puzzleData == None)):
            self.numRows = PuzzleBoard.__DEFAULT_NUM_ROWS
            self.numCols = PuzzleBoard.__DEFAULT_NUM_COLS
            self.__createPuzzleBoard()
        elif (puzzleData != None):
            # todo: define this case
            print("not implemented")
        else:
            self.numRows, self.numCols = size
            self.__createPuzzleBoard()

    # Internal method for creating an empty PuzzleBoard
    # for the specified numRows and numCols
    #
    def __createPuzzleBoard(self):
        self.puzzleBoard = []
        for r in range(0, self.numRows):
            rowA = self.__createRowA()
            rowB = self.__createRowB()

            self.puzzleBoard.append(rowA)
            self.puzzleBoard.append(rowB)

        self.puzzleBoard.append(self.__createRowA())

        self.__blockTopOrBottomRow(self.puzzleBoard[0])

        for row in range(1, (len(self.puzzleBoard) - 1), 2):
            self.puzzleBoard[row][0].setAsBlocked()
            self.puzzleBoard[row][len(self.puzzleBoard[row]) - 1].setAsBlocked()

        self.__blockTopOrBottomRow(self.puzzleBoard[len(self.puzzleBoard) - 1])

    def __blockTopOrBottomRow(self, row):
        for colNum in range(1, len(row) - 1, 2):
            row[colNum].setAsBlocked()

    def isCellEnabled(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].isEnabled())

    def setCellEnabled(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setEnabled()

    def setCellDisabled(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setDisabled()

    def isCellValid(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].isValid())

    def setCellValid(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setValid()

    def setCellInvalid(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setInvalid()

    def isSolved(self):
        return (self.state == PuzzleBoard.STATE_SOLVED)

    def isUnsolved(self):
        return (self.state == PuzzleBoard.STATE_UNSOLVED)

    def isInvalid(self):
        return (self.state == PuzzleBoard.STATE_INVALID)

    def setSolved(self):
        self.state = PuzzleBoard.STATE_SOLVED

    def setUnsolved(self):
        self.state = PuzzleBoard.STATE_UNSOLVED

    def setInvalid(self):
        self.state = PuzzleBoard.STATE_INVALID

    def getSolution(self):
        print("get solution not implemeted")
        # todo implement getSolution()

    def setSolution(self, solution):
        print("set solution not implemented")
        # todo implement setSolution()

    def clearSolution(self):
        for rowNum in range(1, (len(self.puzzleBoard) - 1)):
            row = self.puzzleBoard[rowNum]
            if ((rowNum % 2) == 0):
                # Even Rows
                for colNum in range(1, len(row)-1, 2):
                    row[colNum].setAsOpen()
            else:
                # Odd Rows
                for colNum in range(2, len(row)-2, 2):
                    row[colNum].setAsOpen()

    def lookForBug(self, rowNum, colNum):
        numLines, u, d, l, r = self.getLines(4, 2)
        if (numLines > 2):
            print("BUG!! Cell", 4, "x", 2, "has", numLines, "lines!")
            print("\tThe line was drawn from cell:", rowNum, "x", colNum)

    def drawLineUp(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum - 1][intColNum].setAsLine()
        self.lookForBug(rowNum, colNum)

    def drawLineDown(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum + 1][intColNum].setAsLine()
        self.lookForBug(rowNum, colNum)

    def drawLineLeft(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum - 1].setAsLine()
        self.lookForBug(rowNum, colNum)

    def drawLineRight(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum + 1].setAsLine()
        self.lookForBug(rowNum, colNum)

    def markBlockedUp(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum - 1][intColNum].setAsBlocked()

    def markBlockedDown(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum + 1][intColNum].setAsBlocked()

    def markBlockedLeft(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum - 1].setAsBlocked()

    def markBlockedRight(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum + 1].setAsBlocked()

    def markOpenUp(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum - 1][intColNum].setAsOpen()

    def markOpenDown(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum + 1][intColNum].setAsOpen()

    def markOpenLeft(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum - 1].setAsOpen()

    def markOpenRight(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum + 1].setAsOpen()

    def __mapRowAndCol(self, rowNum, colNum):
        return((rowNum*2) + 1, (colNum*2) + 1)

    def getDimensions(self):
        return ((self.numRows,self.numCols))

    def setBlackCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setAsBlackCircle()

    def setWhiteCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setAsWhiteCircle()

    def setDotAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setAsDot()

    def isBlackCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return(self.puzzleBoard[intRowNum][intColNum].isBlackCircle())

    def isWhiteCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].isWhiteCircle())

    def isDotAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].isDot())

    def getLines(self, rowNum, colNum):
        count = 0
        up = self.hasLineUp(rowNum, colNum)
        if (up):
            count += 1
        down = self.hasLineDown(rowNum, colNum)
        if (down):
            count += 1
        left = self. hasLineLeft(rowNum, colNum)
        if (left):
            count += 1
        right = self.hasLineRight(rowNum, colNum)
        if (right):
            count += 1
        return ((count, left, right, up, down))


    def hasLineUp(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum - 1][intColNum].isLine())

    def hasLineDown(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum + 1][intColNum].isLine())

    def hasLineLeft(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum - 1].isLine())

    def hasLineRight(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum + 1].isLine())

    def getBlockedPaths(self, rowNum, colNum):
        count = 0
        up = self.isBlockedUp(rowNum, colNum)
        if (up):
            count += 1
        down = self.isBlockedDown(rowNum, colNum)
        if (down):
            count += 1
        left = self. isBlockedLeft(rowNum, colNum)
        if (left):
            count += 1
        right = self.isBlockedRight(rowNum, colNum)
        if (right):
            count += 1
        return ((count, left, right, up, down))

    def isBlockedUp(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum - 1][intColNum].isBlocked())

    def isBlockedDown(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum + 1][intColNum].isBlocked())

    def isBlockedLeft(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum - 1].isBlocked())

    def isBlockedRight(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum + 1].isBlocked())


    def getOpenPaths(self, rowNum, colNum):
        count = 0
        up = self.isOpenUp(rowNum, colNum)
        if (up):
            count += 1
        down = self.isOpenDown(rowNum, colNum)
        if (down):
            count += 1
        left = self. isOpenLeft(rowNum, colNum)
        if (left):
            count += 1
        right = self.isOpenRight(rowNum, colNum)
        if (right):
            count += 1
        return ((count, left, right, up, down))

    def isOpenUp(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum - 1][intColNum].isOpen())

    def isOpenDown(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum + 1][intColNum].isOpen())

    def isOpenLeft(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum - 1].isOpen())

    def isOpenRight(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum + 1].isOpen())

    # Internal method for creating a pathway row that
    # represents pathways above and below the cell row:
    #  'N P N P ... P N'
    #
    def __createRowA(self):
        rowA = []

        for c in range(0, self.numCols):
            rowA.append(None)
            rowA.append(Pathway())

        rowA.append(None)
        return(rowA)

    # Internal method for creating the cell row:
    # 'P C P C ... C P'
    #
    def __createRowB(self):
        rowB = []

        for c in range(0, self.numCols):
            rowB.append(Pathway())
            rowB.append(Cell())

        rowB.append(Pathway())
        return (rowB)

    # Print the PuzzleBoard
    #
    def print(self):
        for row in self.puzzleBoard:
            for cell in row:
                if cell == None:
                    print("N", end = "")
                else:
                    cell.print()
            print()
        print()

    def __clone(self, doFullClone, pbClone):
        for rowNum in range (0, self.numRows):
            for colNum in range (0, self.numCols):
                if (self.isBlackCircleAt(rowNum, colNum)):
                    pbClone.setBlackCircleAt(rowNum, colNum)
                elif (self.isWhiteCircleAt(rowNum, colNum)):
                    pbClone.setWhiteCircleAt(rowNum, colNum)

                if (doFullClone):
                    if (self.hasLineUp(rowNum, colNum)):
                        pbClone.drawLineUp(rowNum, colNum)
                    if (self.hasLineDown(rowNum, colNum)):
                        pbClone.drawLineDown(rowNum, colNum)
                    if (self.hasLineLeft(rowNum, colNum)):
                        pbClone.drawLineLeft(rowNum, colNum)
                    if (self.hasLineRight(rowNum, colNum)):
                        pbClone.drawLineRight(rowNum, colNum)
                    if (self.isBlockedUp(rowNum, colNum)):
                        pbClone.markBlockedUp(rowNum, colNum)
                    if (self.isBlockedDown(rowNum, colNum)):
                        pbClone.markBlockedDown(rowNum, colNum)
                    if (self.isBlockedLeft(rowNum, colNum)):
                        pbClone.markBlockedLeft(rowNum, colNum)
                    if (self.isBlockedRight(rowNum, colNum)):
                        pbClone.markBlockedRight(rowNum, colNum)

                if (self.isSolved() and doFullClone):
                    pbClone.setSolved()
                elif (self.isInvalid()):
                    pbClone.setInvalid()
                else:
                    pbClone.setUnsolved()


    def cloneAll(self):
        pbClone = PuzzleBoard(size=(self.numRows, self.numCols))
        self.__clone(True, pbClone)
        return(pbClone)

    def cloneBoardOnly(self):
        pbClone = PuzzleBoard(size=(self.numRows, self.numCols))
        self.__clone(False, pbClone)
        return(pbClone)

    def reset(self):
        self.state = PuzzleBoard.STATE_UNSOLVED
        self.puzzleData = self.__createPuzzleBoard()

if __name__ == "__main__":
    print("Beginning Testing")

    b = PuzzleBoard()
    b.print()

    b.drawLineUp(3, 4)
    b.drawLineLeft(2, 1)
    b.print()

    b.markBlockedLeft(3, 4)
    b.markOpenLeft(2, 1)
    b.setBlackCircleAt(6,5)
    b.setWhiteCircleAt(4,2)
    b.print()

    b.clearSolution()
    b.setDotAt(6,5)
    b.setDotAt(4,2)
    b.print()


