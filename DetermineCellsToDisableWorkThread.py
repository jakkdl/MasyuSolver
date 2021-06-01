from WorkThread import *
from Cell import *
from MasyuExceptions import *

class DetermineCellsToDisableWorkThread(WorkThread):

    def __init__(self, solver, puzzleBoard, itemType):
        super().__init__(solver, puzzleBoard)

        # Save the item type (black circle or white circle), which
        # will be used by the thread code to determine which cells
        # need to be disabled
        self.__itemType = itemType

    # This is the processing-intensive code which is run in the thread.
    # It attempts to replace each cell in the puzzle (one at a time) with
    # the indicated item (black circle or white circle).  After replacing
    # a cell, it runs the solver; if the solver raises and exception, then
    # the item cannot be placed into that cell .. so it will be disabled.
    # If no exception is raised, then the cell is enabled.
    #
    # This is a slow process, but it does allow the user to visually see
    # which cells the current item type can be placed in.
    def codeToRunInThread(self):
        clonedPuzzleBoard = self.pb.cloneBoardOnly()
        numRows, numCols = clonedPuzzleBoard.getDimensions()

        # Cycle through each cell, and if it isn't already set to the indicated
        # item type, then save the current cell setting, and force it to the
        # indicated item type (black circle or white circle). Then run the
        # solver to see if an exception is thrown .. indicating that the item
        # cannot be placed into that cell, so the cell must be disabled.
        for rowNum in range(0, numRows):
            for colNum in range(0, numCols):
                # Save the current cell type
                if (clonedPuzzleBoard.isBlackCircleAt(rowNum, colNum)):
                    currentCell = Cell.TYPE_BLACK_CIRCLE
                elif (clonedPuzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                    currentCell = Cell.TYPE_WHITE_CIRCLE
                else:
                    currentCell = Cell.TYPE_DOT

                # Set cell to active item
                if (self.__itemType == Cell.TYPE_BLACK_CIRCLE):
                    clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                elif (self.__itemType == Cell.TYPE_WHITE_CIRCLE):
                    clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                else:   # Never should fall through to here!
                    clonedPuzzleBoard.setDotAt(rowNum, colNum)

                try:
                    self.solver.solve(clonedPuzzleBoard)
                except (MasyuSolverException, MasyuOrphanedRegionException) as e:
                    # An exception was raised, so we need to disable the cell
                    self.pb.setCellDisabled(rowNum, colNum)
                else:
                    # Solver was happy .. so enable the cell
                    self.pb.setCellEnabled(rowNum, colNum)
                finally:
                    # Restore the cell back to it's original item
                    if (currentCell == Cell.TYPE_BLACK_CIRCLE):
                        clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                    elif (currentCell == Cell.TYPE_WHITE_CIRCLE):
                        clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                    else:
                        clonedPuzzleBoard.setDotAt(rowNum, colNum)

                    # Clean up, in preparation for the next pass
                    clonedPuzzleBoard.clearSolution()