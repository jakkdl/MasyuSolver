from Pathway import *
from Cell import *

# This class encapsulates the Puzzle Board.  To the "outside world",
# the puzzle board looks to be an RxC grid of cells.  Internally,
# the puzzle board is composed of a grid of Cell objects, separated
# by Pathway objects.
class PuzzleBoard():
    STATE_UNSOLVED = 0
    STATE_SOLVED = 1
    STATE_INVALID = -1

    MIN_NUM_ROWS = 5
    MIN_NUM_COLS = 5
    MAX_NUM_ROWS = 15
    MAX_NUM_COLS = 15

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
        else:
            self.numRows, self.numCols = size
            self.__createPuzzleBoard()

    # Internal method for creating an empty PuzzleBoard
    # for the specified numRows and numCols.  Besides placing
    # a Pathway object between each Cell, it also uses Pathway
    # objects to define the border around the edge of the puzzle
    # board, since the edges are (by definition) always blocked.
    #
    # In the grid, even numbered rows contain just Pathway objects,
    # while odd numbered rows contain alternating Pathway and Cell
    # objects.
    def __createPuzzleBoard(self):
        self.puzzleBoard = []
        for r in range(0, self.numRows):
            rowA = self.__createRowA()
            rowB = self.__createRowB()

            self.puzzleBoard.append(rowA)
            self.puzzleBoard.append(rowB)

        # Need to add the last row, representing the puzzle board boundary.
        self.puzzleBoard.append(self.__createRowA())

        # Block all pathways at the top puzzle border
        self.__blockTopOrBottomRow(self.puzzleBoard[0])

        # Block the pathways at the left and right edges
        for row in range(1, (len(self.puzzleBoard) - 1), 2):
            self.puzzleBoard[row][0].setAsBlocked()
            self.puzzleBoard[row][len(self.puzzleBoard[row]) - 1].setAsBlocked()

        # Block all pathways at the bottom puzzle border
        self.__blockTopOrBottomRow(self.puzzleBoard[len(self.puzzleBoard) - 1])

    # All top & bottom pathways are always blocked; they represent the border
    # of the puzzle board
    def __blockTopOrBottomRow(self, row):
        for colNum in range(1, len(row) - 1, 2):
            row[colNum].setAsBlocked()

    # To improve efficiency, each cell has a "processed" flag, which can be
    # set/cleared/queried; allows us to avoid reprecessing a cell during
    # certain operations (like following a line in the puzzle; senseless to
    # follow the line and then refollow it from the ending cell)!
    def wasCellProcessed(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].wasCellProcessed())

    def setCellProcessedFlag(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setProcessedFlag()

    def clearCellProcessedFlag(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].clearProcessedFlag()

    def clearAllCellProcessedFlags(self):
        for rowNum in range(0, self.numRows):
            for colNum in range(0, self.numCols):
                self.clearCellProcessedFlag(rowNum, colNum)

    # Convenience functions for tracking cell states
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

    # Convenience functons for tracking state information about the
    # Puzzle Board
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

    # Clears any solution work
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

    # Convenience functions for drawing a line from the specified cell.
    def drawLineUp(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum - 1][intColNum].setAsLine()

    def drawLineDown(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum + 1][intColNum].setAsLine()

    def drawLineLeft(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum - 1].setAsLine()

    def drawLineRight(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum + 1].setAsLine()

    # Convenience functions for blocking pathways from a specified cell
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

    # Convenince functions for marking a pathway as "open"
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

    # Since the outside world views the grid as being RxC, but
    # internally, we have a mix of Cell and Pathway objects, we
    # need to map the "outside worlds" cell coords in the
    # coords based on the internal puzzle board layout.
    def __mapRowAndCol(self, rowNum, colNum):
        return((rowNum*2) + 1, (colNum*2) + 1)

    # Returns the dimensions (row, col) for the current puzzle
    def getDimensions(self):
        return ((self.numRows,self.numCols))

    # Convenience functions for setting the cell type (black circle,
    # white circle, or dot) for the specified Cell object.
    def setBlackCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setAsBlackCircle()

    def setWhiteCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setAsWhiteCircle()
    
    def setGreyCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setAsGreyCircle()

    def setDotAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        self.puzzleBoard[intRowNum][intColNum].setAsDot()

    def isBlackCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return(self.puzzleBoard[intRowNum][intColNum].isBlackCircle())

    def isWhiteCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].isWhiteCircle())

    def isGreyCircleAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].isGreyCircle())

    def isCircleAt(self, rowNum, colNum):
        return self.isWhiteCircleAt(rowNum, colNum) or self.isBlackCircleAt(rowNum, colNum)

    def isDotAt(self, rowNum, colNum):
        intRowNum, intColNum = self.__mapRowAndCol(rowNum, colNum)
        return (self.puzzleBoard[intRowNum][intColNum].isDot())

    # Returns a tuple (# of lines, left, right, up, down) indicating
    # the number of lines currently defined for a cell, along with
    # boolean values indicating exactly which lines are defined).
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

    # Convenience functions for querying the presence of a specific
    # line in a cell
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

    # Returns a tuple (# of blocked paths, left, right, up, down) indicating
    # the number of blocked paths currently defined for a cell, along with
    # boolean values indicating exactly which paths are blocked).
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

    # Convenience functions for querying the presence of a specific
    # blockage in a cell
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

    # Returns a tuple (# of open paths, left, right, up, down) indicating
    # the number of open pathsways currently defined for a cell, along with
    # boolean values indicating exactly which paths are open).
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

    # Convenience functions for querying whether a specific
    # pathway in a cell is open
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
    # P=Pathway object and N=None
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
    # P=Pathway object and C=Cell object
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

    # Creates a clone (with or without any solution work) of
    # the current puzzle board object.
    def __clone(self, doFullClone, pbClone):
        for rowNum in range (0, self.numRows):
            for colNum in range (0, self.numCols):
                if (self.isBlackCircleAt(rowNum, colNum)):
                    pbClone.setBlackCircleAt(rowNum, colNum)
                elif (self.isWhiteCircleAt(rowNum, colNum)):
                    pbClone.setWhiteCircleAt(rowNum, colNum)
                elif (self.isGreyCircleAt(rowNum, colNum)):
                    pbClone.setGreyCircleAt(rowNum, colNum)

                # Copy any solution work only if a full close was requested
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

    # Returns a complete clone of the current Puzzle Board
    def cloneAll(self):
        pbClone = PuzzleBoard(size=(self.numRows, self.numCols))
        self.__clone(True, pbClone)
        return(pbClone)

    # Returns a clone of the Puzzle Board definition only
    def cloneBoardOnly(self):
        pbClone = PuzzleBoard(size=(self.numRows, self.numCols))
        self.__clone(False, pbClone)
        return(pbClone)

    # Resets the puzzle board to its "virgin" state
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


