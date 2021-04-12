from MasyuExceptions import *

class Solver():
    def solve(self,puzzleBoard):
        changed = True
        while (changed and puzzleBoard.isUnsolved()):
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
            changed = changed or self.__identifyProblems(puzzleBoard)

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
                                puzzleBoard.drawLineRight(rowNum, colNum)
                            if not (puzzleBoard.hasLineRight(rowNum, (colNum + 1))):
                                changesMade = True
                                puzzleBoard.drawLineRight(rowNum, (colNum + 1))

                    if (puzzleBoard.isBlockedRight(rowNum, colNum) or
                        ((colNum < (numCols - 1) and puzzleBoard.isBlockedRight(rowNum, (colNum + 1))))):
                        if ((colNum < 2) or \
                                puzzleBoard.isBlockedLeft(rowNum, colNum) or \
                                puzzleBoard.isBlockedLeft(rowNum, (colNum - 1))):
                            raise MasyuSolverException("Black Circle Blocked L/R - 2", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.drawLineLeft(rowNum, colNum)
                            if not (puzzleBoard.hasLineLeft(rowNum, (colNum - 1))):
                                changesMade = True
                                puzzleBoard.drawLineLeft(rowNum, (colNum - 1))

                    if (puzzleBoard.isBlockedUp(rowNum, colNum) or
                        ((rowNum > 0) and puzzleBoard.isBlockedUp((rowNum - 1), colNum))):
                        if (rowNum > (numRows - 3)) or \
                                puzzleBoard.isBlockedDown(rowNum, colNum) or \
                                puzzleBoard.isBlockedDown((rowNum + 1), colNum):
                            raise MasyuSolverException("Black Circle Blocked U/D", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineDown(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.drawLineDown(rowNum, colNum)
                            if not (puzzleBoard.hasLineDown((rowNum + 1), colNum)):
                                changesMade = True
                                puzzleBoard.drawLineDown((rowNum + 1), colNum)

                    if (puzzleBoard.isBlockedDown(rowNum, colNum) or
                        ((rowNum < (numRows - 1)) and puzzleBoard.isBlockedDown((rowNum + 1), colNum))):
                        if (rowNum < 2) or \
                                puzzleBoard.isBlockedUp(rowNum, colNum) or \
                                puzzleBoard.isBlockedUp((rowNum - 1), colNum):
                            raise MasyuSolverException("Black Circle Blocked U/D - 2", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineUp(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.drawLineUp(rowNum, colNum)
                            if not (puzzleBoard.hasLineUp((rowNum - 1), colNum)):
                                changesMade = True
                                puzzleBoard.drawLineUp((rowNum - 1), colNum)

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
                            print("White circle cannot be in first or last column", (rowNum, colNum))
                            raise MasyuSolverException("White circle cannot be in first or last column",
                                                       (rowNum, colNum))
                        elif (puzzleBoard.isBlockedLeft(rowNum, colNum) or
                              puzzleBoard.isBlockedRight(rowNum, colNum)):
                            print("White circle blocked L/R", (rowNum, colNum))
                            raise MasyuSolverException("White circle blocked L/R", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineLeft(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.drawLineLeft(rowNum, colNum)
                            if not (puzzleBoard.hasLineRight(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.drawLineRight(rowNum, colNum)
                            if not (puzzleBoard.isBlockedUp(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedUp(rowNum, colNum)
                            if not (puzzleBoard.isBlockedDown(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedDown(rowNum, colNum)
                    elif (puzzleBoard.isBlockedLeft(rowNum,colNum) or puzzleBoard.isBlockedRight(rowNum,colNum)):
                        if ((rowNum == 0) or (rowNum == (numRows-1))):
                            print("White circle cannot be in first or last row", (rowNum, colNum))
                            raise MasyuSolverException("White circle cannot be in first or last row",
                                                       (rowNum, colNum))
                        elif (puzzleBoard.isBlockedUp(rowNum, colNum) or
                              puzzleBoard.isBlockedDown(rowNum, colNum)):
                            print("White circle blocked U/D,", (rowNum, colNum))
                            raise MasyuSolverException("White circle blocked U/D", (rowNum, colNum))
                        else:
                            if not (puzzleBoard.hasLineUp(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.drawLineUp(rowNum, colNum)
                            if not (puzzleBoard.hasLineDown(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.drawLineDown(rowNum, colNum)
                            if not (puzzleBoard.isBlockedLeft(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedLeft(rowNum, colNum)
                            if not (puzzleBoard.isBlockedRight(rowNum, colNum)):
                                changesMade = True
                                puzzleBoard.markBlockedRight(rowNum, colNum)

                    count, l, r, u, d = puzzleBoard.getLines(rowNum, colNum)
                    if (count == 1):
                        if (l):
                            puzzleBoard.drawLineRight(rowNum, colNum)
                            changesMade = True
                        elif (r):
                            puzzleBoard.drawLineLeft(rowNum, colNum)
                            changesMade = True
                        elif (u):
                            puzzleBoard.drawLineDown(rowNum, colNum)
                            changesMade = True
                        elif (d):
                            puzzleBoard.drawLineUp(rowNum, colNum)
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

                    # If there is only 1 line into the cell and only 1 open path, then we know
                    # that the line must extend out through the open path .. it is the only
                    # available option!
                    if ((numLines == 1) and (numOpenPaths == 1)):
                        changesMade = True
                        if (openL):
                            puzzleBoard.drawLineLeft(rowNum, colNum)
                        elif (openR):
                            puzzleBoard.drawLineRight(rowNum, colNum)
                        elif (openU):
                            puzzleBoard.drawLineUp(rowNum, colNum)
                        else:
                            puzzleBoard.drawLineDown(rowNum, colNum)

        return (changesMade)

    def __processSubPaths(self, puzzleBoard):
        print("__processSubPaths")
        # todo __processSubPaths

    def __identifyProblems(self, puzzleBoard):
        print("__identifyProblems")
        # todo __identifyProblems
