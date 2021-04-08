from MasyuExceptions import *

class Solver():
    def solve(self,puzzleBoard):
        if (puzzleBoard.isUnsolved()):
            changed = True
            while (changed):
                changed = False
                changed = changed or self.__processSpecialCases(puzzleBoard)
                changed = changed or self.__findPathwaysToBlock(puzzleBoard)
                changed = changed or self.__processDeadendPaths(puzzleBoard)
                changed = changed or self.__processBlackCircles(puzzleBoard)
                changed = changed or self.__processWhiteCircles(puzzleBoard)
                changed = changed or self.__addLines(puzzleBoard)
                changed = changed or self.__processSubPaths(puzzleBoard)
                changed = changed or self.__identifyProblems(puzzleBoard)

    def __processSpecialCases(self, puzzleBoard):
        print("processSpecialCases")
        # todo processSpecialCases

    def __findPathwaysToBlock(self, puzzleBoard):
        print("findPathwaysToBlock")
        # todo findPathwaysToBlock

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
                                elif not (r):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedRight(rowNum, colNum)
                                elif not (u):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedUp(rowNum, colNum)
                                elif not (d):
                                    deadEndFound = True
                                    puzzleBoard.markBlockedDown(rowNum, colNum)

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
        return (changesMade)

    def __addLines(self, puzzleBoard):
        print("__addLines")
        # todo __addLines

    def __processSubPaths(self, puzzleBoard):
        print("__processSubPaths")
        # todo __processSubPaths

    def __identifyProblems(self, puzzleBoard):
        print("__identifyProblems")
        # todo __identifyProblems
