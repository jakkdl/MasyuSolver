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
        print("__processWhiteCircles")
        # todo __processWhiteCircles

    def __addLines(self, puzzleBoard):
        print("__addLines")
        # todo __addLines

    def __processSubPaths(self, puzzleBoard):
        print("__processSubPaths")
        # todo __processSubPaths

    def __identifyProblems(self, puzzleBoard):
        print("__identifyProblems")
        # todo __identifyProblems
