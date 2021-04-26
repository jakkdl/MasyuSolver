from PuzzleBoard import *
from MasyuExceptions import *

class PuzzleBoardFile():
    # Class variables
    __BLACK_CIRCLE = 'B'
    __WHITE_CIRCLE = 'W'
    __DOT = 'D'

    # This is the file extension we use for Puzzle Board Data file
    FILE_EXTENSION = 'pbd'      # Puzzle board data

    @classmethod
    # Method for saving a puzzle board to a file
    #
    # Parameter is the puzzle board to be written, and the path to the file to be written to
    def saveToFile(cls, filePath, puzzleBoard):
        # Create a list-of-lists for storing each line to be written to the file
        puzzleBoardFileData = []

        # Loop through the puzzle board object
        # Determine each cell type, and add it to the string representing the current row
        # When a row is done being processed, save it in the list-of-lists
        numRows, numCols = puzzleBoard.getDimensions()
        for rowNum in range(0, numRows):
            line = "["
            for colNum in range(0, numCols):
                if (puzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    line += cls.__BLACK_CIRCLE
                elif (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    line += cls.__WHITE_CIRCLE
                else:
                    line += cls.__DOT
            line += "]\n"
            puzzleBoardFileData.append(line)

        # Open the specified file; raise an exception if the system has any problems opening
        # the file (MasyuSaveFileException (propagate))
        try:
            with open(filePath, 'w') as filehandle:
                filehandle.writelines(puzzleBoardFileData)

        except Exception as e:
            raise MasyuFileSaveException("Error opening puzzle file") from e

    @classmethod
    # Method for loading a saved puzzle board file
    #
    # Performs some basic validation: makes sure that each row has the same number
    # of cells, verifies that the data only contains valid letters ('B', 'W', and 'D'), and
    # makes sure that the size of the puzzle is valid (not too large or too small).  Any
    # problems will cause an exception to be raised!
    #
    # If the data is correct, then it creates a new PuzzleBoard object, and sets the cells
    # to match the information read from the file
    def loadFile(cls, filePath):
        # Open the file; raise exception if that fails
        try:
            with open(filePath, 'r') as reader:
                allLines = reader.readlines()

        except Exception as e:
            raise MasyuFileOpenException("Error during opening Puzzle File") from e

        numCols = -1
        rowData = []
        for line in allLines:
            line = line.strip()
            length = len(line)

            if not (line.startswith("[")) or not (line.endswith("]")):
                raise MasyuInvalidPuzzleFileException("Invalid Puzzle File")
            else:
                line = line[1:(length - 1)]
                length = len(line)

            # Verify that each row is the same size; raise an exception if there is a mismatch
            if (numCols == -1):
                numCols = length
            elif (numCols != length):
                raise MasyuInvalidPuzzleFileException("Mismatched row and/or column lengths in Puzzle File")

            # Validate characters in the line
            for char in line:
                if not (char == cls.__DOT) and not (char == cls.__BLACK_CIRCLE) and not (char == cls.__WHITE_CIRCLE):
                    raise MasyuInvalidPuzzleFileException("Invalid character in Puzzle File")

            rowData.append(line)

        # Validate puzzle board size
        if not (PuzzleBoard.MIN_NUM_COLS <= numCols <= PuzzleBoard.MAX_NUM_COLS):
            raise MasyuInvalidPuzzleFileException("Invalid Puzzle Column Size")

        if not (PuzzleBoard.MIN_NUM_ROWS <= len(rowData) <= PuzzleBoard.MAX_NUM_ROWS):
            raise MasyuInvalidPuzzleFileException("Invalid Puzzle Row Size")

        # Create a new PuzzleBoard object of the needed size
        newPuzzleBoard = PuzzleBoard(size=(len(rowData), numCols))

        for rowNum in range (0, len(rowData)):
            nextRow = rowData[rowNum]

            for colNum in range (0, numCols):
                nextChar = nextRow[colNum]
                if (nextChar == cls.__WHITE_CIRCLE):
                    newPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                elif (nextChar == cls.__BLACK_CIRCLE):
                    newPuzzleBoard.setBlackCircleAt(rowNum, colNum)

        return (newPuzzleBoard)


if __name__ == "__main__":
    pb = PuzzleBoard()
    pb.setWhiteCircleAt(0, 0)
    pb.setBlackCircleAt(1, 1)
    PuzzleBoardFile.saveToFile("./testFile1" + "." + PuzzleBoardFile.FILE_EXTENSION, pb)