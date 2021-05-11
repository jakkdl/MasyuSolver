from MasyuExceptions import *
from Utilities import *
from OrphanedRegions import *

class Solver():
    def __init__(self):
        self.__orphanedRegionDetector = OrphanedRegions()

    def solve(self,puzzleBoard):
        changed = True
        # You can't terminate the solving loop when the puzzle becomes solved, because this ends up
        # leaving cells enabled which should have been disabled .. but they aren't, because the
        # solving loop prematurely exited because it thought the puzzle was solved .. even though
        # the "solving" happened in the clone board, while trying to determine which cells needed to
        # be disabled!

        # Temporary flag to allow disabling of the orphaned region code,
        # until the point where the bugs have been worked out
        orphanedRegionCheckEnabled = True

        while (changed):
            changed = False
            changed = changed or self.__processSpecialCases(puzzleBoard)
            #print("before findPathwaysToBlock")
            #puzzleBoard.print()
            changed = changed or self.__findPathwaysToBlock(puzzleBoard)
            #print("after findPathwaysToBlock")
            #puzzleBoard.print()
            changed = changed or self.__processDeadendPaths(puzzleBoard)
            #print("after processDeadendPaths")
            #puzzleBoard.print()
            changed = changed or self.__processBlackCircles(puzzleBoard)
            #print("after processBlackCircles")
            #puzzleBoard.print()
            changed = changed or self.__processWhiteCircles(puzzleBoard)
            #print("after processWhiteCircles")
            #puzzleBoard.print()
            changed = changed or self.__addLines(puzzleBoard)
            #print("after addLines")
            #puzzleBoard.print()
            changed = changed or self.__processSubPaths(puzzleBoard)
            # print("Changed is = ", changed)
            changed = changed or self.__identifyProblems(puzzleBoard)

            if not (changed) and orphanedRegionCheckEnabled:
                # After all other processing has completed, we will check for
                # problems caused by orphaned regions.
                changed = self.__orphanedRegionDetector.checkForOrphanedRegions(puzzleBoard)

    def __updateBlockedPathways(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

        if (lineCount == 2):
            if not(l):
                puzzleBoard.markBlockedLeft(rowNum, colNum)

            if not(r):
                puzzleBoard.markBlockedRight(rowNum, colNum)

            if not(u):
                puzzleBoard.markBlockedUp(rowNum, colNum)

            if not(d):
                puzzleBoard.markBlockedDown(rowNum, colNum)
        elif (lineCount > 2):
            raise MasyuSolverException("Cell has more than 2 lines", (rowNum, colNum))

    def drawLineLeftWrapper(self, puzzleBoard, rowNum, colNum):
        self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)

    # The following methods are "wrappers" for the four "drawLine" methods of the PuzzleBoard
    # class.  They not only draw the line, but they then immediately call the method which
    # blocks paths affected by the line we just drew
    def __drawLineLeftWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineLeftWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):
            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)
            # Check if the subpath ended in the cell to our left
            if ((endingCol == (colNum - 1)) and (endingRow == rowNum)):
                # totalNumCircles = self.__getNumberOfCircles(puzzleBoard)
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException ("lineLeftWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        # Call the PuzzleBoard drawLine method
        puzzleBoard.drawLineLeft(rowNum, colNum)

        # Now make sure that any paths needing to be blocked get blocked
        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, rowNum, (colNum - 1))

    def __drawLineRightWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineRightWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):
            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)
            # Check if the subpath ended in the cell to our right
            if ((endingCol == (colNum + 1)) and (endingRow == rowNum)):
                # totalNumCircles = self.__getNumberOfCircles(puzzleBoard)
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException("lineRightWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        # Call the PuzzleBoard drawLine method
        puzzleBoard.drawLineRight(rowNum, colNum)

        # Now make sure that any paths needing to be blocked get blocked
        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, rowNum, (colNum + 1))

    def __drawLineUpWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineUpWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):
            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)
            # Check if the subpath ended in the cell above
            if ((endingCol == colNum) and (endingRow == (rowNum - 1))):
                # totalNumCircles = self.__getNumberOfCircles(puzzleBoard)
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException("lineUpWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        # Call the PuzzleBoard drawLine method
        puzzleBoard.drawLineUp(rowNum, colNum)

        # Now make sure that any paths needing to be blocked get blocked
        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, (rowNum - 1), colNum)

    def __drawLineDownWrapper(self, puzzleBoard, rowNum, colNum):
        lineCount, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
        if (lineCount >= 2):
            raise MasyuSolverException("lineDownWrapper: too many lines in cell", (rowNum, colNum))

        elif (lineCount == 1):
            endingRow, endingCol, numCirclesVisited = self.__processSubPath(puzzleBoard, rowNum, colNum)
            # Check if the subpath ended in the cell below
            if ((endingCol == colNum) and (endingRow == (rowNum + 1))):
                # totalNumCircles = self.__getNumberOfCircles(puzzleBoard)
                totalNumCircles = Utilities.getNumberOfCircles(puzzleBoard)
                if not (numCirclesVisited == totalNumCircles):
                    raise MasyuSolverException("lineDownWrapper: detected potential closed subloop", (rowNum, colNum))
                else:
                    puzzleBoard.setSolved()

        # Call the PuzzleBoard drawLine method
        puzzleBoard.drawLineDown(rowNum, colNum)

        # Now make sure that any paths needing to be blocked get blocked
        self.__updateBlockedPathways(puzzleBoard, rowNum, colNum)
        self.__updateBlockedPathways(puzzleBoard, (rowNum + 1), colNum)

    # The following is a helper function, which will be called recursively. Each time it is called,
    # it is passed the row and column number for the cell to be looked at, along with the row
    # and column of the previous cell in the line we are following. The count of the number
    # of circles passed through so far is also passed in.
    #
    # Each time this method is called, it will check the next cell to see if the line continues to
    # another cell. If it does, then it recursively calls this function, specifying the next cell.
    # But if it has reached the end of the line, then it returns a tuple, specifying the row and
    # column numbers for the last cell in the line, along with a total of the number of circles
    # the line passed through.
    def __moveToNextCell(self, puzzleBoard, row, col, prevRow, prevCol, numCirclesVisited):
        # If the cell we are in is a circle, then increment numCirclesVisited
        if not (puzzleBoard.isDotAt(row, col)):
            numCirclesVisited += 1

        # If the cell only has 1 line, then we've reached the end of the line
        lineCount, l, r, u, d = puzzleBoard.getLines(row, col)
        # print("processing: ", row, "x", col, "linecount =", lineCount, l, r, u, d)
        if (lineCount == 1):
            # We're done! Return where we stopped and the # of circles visited
            return ((row, col, numCirclesVisited))
        else:
            # We need to figure out which cell to travel to next; we must be careful to
            # not backtrack out the way we came into the cell!

            # If there is a line to the left, we can go there next, unless the previous cell
            # was the one to the left!
            if ((l) and ((prevRow != row) or (prevCol != (col - 1)))):
                return (self.__moveToNextCell(puzzleBoard, row, (col - 1), row, col, numCirclesVisited))

            # If there is a line to the right, we can go there next, unless the previous cell
            # was the one to the right!
            if (r) and ((prevRow != row) or (prevCol != (col + 1))):
                return (self.__moveToNextCell(puzzleBoard, row, (col + 1), row, col, numCirclesVisited))

            # If there is a line up, we can go there next, unless the previous cell
            # was the one above us!
            if (u) and ((prevCol != col) or (prevRow != (row - 1))):
                return (self.__moveToNextCell(puzzleBoard, (row - 1), col, row, col, numCirclesVisited))

            # If there is a line down, we can go there next, unless the previous cell
            # was the one below us!
            if (d) and ((prevCol != col) or (prevRow != (row + 1))):
                return (self.__moveToNextCell(puzzleBoard, (row + 1), col, row, col, numCirclesVisited))

            # We should never drop through to here!!

    # Returns number of circles in the puzzle
    # def __getNumberOfCircles(self, puzzleBoard):
    #     numCircles = 0
    #     numRows, numCols = puzzleBoard.getDimensions()
    #     for rowNum in range(0, numRows):
    #         for colNum in range(0, numCols):
    #             if not (puzzleBoard.isDotAt(rowNum, colNum)):
    #                 numCircles += 1
    #
    #     return (numCircles)

    # Checks if the two cells are next to each other (abut). Returns 'True' if they do; else 'False'.
    def __cellsAbut(self, r1, c1, r2, c2):

        # Is cell 2 to the left of cell 1?
        if ((r2 == r1) and (c2 == (c1 - 1))):
            return (True)

        # Is cell 2 to the right of cell 1?
        if ((r2 == r1) and (c2 == (c1 + 1))):
            return (True)

        # Is cell 2 above cell 1?
        if ((r2 == (r1 - 1)) and (c2 == c1)):
            return (True)

        # Is cell 2 below cell 1?
        if ((r2 == (r1 + 1)) and (c2 == c1)):
            return (True)

        # Cells do not abut
        return (False)

    # Draw a line between the two cells, if it isn't already there. Return 'True' if the line
    # was drawn (a change was made), and 'False' if not.
    def __drawLineBetweenCells(self, puzzleBoard, r1, c1, r2, c2):
        # Is cell 2 to the left of cell 1?
        if ((r2 == r1) and (c2 == (c1 - 1))):
            if not (puzzleBoard.hasLineLeft(r1, c1)):
                # Draw the line
                # puzzleBoard.drawLineLeft(r1, c1)
                self.__drawLineLeftWrapper(puzzleBoard, r1, c1)
                return (True)
            else:
                 # Line is already there!
                return (False)

        # Is cell 2 to the right of cell 1?
        if ((r2 == r1) and (c2 == (c1 + 1))):
            if not (puzzleBoard.hasLineRight(r1, c1)):
                # Draw the line
                # puzzleBoard.drawLineRight(r1, c1)
                self.__drawLineRightWrapper(puzzleBoard, r1, c1)
                return (True)
            else:
                # Line is already there!
                return (False)

        # Is cell 2 above cell 1?
        if ((r2 == (r1 - 1)) and (c2 == c1)):
            if not (puzzleBoard.hasLineUp(r1, c1)):
                # Draw the line
                # puzzleBoard.drawLineUp(r1, c1)
                self.__drawLineUpWrapper(puzzleBoard, r1, c1)
                return (True)
            else:
                # Line is already there!
                return (False)

        # Is cell 2 below cell 1?
        if ((r2 == (r1 + 1)) and (c2 == c1)):
            if not (puzzleBoard.hasLineDown(r1, c1)):
                # Draw the line
                # puzzleBoard.drawLineDown(r1, c1)
                self.__drawLineDownWrapper(puzzleBoard, r1, c1)
                return (True)
            else:
                # Line is already there!
                return (False)

        # No line was drawn
        return (False)

    # Block the path between the two cells, if it isn't already blocked. Return 'True' if the block
    # was added (a change was made), and 'False' if not.
    def __blockPathBetweenCells(self, puzzleBoard, r1, c1, r2, c2):
        # Is cell 2 to the left of cell 1?
        if ((r2 == r1) and (c2 == (c1 - 1))):
            if not (puzzleBoard.isBlockedLeft(r1, c1)):
                # Block the path
                # print("Blocking Left ", r1, c1, r2, c2)
                puzzleBoard.markBlockedLeft(r1, c1)
                return (True)
            else:
                # Path is already blocked
                return (False)

        # Is cell 2 to the right of cell 1?
        if ((r2 == r1) and (c2 == (c1 + 1))):
            if not (puzzleBoard.isBlockedRight(r1, c1)):
                # Block the path
                # print("Blocking Right ", r1, c1, r2, c2)
                puzzleBoard.markBlockedRight(r1, c1)
                return (True)
            else:
                # Path is already blocked
                return (False)

        # Is cell 2 above cell 1?
        if ((r2 == (r1 - 1)) and (c2 == c1)):
            if not (puzzleBoard.isBlockedUp(r1, c1)):
                # Block the path
                # print("Blocking Up ", r1, c1, r2, c2)
                puzzleBoard.markBlockedUp(r1, c1)
                return (True)
            else:
                # Path is already blocked
                return (False)

        # Is cell 2 below cell 1?
        if ((r2 == (r1 + 1)) and (c2 == c1)):
            if not (puzzleBoard.isBlockedDown(r1, c1)):
                # Block the path
                # print("Blocking Down ", r1, c1, r2, c2)
                puzzleBoard.markBlockedDown(r1, c1)
                return (True)
            else:
                # Path is already blocked
                return (False)

        # Path was already blocked
        return (False)

    def __numConsecutiveWhiteCirclesInCol(self, puzzleBoard, rowNum, colNum):
        # This function starts at the specified cell, and determines the number of consecutive white
        # circle cells which are in the specified column. If there is a white circle in the cell above
        # this one, then iAmFirst will be set to 'false', and count will be set to -1; that is because
        # this cell is not the first in the line of white circle cells. Otherwise, if this is the first
        # white circle cell in the vertical line, then iAmFirst will be set to 'true', and count will be
        # set to the number of consecutive white circle cells in the line.

        if ((rowNum == 0) or (rowNum > 0) and not (puzzleBoard.isWhiteCircleAt((rowNum - 1), colNum))):
            # The starting cell is the first one
            count = 0
            numRows, numCols = puzzleBoard.getDimensions()
            for i in range(rowNum, numRows):
                if (puzzleBoard.isWhiteCircleAt(i, colNum)):
                    count += 1
                else:
                    return (True, count)

            return (True, count)
        else:
            return (False, -1)

    def __numConsecutiveWhiteCirclesInRow(self, puzzleBoard, rowNum, colNum):
        # This function starts at the specified cell, and determines the number of consecutive white
        # circle cells which are in the specified row. If there is a white circle in the cell to the left
        # of this one, then iAmFirst will be set to 'false', and count will be set to -1; that is because
        # this cell is not the first in the line of white circle cells. Otherwise, if this is the first
        # white circle cell in the horizontal line, then iAmFirst will be set to 'true', and count will
        # be set to the number of consecutive white circle cells in the line.

        if ((colNum == 0) or (colNum > 0) and not (puzzleBoard.isWhiteCircleAt(rowNum, (colNum - 1)))):
            # The starting cell is the first one
            count = 0
            numRows, numCols = puzzleBoard.getDimensions()
            for i in range(colNum, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum, i)):
                    count += 1
                else:
                    return (True, count)

            return (True, count)
        else:
            return (False, -1)

    def __processSpecialCases(self, puzzleBoard):
        # Case 9
        # Look for 3 or more consecutive white circles.
        # If found: block the pathway between each white circle, and at both ends.
        # Algorithm assumes we process the Puzzle Board going L->R, T->B order.
        # Because of this, if a white circle is found which isn't the first in line of a
        # group of white circles, then it is skipped because it was already processed
        # when the first white circle was encountered.

        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if(puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    # Check for vertical line of white circles
                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInCol(puzzleBoard, rowNum, colNum)

                    # Skip if not the first in the series
                    if (iAmFirst and (count > 2)):
                        if ((colNum > 0) and (colNum < (numCols - 1))):
                            # Block paths between and at ends of white circle cells
                            # If any place we plan to “block” already has a line, then
                            # the puzzle is invalid (or our code has a bug!)

                            # Block above starting cell
                            if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line up in special case 9", (rowNum, colNum))
                            elif not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                                    changesMade = True


                            # Now block the bottom pathway of each of the consecutive cells
                            for i in range(rowNum, (rowNum + count)):
                                if (puzzleBoard.hasLineDown(i, colNum)):
                                    raise MasyuSolverException("Unexpected line down in special case 9", (i, colNum))
                                elif not (puzzleBoard.isBlockedDown(i, colNum)):
                                    puzzleBoard.markBlockedDown(i, colNum)
                                    changesMade = True

                        else:
                            raise MasyuSolverException("Invalid white circle location in special case 9-1", (rowNum, colNum))

                    # else:
                        # Not first, or less than 3 in a row
                        # Do Nothing

                    # Check for horizontal line of white circles
                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInRow(puzzleBoard, rowNum, colNum)

                    # Skip if not the first in the series
                    if (iAmFirst and (count > 2)):
                        if ((rowNum > 0) and (rowNum < (numRows - 1))):
                            # Block paths between and at ends of white circle cells
                            # If any place we plan to “block” already has a line, then
                            # the puzzle is invalid (or our code has a bug!)

                            # Block to the left of the starting cell
                            if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line left in special case 9", (rowNum, colNum))
                            elif not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True

                            # Now block the right pathway of each of the consecutive cells
                            for i in range(colNum, (colNum + count)):
                                if (puzzleBoard.hasLineRight(rowNum, i)):
                                    raise MasyuSolverException("Unexpected line right in special case 9", (rowNum, i))
                                elif not (puzzleBoard.isBlockedRight(rowNum, i)):
                                    puzzleBoard.markBlockedRight(rowNum, i)
                                    changesMade = True

                        else:
                            raise MasyuSolverException("Invalid white circle location in special case 9-2", (rowNum, colNum))

                    # else:
                    # Not first, or less than 3 in a row
                    # Do Nothing

                    # Handle case 14
                    # Check for 2 vertically adjacent white circles
                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInCol(puzzleBoard, rowNum, colNum)

                    # Skip if not the first in the series
                    if (iAmFirst and (count == 2)):
                        # Case 14-1
                        if (rowNum > 1):
                            if (puzzleBoard.hasLineUp((rowNum - 1), colNum)):
                                if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in Case 14-1", (rowNum, colNum))
                                elif (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                                    raise MasyuSolverException("Unexpected line down in Case 14-1", ((rowNum + 1), colNum))
                                else:
                                    if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                        puzzleBoard.markBlockedUp(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedDown((rowNum + 1), colNum)):
                                        puzzleBoard.markBlockedDown((rowNum + 1), colNum)
                                        changesMade = True

                        # Case 14-3
                        if (rowNum < (numRows - 3)):
                            if (puzzleBoard.hasLineDown((rowNum + 2), colNum)):
                                if (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                                    raise MasyuSolverException("Unexpected line down in Case 14-3", ((rowNum + 1), colNum))
                                elif (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in Case 14-3",(rowNum, colNum))
                                else:
                                    if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                        puzzleBoard.markBlockedUp(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedDown((rowNum + 1), colNum)):
                                        puzzleBoard.markBlockedDown((rowNum + 1), colNum)
                                        changesMade = True

                    # Check for horizontal line of white circles
                    iAmFirst, count = self.__numConsecutiveWhiteCirclesInRow(puzzleBoard, rowNum, colNum)
                    # Skip if not the first in the series
                    if (iAmFirst and (count == 2)):
                        # Case 14-2
                        if (colNum > 1):
                            if (puzzleBoard.hasLineLeft(rowNum, (colNum - 1))):
                                if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in Case 14-2",(rowNum, colNum))
                                elif (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                                    raise MasyuSolverException("Unexpected line right in Case 14-2",(rowNum, (colNum + 1)))
                                else:
                                    if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                        puzzleBoard.markBlockedLeft(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedRight(rowNum, (colNum + 1))):
                                        puzzleBoard.markBlockedRight(rowNum, (colNum + 1))
                                        changesMade = True

                        # Case 14-4
                        if (colNum < (numCols - 3)):
                            if (puzzleBoard.hasLineRight(rowNum, (colNum + 2))):
                                if (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                                    raise MasyuSolverException("Unexpected line right in Case 14-4",(rowNum, (colNum + 1)))
                                elif (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in Case 14-4",(rowNum, colNum))
                                else:
                                    if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                        puzzleBoard.markBlockedLeft(rowNum, colNum)
                                        changesMade = True
                                    if not (puzzleBoard.isBlockedRight(rowNum, (colNum + 1))):
                                        puzzleBoard.markBlockedRight(rowNum, (colNum + 1))
                                        changesMade = True

                    # Handle case 15-1
                    if (1 < rowNum < (numRows - 2)):
                        if ((puzzleBoard.hasLineUp((rowNum - 1), colNum)) and (puzzleBoard.hasLineDown((rowNum + 1), colNum))):
                            if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line up in Case 15-1", (rowNum, colNum))
                            if (puzzleBoard.hasLineDown(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line down in Case 15-1", (rowNum, colNum))
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True

                    # Handle case 15-2
                    if (1 < colNum < (numCols - 2)):
                        if ((puzzleBoard.hasLineLeft(rowNum, (colNum - 1)) and (puzzleBoard.hasLineRight(rowNum, (colNum + 1))))):
                            if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line left in Case 15-2",(rowNum, colNum))
                            if (puzzleBoard.hasLineRight(rowNum, colNum)):
                                raise MasyuSolverException("Unexpected line right in Case 15-2",(rowNum, colNum))
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True

                elif (puzzleBoard.isBlackCircleAt(rowNum, colNum)):

                    # Case 10-1: both white circles are below the black circle
                    if ((colNum > 0) and (colNum < (numCols - 1)) and (rowNum < (numRows - 1))):
                       if (puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum - 1)) and
                               puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum + 1))):
                            if (rowNum > 1):
                                if (puzzleBoard.hasLineDown(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line down in case 10-1", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                    puzzleBoard.markBlockedDown(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-1", (rowNum, colNum))

                    # Case 10-2: Both white circles are to the left of the black circle
                    if ((rowNum > 0) and (rowNum < (numRows - 1)) and (colNum > 0)):
                       if (puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum - 1)) and
                               puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum - 1))):
                            if (colNum < (numCols - 2)):
                                if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in case 10-2", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                    puzzleBoard.markBlockedLeft(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-2", (rowNum, colNum))

                    # Case 10-3: Both white circles are above the black circle
                    if ((colNum > 0) and (colNum < (numCols - 1)) and (rowNum > 0)):
                       if (puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum - 1)) and
                               puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum + 1))):
                            if (rowNum < (numRows - 2)):
                                if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in case 10-3", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-3", (rowNum, colNum))

                    # Case 10-4: Both white circles are to the right of the black circle
                    if ((rowNum > 0) and (rowNum < (numRows - 1)) and (colNum < (numCols - 1))):
                        if (puzzleBoard.isWhiteCircleAt((rowNum - 1), (colNum + 1)) and
                                puzzleBoard.isWhiteCircleAt((rowNum + 1), (colNum + 1))):
                            if (colNum > 1):
                                if (puzzleBoard.hasLineRight(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line right in case 10-4", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                    puzzleBoard.markBlockedRight(rowNum, colNum)
                                    changesMade = True
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 10-4", (rowNum, colNum))

                    # Case 12-1: Both white circles are below the black circle
                    if (rowNum < (numRows - 3)):
                        if ((puzzleBoard.isDotAt((rowNum + 1), colNum)) and
                                puzzleBoard.isWhiteCircleAt((rowNum + 2), colNum) and
                                puzzleBoard.isWhiteCircleAt((rowNum + 3), colNum)):
                            if (rowNum > 1):
                                if (puzzleBoard.hasLineDown(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line down in case 12-1", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                    puzzleBoard.markBlockedDown(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-1", (rowNum, colNum))

                    # Case 12-2: Both white circles are to the left of the black circle
                    if (colNum > 2):
                        if ((puzzleBoard.isDotAt(rowNum, (colNum - 1)) and
                                puzzleBoard.isWhiteCircleAt(rowNum, (colNum - 2)) and
                                puzzleBoard.isWhiteCircleAt(rowNum, (colNum - 3)))):
                            if (colNum < (numCols - 2)):
                                if (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line left in case 12-2", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                    puzzleBoard.markBlockedLeft(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-2", (rowNum, colNum))

                    # Case 12-3: Both white circles are above the black circle
                    if (rowNum > 2):
                        if ((puzzleBoard.isDotAt((rowNum - 1), colNum)) and
                                puzzleBoard.isWhiteCircleAt((rowNum - 2), colNum) and
                                puzzleBoard.isWhiteCircleAt((rowNum - 3), colNum)):
                            if (rowNum < (numRows - 2)):
                                if (puzzleBoard.hasLineUp(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line up in case 12-3", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-3", (rowNum, colNum))

                    # Case 12-4: Both white circles are to the right of the black circle
                    if (colNum < (numCols - 3)):
                        if ((puzzleBoard.isDotAt(rowNum, (colNum + 1)) and
                             puzzleBoard.isWhiteCircleAt(rowNum, (colNum + 2)) and
                             puzzleBoard.isWhiteCircleAt(rowNum, (colNum + 3)))):
                            if (colNum > 1):
                                if (puzzleBoard.hasLineRight(rowNum, colNum)):
                                    raise MasyuSolverException("Unexpected line right in case 12-4", (rowNum, colNum))
                                elif not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                    puzzleBoard.markBlockedRight(rowNum, colNum)
                            else:
                                raise MasyuSolverException("Illegal black circle location in case 12-4", (rowNum, colNum))

    def __findPathwaysToBlock(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        # Case 1
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)
                    # Case 1a
                    if (lineLeft and lineRight and (colNum > 1)):
                        if (puzzleBoard.hasLineLeft(rowNum, (colNum - 1))):
                            if not (puzzleBoard.isBlockedRight(rowNum, (colNum + 1))):
                                puzzleBoard.markBlockedRight(rowNum, (colNum + 1))
                                changesMade = True

                    # Case 1b
                    if (lineLeft and lineRight and (colNum < (numCols - 2))):
                        if (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                             if not (puzzleBoard.isBlockedLeft(rowNum, (colNum - 1))):
                                 puzzleBoard.markBlockedLeft(rowNum, (colNum - 1))
                                 changesMade = True

                    # Case 1c
                    if (lineUp and lineDown and (rowNum > 1)):
                        if (puzzleBoard.hasLineUp((rowNum - 1), colNum)):
                            if not (puzzleBoard.isBlockedDown((rowNum + 1), colNum)):
                                puzzleBoard.markBlockedDown((rowNum + 1), colNum)
                                changesMade = True

                    # Case 1d
                    if (lineUp and lineDown and (rowNum < (numRows - 2))):
                        if (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                            if not (puzzleBoard.isBlockedUp((rowNum - 1), colNum)):
                                puzzleBoard.markBlockedUp((rowNum - 1), colNum)
                                changesMade = True

        # Case 2
        for rowNum in range(0, numRows):
             for colNum in range(0, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)
                    # Case 2a
                    if (lineUp or lineDown):
                        if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                            puzzleBoard.markBlockedLeft(rowNum, colNum)
                            changesMade = True

                        if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                            puzzleBoard.markBlockedRight(rowNum, colNum)
                            changesMade = True

                    # Case 2b
                    if (lineLeft or lineRight):
                        if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                            puzzleBoard.markBlockedUp(rowNum, colNum)
                            changesMade = True

                        if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                            puzzleBoard.markBlockedDown(rowNum, colNum)
                            changesMade = True

        # Case 3
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                # Any cell which has two lines can have the other two pathways blocked.
                numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)
                if (puzzleBoard.isDotAt(rowNum, colNum)):
                    if (numLines == 2):
                        if not (lineLeft):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                        if not (lineUp):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                        if not (lineRight):
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                        if not (lineDown):
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True

                elif (puzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    if (numLines == 2):
                        if (lineLeft and lineRight):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True
                        elif (lineUp and lineDown):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                        else:
                            raise MasyuSolverException("Invalid turn in white circle", (rowNum, colNum))

                elif (puzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    if (numLines == 2):
                        if (lineLeft and lineUp):
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True
                        elif (lineUp and lineRight):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True
                        elif (lineRight and lineDown):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                        elif (lineLeft and lineDown):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True
                        else:
                            raise MasyuSolverException("Missing turn in black circle", (rowNum, colNum))

        # Case 4
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    # Checking cell to the left
                    if (colNum > 0):
                        if (puzzleBoard.hasLineUp(rowNum, (colNum - 1)) or puzzleBoard.hasLineDown(rowNum, (colNum - 1))):
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                                changesMade = True

                    # Checking cell to the right
                    if (colNum < (numCols - 1)):
                        if (puzzleBoard.hasLineUp(rowNum, (colNum + 1)) or puzzleBoard.hasLineDown(rowNum, (colNum + 1))):
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                puzzleBoard.markBlockedRight(rowNum, colNum)
                                changesMade = True

                    # Checking cell above
                    if (rowNum > 0):
                        if (puzzleBoard.hasLineLeft((rowNum - 1), colNum) or puzzleBoard.hasLineRight((rowNum - 1), colNum)):
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                                changesMade = True

                    # Checking cell below
                    if (rowNum < (numRows - 1)):
                        if (puzzleBoard.hasLineLeft((rowNum + 1), colNum) or puzzleBoard.hasLineRight((rowNum + 1), colNum)):
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                                changesMade = True

        return (changesMade)


    def __processDeadendPaths(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        deadEndFound = True
        while deadEndFound:
            deadEndFound = False
            for rowNum in range(0, numRows):
                for colNum in range(0, numCols):
                    if (puzzleBoard.isDotAt(rowNum, colNum)):
                        count, l, r, u, d = puzzleBoard.getBlockedPaths(rowNum, colNum)
                        if (count == 3):
                            numLines, lineLeft, lineRight, lineUp, lineDown = puzzleBoard.getLines(rowNum, colNum)
                            if (numLines != 0):
                                raise MasyuSolverException("Unexpected line at dead-end", (rowNum, colNum))
                            else:
                                if not (l):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedLeft(rowNum, colNum)
                                    changesMade = True
                                elif not (r):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedRight(rowNum, colNum)
                                    changesMade = True
                                elif not (u):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                                    changesMade = True
                                elif not (d):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedDown(rowNum, colNum)
                                    changesMade = True

            changesMade = changesMade | deadEndFound

        return (changesMade)

    def __processBlackCircles(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    if (puzzleBoard.isBlockedLeft(rowNum, colNum) or
                        ((colNum > 0) and puzzleBoard.isBlockedLeft(rowNum, (colNum - 1)))):
                        if (colNum > (numCols - 3)) or \
                                puzzleBoard.isBlockedRight(rowNum, colNum) or \
                                puzzleBoard.isBlockedRight(rowNum, (colNum + 1)):
                            raise MasyuSolverException("Black Circle Blocked L/R", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineRight(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineRight(rowNum, colNum)
                                self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                                changesMade = True
                                # puzzleBoard.drawLineRight(rowNum, (colNum + 1))
                                self.__drawLineRightWrapper(puzzleBoard, rowNum, (colNum + 1))

                    if (puzzleBoard.isBlockedRight(rowNum, colNum) or
                        ((colNum < (numCols - 1) and puzzleBoard.isBlockedRight(rowNum, (colNum + 1))))):
                        if ((colNum < 2) or \
                                puzzleBoard.isBlockedLeft(rowNum, colNum) or \
                                puzzleBoard.isBlockedLeft(rowNum, (colNum - 1))):
                            raise MasyuSolverException("Black Circle Blocked L/R - 2", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineLeft(rowNum, colNum)
                                self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineLeft(rowNum, (colNum - 1))):
                                changesMade = True
                                # puzzleBoard.drawLineLeft(rowNum, (colNum - 1))
                                self.__drawLineLeftWrapper(puzzleBoard, rowNum, (colNum - 1))

                    if (puzzleBoard.isBlockedUp(rowNum, colNum) or
                        ((rowNum > 0) and puzzleBoard.isBlockedUp((rowNum - 1), colNum))):
                        if (rowNum > (numRows - 3)) or \
                                puzzleBoard.isBlockedDown(rowNum, colNum) or \
                                puzzleBoard.isBlockedDown((rowNum + 1), colNum):
                            raise MasyuSolverException("Black Circle Blocked U/D", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineDown(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineDown(rowNum, colNum)
                                self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineDown((rowNum + 1), colNum)
                                self.__drawLineDownWrapper(puzzleBoard, (rowNum + 1), colNum)

                    if (puzzleBoard.isBlockedDown(rowNum, colNum) or
                        ((rowNum < (numRows - 1)) and puzzleBoard.isBlockedDown((rowNum + 1), colNum))):
                        if (rowNum < 2) or \
                                puzzleBoard.isBlockedUp(rowNum, colNum) or \
                                puzzleBoard.isBlockedUp((rowNum - 1), colNum):
                            raise MasyuSolverException("Black Circle Blocked U/D - 2", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineUp(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineUp(rowNum, colNum)
                                self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineUp((rowNum - 1), colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineUp((rowNum - 1), colNum)
                                self.__drawLineUpWrapper(puzzleBoard, (rowNum - 1), colNum)

                    # After drawing lines, we need to see if anything can be blocked for the
                    # cell being processed, or for the adjacent cell (since the line for a black
                    # circle extends for 2 cells!
                    count, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

                    # If line to the left from c[r,c], then block to the right of c[r,c] and also block up
                    # and down for c[r, c-1] (the cell to the left, where the first line segment goes)
                    if (l):
                        if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedRight(rowNum, colNum)

                        if not (puzzleBoard.isBlockedUp(rowNum, (colNum - 1))):
                            changesMade = True
                            puzzleBoard.markBlockedUp(rowNum, (colNum - 1))

                        if not (puzzleBoard.isBlockedDown(rowNum, (colNum - 1))):
                            changesMade = True
                            puzzleBoard.markBlockedDown(rowNum, (colNum - 1))

                    # If line to the right from c[r,c], then block to the left of c[r,c] and also block up
                    # and down for c[r, c+1] (the cell to the right, where the first line segment goes)
                    if (r):
                        if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedLeft(rowNum, colNum)
                        #if (colNum == (numCols - 1)):
                        #    puzzleBoard.print()
                        #    print ("bad stuff")
                        if not (puzzleBoard.isBlockedUp(rowNum, (colNum + 1))):
                            changesMade = True
                            puzzleBoard.markBlockedUp(rowNum, (colNum + 1))

                        if not (puzzleBoard.isBlockedDown(rowNum, (colNum + 1))):
                            changesMade = True
                            puzzleBoard.markBlockedDown(rowNum, (colNum + 1))

                    # If line up from c[r,c], then block down from c[r,c] and also block left
                    # and right for c[r-1, c] (the cell above, where the first line segment goes)
                    if (u):
                        if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedDown(rowNum, colNum)
                        if not (puzzleBoard.isBlockedLeft((rowNum - 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedLeft((rowNum - 1), colNum)
                        if not (puzzleBoard.isBlockedRight((rowNum - 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedRight((rowNum - 1), colNum)

                    # If line down from c[r,c], then block up from c[r,c] and also block left
                    # and right for c[r+1, c] (the cell below, where the first line segment goes)
                    if (d):
                        if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedUp(rowNum, colNum)
                        if not (puzzleBoard.isBlockedLeft((rowNum + 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedLeft((rowNum + 1), colNum)
                        if not (puzzleBoard.isBlockedRight((rowNum + 1), colNum)):
                            changesMade = True
                            puzzleBoard.markBlockedRight((rowNum + 1), colNum)

        return (changesMade)

    def __processWhiteCircles(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isWhiteCircleAt(rowNum,colNum)):

                    if (puzzleBoard.isBlockedUp(rowNum,colNum) or puzzleBoard.isBlockedDown(rowNum,colNum)):
                        if ((colNum == 0) or (colNum == (numCols-1))):
                            # print("White circle cannot be in first or last column", (rowNum, colNum))
                            raise MasyuSolverException("White circle cannot be in first or last column",
                                                       (rowNum, colNum))
                        elif (puzzleBoard.isBlockedLeft(rowNum, colNum) or
                              puzzleBoard.isBlockedRight(rowNum, colNum)):
                            # print("White circle blocked L/R", (rowNum, colNum))
                            raise MasyuSolverException("White circle blocked L/R", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineLeft(rowNum, colNum)
                                self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineRight(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineRight(rowNum, colNum)
                                self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                    elif (puzzleBoard.isBlockedLeft(rowNum,colNum) or puzzleBoard.isBlockedRight(rowNum,colNum)):
                        if ((rowNum == 0) or (rowNum == (numRows-1))):
                            # print("White circle cannot be in first or last row", (rowNum, colNum))
                            raise MasyuSolverException("White circle cannot be in first or last row",
                                                       (rowNum, colNum))
                        elif (puzzleBoard.isBlockedUp(rowNum, colNum) or
                              puzzleBoard.isBlockedDown(rowNum, colNum)):
                            # print("White circle blocked U/D,", (rowNum, colNum))
                            raise MasyuSolverException("White circle blocked U/D", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineUp(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineUp(rowNum, colNum)
                                self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.hasLineDown(rowNum, colNum)):
                                changesMade = True
                                # puzzleBoard.drawLineDown(rowNum, colNum)
                                self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedRight(rowNum, colNum)

                    count, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
                    if (count == 1):
                        if (l):
                            # puzzleBoard.drawLineRight(rowNum, colNum)
                            self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True
                        elif (r):
                            # puzzleBoard.drawLineLeft(rowNum, colNum)
                            self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True
                        elif (u):
                            # puzzleBoard.drawLineDown(rowNum, colNum)
                            self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True
                        elif (d):
                            # puzzleBoard.drawLineUp(rowNum, colNum)
                            self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                            changesMade = True

        return (changesMade)

    def __addLines(self, puzzleBoard):
        # We are looking for cells which have a single line entering in, but doesn't yet have a
        # second line exiting the cell. In this case, if 2 of the paths are blocked, then we know
        # that the remaining line must continue out through the only unblocked path.

        # Most of this work is already handled (I think) by the code dealing with black
        # and white circles! What isn't handled is dealing with “dots”. So that is what
        # we need to process here!
        numRows, numCols = puzzleBoard.getDimensions()
        changesMade = False
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (puzzleBoard.isDotAt(rowNum, colNum)):
                    numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
                    numOpenPaths, openL, openR, openU, openD = puzzleBoard.getOpenPaths(rowNum, colNum)
                    # if ((rowNum == 3) and (colNum == 4)):
                    #     print("NumLines = ", numLines, l, r, u, d)
                    #     print("OpenPaths= ", numOpenPaths, openL, openR, openU, openD)
                    #     print("Up = ", puzzleBoard.isOpenUp(rowNum, colNum))
                    #     print("Down = ", puzzleBoard.isOpenDown(rowNum, colNum))
                    #     print("Left = ", puzzleBoard.isOpenLeft(rowNum, colNum))
                    #     print("Right = ", puzzleBoard.isOpenRight(rowNum, colNum))
                    #     numOpenPathsX, openLX, openRX, openUX, openDX = puzzleBoard.getOpenPaths((rowNum - 1), colNum)
                    #     print("OpenPaths= ", numOpenPathsX, openLX, openRX, openUX, openDX)
                    #     print("Up = ", puzzleBoard.isOpenUp((rowNum - 1), colNum))
                    #     print("Down = ", puzzleBoard.isOpenDown((rowNum - 1), colNum))
                    #     print("Left = ", puzzleBoard.isOpenLeft((rowNum - 1), colNum))
                    #     print("Right = ", puzzleBoard.isOpenRight((rowNum - 1), colNum))
                    #     puzzleBoard.print()


                    # If there is only 1 line into the cell and only 1 open path, then we know
                    # that the line must extend out through the open path .. it is the only
                    # available option!
                    if ((numLines == 1) and (numOpenPaths == 1)):
                        changesMade = True
                        if (openL):
                            # puzzleBoard.drawLineLeft(rowNum, colNum)
                            self.__drawLineLeftWrapper(puzzleBoard, rowNum, colNum)
                        elif (openR):
                            # puzzleBoard.drawLineRight(rowNum, colNum)
                            self.__drawLineRightWrapper(puzzleBoard, rowNum, colNum)
                        elif (openU):
                            # puzzleBoard.drawLineUp(rowNum, colNum)
                            self.__drawLineUpWrapper(puzzleBoard, rowNum, colNum)
                        else:
                            # puzzleBoard.drawLineDown(rowNum, colNum)
                            self.__drawLineDownWrapper(puzzleBoard, rowNum, colNum)

        return (changesMade)

    # Follow the subpath starting at the specified rowNum/colNum.
    # Returns a tuple: (endingRowNum, endingColNum, numCirclesVisited)

    def __processSubPath(self, puzzleBoard, rowNum, colNum):
        numCirclesVisited = 0

        numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)

        puzzleBoard.setCellProcessedFlag(rowNum, colNum)

        if not (puzzleBoard.isDotAt(rowNum, colNum)):
            # Started in a circle; so increment our circle count
            numCirclesVisited += 1

        # Follow the line to the next cell
        if (l):
            # Proceed to the cell to the left (cell(rowNum, colNum-1))
            # print("starting:", rowNum, "x", colNum)
            result = self.__moveToNextCell(puzzleBoard, rowNum, colNum - 1, rowNum, colNum, numCirclesVisited)

        elif (r):
            # Proceed to the cell to the right (cell(rowNum, colNum+1))
            # print("starting:", rowNum, "x", colNum)
            result = self.__moveToNextCell(puzzleBoard, rowNum, colNum + 1, rowNum, colNum, numCirclesVisited)

        elif (u):
            # Proceed to the cell above (cell(rowNum-1, colNum))
            # print("starting:", rowNum, "x", colNum)
            result = self.__moveToNextCell(puzzleBoard, rowNum - 1, colNum, rowNum, colNum, numCirclesVisited)

        else:
            # Proceed to the cell below (cell(rowNum+1, colNum))
            # print("starting:", rowNum, "x", colNum)
            result = self.__moveToNextCell(puzzleBoard, rowNum + 1, colNum, rowNum, colNum, numCirclesVisited)

        endRowNum, endColNum, na = result
        puzzleBoard.setCellProcessedFlag(endRowNum, endColNum)

        # Once the recursion has completed (because we reached the end
        # of the line), the return 'result' is a tuple, telling us the row and column
        # where the line stopped, along with the total count of circles the line
        # passed through.
        return(result)

    # Identify paths which must be blocked, because otherwise they would allow
    # a closed sub-path to be created, which is not allowed. The code also detects
    # if the path being checked actually causes the puzzle to be
    # completed (in which case we draw the line instead of blocking the path)!
    # These 2 cases are distinguished by tracking the number or “circle cells”
    # the path travels through; if it travels through all of the “circle cells”,
    # then the puzzle is complete, so the line segment between the two abutting cells
    # can be drawn and the puzzle marked as 'solved'; otherwise, the path between the
    # abutting cells must be blocked! If the line doesn't start and end in abutting cells,
    # then we don't have to do anything.
    #
    # This method returns a boolean value, indicating whether any changes were made to
    # the puzzle board.
    # We will scan the puzzle board, looking for cells which only have one line (the starting
    # cell). Then we will follow that line, until we come to another cell with only one line
    # (the ending cell).
    def __processSubPaths(self, puzzleBoard):
        changesMade = False
        numRows, numCols = puzzleBoard.getDimensions()
        puzzleBoard.clearAllCellProcessedFlags()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                # Follow the path only if the cell has one line
                numLines, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
                if (numLines == 1):
                    if (puzzleBoard.wasCellProcessed(rowNum, colNum)):
                        # print("skipping path at ", (rowNum, colNum))
                        continue
                    numCirclesVisited = 0
                    startingRow = rowNum
                    startingCol = colNum

                    if not (puzzleBoard.isDotAt(rowNum, colNum)):
                        # Started in a circle; so increment our circle count
                        numCirclesVisited += 1

                    result = self.__processSubPath(puzzleBoard, startingRow, startingCol)

                    # Once the recursion has completed (because we reached the end
                    # of the line), the return 'result' is a tuple, telling us the row and column
                    # where the line stopped, along with the total count of circles the line
                    # passed through.

                    # Check if the starting and ending cells abutted
                    endingRow, endingCol, numCirclesVisited = result
                    if (self.__cellsAbut(startingRow, startingCol, endingRow, endingCol)):
                        # Yes .. they abutted. Now .. if we visited all of the circles,
                        # then we can complete the puzzle by drawing the line between
                        # the 2 cells; otherwise, we need to block the path between
                        # the 2 cells.
                        # numCirclesInPuzzle = self.__getNumberOfCircles(puzzleBoard)
                        numCirclesInPuzzle = Utilities.getNumberOfCircles(puzzleBoard)

                        if (numCirclesInPuzzle == numCirclesVisited):
                            # Puzzle is solved!
                            # Mark the puzzle as solved
                            puzzleBoard.setSolved()

                            # Draw the line connecting the two cells
                            changesMade = changesMade | self.__drawLineBetweenCells(puzzleBoard, startingRow, startingCol, endingRow, endingCol)

                        else:
                            # Path must be blocked!
                            changesMade = changesMade | self.__blockPathBetweenCells(puzzleBoard, startingRow, startingCol, endingRow, endingCol)

                    # else:
                        # The starting and ending cells did not abut, so there is
                        # nothing to do .. no changes need to be made.
                        # return (False)

        return (changesMade)

    def __identifyProblems(self, puzzleBoard):
        #print("__identifyProblems")
        # todo __identifyProblem
        foo = 0
