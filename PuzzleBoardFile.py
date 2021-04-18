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

if __name__ == "__main__":
    pb = PuzzleBoard()
    pb.setWhiteCircleAt(0, 0)
    pb.setBlackCircleAt(1, 1)
    PuzzleBoardFile.saveToFile("./testFile1" + "." + PuzzleBoardFile.FILE_EXTENSION, pb)