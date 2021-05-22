from WorkThread import *
from ProgressDialog import *
from Utilities import *
import time

class BruteForceSolveWorkThread(WorkThread):

    # Define the direction of the line to be drawn
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __init__(self, solver, puzzleBoard):
        super().__init__(solver, puzzleBoard)

        # Initialize the variable holding the brute force results
        self.__bruteForceResults = None
        self.__wasCancelledByUser = False

    # Find the first black circle, which has one line, and determine which
    # line we should try drawing (based on which pathways out of the cell are
    # open).
    def __findBlackCircleWithOneLine(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range (0, numRows):
            for colNum in range (0, numCols):
                if (pb.isBlackCircleAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 1):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u):
                            return((rowNum, colNum, self.UP))
                        if (d):
                            return((rowNum, colNum, self.DOWN))
                        if (l):
                            return((rowNum, colNum, self.LEFT))
                        if (r):
                            return((rowNum, colNum, self.RIGHT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    # Find the first white circle, which has no lines, and determine which
    # line we should try drawing (based on which pathways out of the cell are
    # open).
    def __findWhiteCircleWithNoLines(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (pb.isWhiteCircleAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 0):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u and d):
                            return ((rowNum, colNum, self.UP))
                        if (l and r):
                            return ((rowNum, colNum, self.LEFT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    # Find the first black circle, which has no lines, and determine which
    # line we should try drawing (based on which pathways out of the cell are
    # open).
    def __findBlackCircleWithNoLines(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (pb.isBlackCircleAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 0):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u):
                            return ((rowNum, colNum, self.UP))
                        if (d):
                            return ((rowNum, colNum, self.DOWN))
                        if (l):
                            return ((rowNum, colNum, self.LEFT))
                        if (r):
                            return ((rowNum, colNum, self.RIGHT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    # Find the first dot cell, which has only one line, and determine which
    # line we should try drawing (based on which pathways out of the cell are
    # open).
    def __findDotWithOneLine(self, pb):
        numRows, numCols = pb.getDimensions()
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                if (pb.isDotAt(rowNum, colNum)):
                    numLines, l, r, u, d = pb.getLines(rowNum, colNum)
                    if (numLines == 1):
                        numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
                        if (u):
                            return ((rowNum, colNum, self.UP))
                        if (d):
                            return ((rowNum, colNum, self.DOWN))
                        if (l):
                            return ((rowNum, colNum, self.LEFT))
                        if (r):
                            return ((rowNum, colNum, self.RIGHT))

                        return ((-1, -1, -1))

        return ((-1, -1, -1))

    # If we make a guess, but the solver still can't solve the puzzle, then
    # need to search the puzzle for the next guess.  We look for the next
    # cell to make a guess for, using the following order:
    #
    #   1) Find the first black circle which has only a single line
    #   2) Find the first white circle which has no lines
    #   3) Find the first black circle which has no lines
    #   4) Find the first dot with only a single line
    def __findNextGuess(self, pb):
        rowNum, colNum, direction = self.__findBlackCircleWithOneLine(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        rowNum, colNum, direction = self.__findWhiteCircleWithNoLines(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        rowNum, colNum, direction = self.__findBlackCircleWithNoLines(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        rowNum, colNum, direction = self.__findDotWithOneLine(pb)
        if ((rowNum != -1) and (colNum != -1)):
            return (rowNum, colNum, direction)

        # Unable to solve the puzzle!  No more brute force guess to be made.
        return ((-1,-1,-1))

    # When making a "guess", there is a specific order we attempt to draw a line;
    # the order is based upon the cell type (black circle, white circle, dot):
    #
    #   Black circle: up, down, left right
    #   White circle: up/down, left/right
    #   Dot: up, down, left, right
    #
    # If we attempt to draw a line in a certain direction, and an exception is
    # raised by the solver, then we need to determine which is the next direction
    # to try .. and if there are none left to try, then we need to discard the last
    # guess, and try a different direction for the previous guess.
    def __findNextDirection(self, pb, lastGuess):
        rowNum, colNum, direction = lastGuess
        if (pb.isBlackCircleAt(rowNum, colNum) or pb.isDotAt(rowNum, colNum)):
            numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
            if (direction == self.UP):
                if (d):
                    return ((rowNum, colNum, self.DOWN))
                elif (l):
                    return ((rowNum, colNum, self.LEFT))
                elif (r):
                    return ((rowNum, colNum, self.RIGHT))

            elif (direction == self.DOWN):
                if (l):
                    return ((rowNum, colNum, self.LEFT))
                elif (r):
                    return ((rowNum, colNum, self.RIGHT))

            elif (direction == self.LEFT):
                if (r):
                    return ((rowNum, colNum, self.RIGHT))

        elif (pb.isWhiteCircleAt(rowNum, colNum)):
            numOpen, l, r, u, d = pb.getOpenPaths(rowNum, colNum)
            if (direction == self.UP):
                if (l):
                    return ((rowNum, colNum, self.LEFT))

        # Nothing left to try!
        return ((-1, -1, -1))

    # This method takes the next brute force "guess", and applies it
    # to a cloned copy of the indicated puzzle board.  It returns the
    # modified and cloned puzzle board
    #
    # The 'nextGuess' parameter is a tuple representing the row number
    # and column number of the cell to be modified, along with a direction
    # indicator, telling us which line to draw.
    def __applyNextGuess(self, pb, nextGuess):
        # We want to use the specified puzzle board as the basis to
        # which we apply the "guess", but we want to use a clone, so
        # as to not disturb the original
        pbClone = pb.cloneAll()
        rowNum, colNum, direction = nextGuess

        if (direction == self.UP):
            self.solver.drawLineUpWrapper(pbClone,rowNum, colNum)
        elif (direction == self.DOWN):
            self.solver.drawLineDownWrapper(pbClone, rowNum, colNum)
        elif (direction == self.LEFT):
            self.solver.drawLineLeftWrapper(pbClone, rowNum, colNum)
        elif (direction == self.RIGHT):
            self.solver.drawLineRightWrapper(pbClone, rowNum, colNum)

        return(pbClone)

    __enableShowInterimResults = False

    # This method is used during debugging, to ask the UI thread to
    # display a "progress" window, showing the current state of the
    # puzzle board being brute force solved.
    # It will block the work thread until either the UI thread signals
    # that it should continue with the solving process, or the UI thread
    # indicates that the user has cancelled the brute force operation.
    #
    # This method returns 'False' if the user cancelled the brute force
    # work, or 'True' if the work should continue
    def __showInterimResults(self, pb):
        # If this feature is disabled, then return without doing anything
        if not (self.__enableShowInterimResults):
            return (True)

        self.__bruteForceResults = pb
        self.showResultsEvent.set()

        while ((not self.cancelEvent.isSet()) and (not self.resumeEvent.isSet())):
            time.sleep(0.1)

        if (self.cancelEvent.isSet()):
            self.cancelEvent.clear()
            self.__bruteForceResults = None
            self.__wasCancelledByUser = True
            return (False)
        else:
            self.resumeEvent.clear()
            return (True)

    # Way for determining if the user had cancelled the brute force solving request
    def wasRequestCancelledByUser(self):
        return(self.__wasCancelledByUser)

    # After repetitively applying all of the standard solving rules, if we
    # still have not found a solution to the puzzle, then the user is able
    # to request that we try brute force solving it.
    #
    # Brute force solving involves looking for a cell meeting one of the
    # following criteria:
    #
    #   1) Black circle with only 1 line
    #   2) White circle with 0 lines
    #   3) Black circle with 0 lines
    #   4) Dot with only 1 line
    #
    # Based on where the current line is, and the type of cell, the code
    # makes an educated guess for where to draw the next line.  After adding
    # the line, it calls the solver.
    #
    # If the solver doesn't raise an exception, then the process is repeated.
    # If the puzzle is solved, then we are done.
    # If the solver raises and exception, then the last guess we made was
    # invalid.  We then check if there was a different line we could have
    # drawn in the last cell.  If there was, then we draw that line, and
    # repeat the process of calling the solver.  In the case where there were
    # no more lines to try in the last cell, then we need to drop back to the
    # previous cell to see if there is a different line we could draw there.
    #
    # The code uses two stacks: one to track the guesses made so far, and a
    # second to track the puzzle board object resulting from adding a guess
    # to the previous puzzle board.
    def codeToRunInThread(self):
        # Start out by making a clone of the starting puzzle board, and then pushing
        # it onto the top of the puzzle board clone stack .. the top clone on the
        # stack is always the one to which the next "guess" is applied.
        pbClone = self.pb.cloneAll()
        cloneStack = []
        cloneStack.append(pbClone)
        guessStack = []

        self.__wasCancelledByUser = False

        # Determine the next "guess" to try
        nextGuess = self.__findNextGuess(pbClone)
        rowNum, colNum, direction = nextGuess

        if ((rowNum == -1) and (colNum == -1)):
            # Seems that wasn't even an initial guess for us to try!
            self.__bruteForceResults = None
            return

        # Keep iterating, until we either solve the puzzle, or run out of possible guesses.
        while (True):
            # Save the next guess information on the "guess" stack, and
            # then create a new puzzle board, based on the guess being applied
            # to the top clone on the clone stack.
            guessStack.append(nextGuess)
            pbClone = self.__applyNextGuess(pbClone, nextGuess)
            cloneStack.append(pbClone)

            # Debugging only .. pause while showing the puzzle board with the guess applied
            if (self.__showInterimResults(pbClone) == False):
                return

            try:
                # Check to see if the brute force request was cancelled by the user
                if (self.cancelEvent.isSet()):
                    self.cancelEvent.clear()
                    self.__bruteForceResults = None
                    self.__wasCancelledByUser = True
                    return

                # Let the solver work on the modified puzzle.
                self.solver.solve(pbClone)

                # Debugging only .. pause while showing the puzzle board after the solver has processed it
                if (self.__showInterimResults(pbClone) == False):
                    return

            except Exception as e:
                # If the solver raised an exception, then the last guess caused the puzzle to
                # become invalid.
                rowNum = -1
                colNum = -1

            else:
                # The solver was able to process the puzzle, so check if the puzzle was solved.
                if (Utilities.checkIfPuzzleIsSolved(pbClone)):
                    # Puzzle was solved!
                    self.__bruteForceResults = pbClone
                    return

                # Puzzle wasn't solved; determine next guess to try
                nextGuess = self.__findNextGuess(pbClone)
                rowNum, colNum, direction = nextGuess

            finally:
                # If the last guess caused the solver to raise an exception,
                # then we need to pop the last guess off the stack, and see if
                # there are any other directions in that cell we could have drawn
                # a line.  If so, then we will set up to try the same cell, but a
                # different line direction.  But if there are no other choices
                # remaining for that guess, then we need to backtrack to the
                # previous guess on the stack, and see if we can draw a different
                # line in it.  If we backtrack all the way through the stack without
                # finding another guess to try, then we can't solve the puzzle.
                while ((rowNum == -1) and (colNum == -1)):
                    if (len(guessStack) <= 0):
                        # Stack is now empty .. puzzle can't be solved!
                        self.__bruteForceResults = None
                        return

                    # Pop the top items from both the clone stack and the guess stack.
                    cloneStack.pop()
                    lastGuess = guessStack.pop()
                    if (len(cloneStack) <= 0):
                        self.__bruteForceResults = None
                        return

                    # Revert to using the clone now on the top of the stack, and see if the
                    # previous guess can be used with a different line direction
                    pbClone = cloneStack[-1]
                    nextGuess = self.__findNextDirection(pbClone, lastGuess)
                    rowNum, colNum, direction = nextGuess

    # Returns either 'None' (if a solution wasn't found, or if the user
    # cancelled the request), or a PuzzleBoard object containing the
    # solution to the puzzle.
    def getBruteForceResults(self):
        return(self.__bruteForceResults)

    # The brute force solver allows the user to cancel the request, so we
    # need to let the UI thread know that, so that it will display a
    # "Cancel" button.
    def supportsCancelRequest(self):
        return(True)

    # This is invoked by the main UI thread, each time it "wakes up" to check
    # whether the thread has completed.  It gives us the opportunity to monitor
    # UI requests from the thread code .. for now, it is primarily used during
    # debugging, to allow the thread code to request that the current "work" be
    # displayed in a progress dialog.
    #
    # It returns 'True' if a modal dialog has been displayed by the timer handler,
    # so that the main UI code can then "lift" the UI windows back to the top of
    # the window stack, since they mysteriously jump to the bottom of the window
    # stack after we unpost the 'progress' dialog!
    def timerHandler(self, parentWindow):
        if (self.showResultsEvent.isSet()):
            self.showResultsEvent.clear()
            self.__progressDialog = ProgressDialog(parentWindow, self.__bruteForceResults, self.cancelEvent, self.resumeEvent)
            self.__progressDialog.showDialog()
            return (True)

        # No need to "lift" the UI window
        return(False)