from Pathway import *
from Cell import *

class PuzzleBoard():
    STATE_UNSOLVED = 0
    STATE_SOLVED = 1
    STATE_INVALID = -1
    __DEFAULT_NUM_ROWS = 8
    __DEFAULT_NUM_COLS = 8

    def __init__(self, size = None, puzzleData = None):
        self.state = PuzzleBoard.STATE_UNSOLVED

        if ((size == None) and (puzzleData == None)):
            self.numRows = PuzzleBoard.__DEFAULT_NUM_ROWS
            self.numCols = PuzzleBoard.__DEFAULT_NUM_COLS
            self.puzzleData = self.__createPuzzleBoard()
        elif (size != None):
            self.numRows, self.numCols = size
            self.puzzleData = self.__createPuzzleBoard()

    def __createPuzzleBoard(self):
        self.puzzleBoard = []
        for r in range(0, self.numRows):
            rowA = self.__createRowA()
            rowB = self.__createRowB()

            self.puzzleBoard.append(rowA)
            self.puzzleBoard.append(rowB)

        self.puzzleBoard.append(self.__createRowA())

    def __createRowA(self):
        rowA = []

        for c in range(0, self.numCols):
            rowA.append(None)
            rowA.append(Pathway())

        rowA.append(None)
        return(rowA)

    def __createRowB(self):
        rowB = []

        for c in range(0, self.numCols):
            rowB.append(Pathway())
            rowB.append(Cell())

        rowB.append(Pathway())
        return (rowB)

    def print(self):
        for l in self.puzzleBoard:
            for e in l:
                if e == None:
                    print("N", end = "")
                else:
                    e.print()
            print()

if __name__ == "__main__":
    print("Beginning Testing")

    b = PuzzleBoard()
    b.print()