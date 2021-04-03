class Solver():
    def solve(self,puzzleBoard):
        if (puzzleBoard.isUnsolved()):
            changed = True
            while (changed):
                changed = False
                changed |= self.__processSpecialCases(puzzleBoard)
                changed |= self.__findPathwaysToBlock(puzzleBoard)
                changed |= self.__processDeadendPaths(puzzleBoard)
                changed |= self.__processBlackCircles(puzzleBoard)
                changed |= self.__processWhiteCircles(puzzleBoard)
                changed |= self.__addLines(puzzleBoard)
                changed |= self.__processSubPaths(puzzleBoard)
                changed |= self.__identifyProblems(puzzleBoard)

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

    def __processBlackCircles(self, puzzleBoard):
        print("__processBlackCircles")
        # todo __processBlackCircles

    def __addLines(self, puzzleBoard):
        print("__addLines")
        # todo __addLines

    def __processSubPaths(self, puzzleBoard):
        print("__processSubPaths")
        # todo __processSubPaths

    def __identifyProblems(self, puzzleBoard):
        print("__identifyProblems")
        # todo __identifyProblems
