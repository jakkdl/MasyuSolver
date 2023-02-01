class Utilities():

    @classmethod
    # Given how the current cell was entered (specified by lastRowOffset and lastColOffset),
    # disable that particular line (to prevent backtracking), and return the offset to be
    # used to travel to the next cell .. or (-1, -1), it there isn't a second line leading
    # out of the current cell.
    def chooseNextLineToFollow(cls, lastRowOffset, lastColOffset, l, r, u, d):
        # Disable the line we used to enter the current cell
        if ((lastRowOffset == 1) and (lastColOffset == 0)):
            # Entry was via the top line
            u = False
        elif ((lastRowOffset == -1) and (lastColOffset == 0)):
            # Entry was via the bottom line
            d = False
        elif ((lastRowOffset == 0) and (lastColOffset == 1)):
            # Entry was via the left line
            l = False
        elif ((lastRowOffset == 0) and (lastColOffset == -1)):
            # Entry was via the right line
            r = False

        # Now, no more than one path should remain available, so
        # take it
        if (l):
            return((0, -1))
        elif (r):
            return((0, 1))
        elif (u):
            return((-1, 0))
        elif (d):
            return((1, 0))
        else:
            # No path to follow!
            return((-1, -1))

    # Returns number of black and white circles in the puzzle
    @classmethod
    def getNumberOfCircles(cls, puzzleBoard):
        numCircles = 0
        numRows, numCols = puzzleBoard.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if puzzleBoard.isCircleAt(rowNum, colNum):
                    numCircles += 1

        return (numCircles)

    # Enable all the cells in the specified puzzle board
    @ classmethod
    def enableAllCells(cls, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                puzzleBoard.setCellEnabled(rowNum, colNum)

    # A puzzle is solved when there is a single closed path, which travels through
    # all of the circles in the puzzle.
    @classmethod
    def checkIfPuzzleIsSolved(cls, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        numCirclesInPuzzle = Utilities.getNumberOfCircles(puzzleBoard)
        numCirclesFound = 0

        for rowNum in range (0, numRows):
            for colNum in range (0, numCols):
                # Start by looking for a cell with 2 lines, and then see if it forms a closed loop.
                # But if we encounter a cell with only 1 line, or a circle with < 2 lines, then
                # we can stop because we know the puzzle isn't solved
                numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

                # Check for a single line
                if (0 < numLines < 2):
                    return(False)

                if (numLines == 0):
                    if not (puzzleBoard.isCircleAt(rowNum, colNum)):
                        # Keep looking
                        continue
                    else:
                        # Found a circle with no lines!
                        return(False)

                # We've found the line to follow!  Pick a direction to go!
                if (u):
                    nextRowOffset = -1
                    nextColOffset = 0
                elif (d):
                    nextRowOffset = 1
                    nextColOffset = 0
                elif (l):
                    nextRowOffset = 0
                    nextColOffset = -1
                elif (r):
                    nextRowOffset = 0
                    nextColOffset = 1

                startingRowNum = rowNum
                startingColNum = colNum

                nextRowNum = rowNum + nextRowOffset
                nextColNum = colNum + nextColOffset

                # See if we are starting in a cell with a circle
                if (puzzleBoard.isCircleAt(rowNum, colNum)):
                    numCirclesFound += 1

                # Follow the path until we come back to where we started, or the line stops
                while ((nextRowNum != startingRowNum) or (nextColNum != startingColNum)):
                    numLines, l, r, u, d = puzzleBoard.getLines(nextRowNum, nextColNum)

                    # Check if the line stopped
                    if (numLines < 2):
                        return (False)

                    # Determine which cell to go to next
                    nextRowOffset, nextColOffset = Utilities.chooseNextLineToFollow(nextRowOffset, nextColOffset, l, r, u, d)

                    if ((nextRowOffset == -1) and (nextColOffset == -1)):
                        return (False)

                    # Track if this cell had a circle
                    if (puzzleBoard.isCircleAt(nextRowNum, nextColNum)):
                        numCirclesFound += 1

                    nextRowNum = nextRowNum + nextRowOffset
                    nextColNum = nextColNum + nextColOffset

                # If we made it here, then the puzzle was solved if all the circles were visited
                if (numCirclesInPuzzle == numCirclesFound):
                    return(True)

                # This should happen!
                return(False)
