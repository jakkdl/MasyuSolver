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
        print("__processDeadendPaths")
        # todo __processDeadendPaths

    def __processBlackCircles(self, puzzleBoard):
        print("__processBlackCircles")
        # todo __processBlackCircles

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
