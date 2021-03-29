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
        for col in range(1, len(row) - 1, 2):
            row[col].setAsBlocked()



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

    def clone(self):
        #todo: needs to be implemented
        print("not implemented")

    def cloneBoardOnly(self):
        #todo: needs to be implemented
        print("not implemented")

    def reset(self):
        self.state = PuzzleBoard.STATE_UNSOLVED
        self.puzzleData = self.__createPuzzleBoard()

if __name__ == "__main__":
    print("Beginning Testing")

    b = PuzzleBoard()
    b.print()