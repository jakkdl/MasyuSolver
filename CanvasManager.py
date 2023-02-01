import re

# The CanvasManager class is responsible for keeping the canvas (which
# draws the puzzle board) in sync with the PuzzleBoard object defining
# the current puzzle board.
class CanvasManager():

    ITEM_WIDTH = 30  # Width of each item
    ITEM_HEIGHT = 30  # Height of each item

    BOARD_ITEM_WHITE_CIRCLE_SIZE = 10  # Size of the white circle item
    BOARD_ITEM_BLACK_CIRCLE_SIZE = 10  # Size of the black circle item
    BOARD_ITEM_GREY_CIRCLE_SIZE = 10  # Size of the black circle item
    BOARD_ITEM_DOT_SIZE = 4  # Size of the dot item

    CELL_LINE_WIDTH = 2
    CELL_BLOCKS_WIDTH = 2
    CELL_BLOCKS_OFFSET = 5

    ####################
    # Item tag patterns
    # We use tags extensively, to make it easier to turn on and off
    # certain visual features of a cell .. or a group of cells.
    ####################

    # Tags used to identify all items of a given type
    ALL_PATHWAYS_TAG = "allPathways"
    ALL_LINES_TAG = "allLines"
    ALL_BLOCKS_TAG = "allBlocks"
    ALL_WHITE_CIRCLES_TAG = "allWhiteCircles"
    ALL_BLACK_CIRCLES_TAG = "allBlackCircles"
    ALL_GREY_CIRCLES_TAG = "allGreyCircles"
    ALL_DOTS_TAG = "allDots"

    # Tag used to identify all items within a given cell
    CELL_ALL_TAG = "_All"

    # Tag used to identify the rectangular cell background item
    CELL_BACKGROUND_TAG = "_Background"

    # Tags used to identify the dot, black circle and white circle
    # items in a cell
    CELL_DOT_TAG = "_Dot"
    CELL_WHITE_CIRCLE_TAG = "_WhiteCircle"
    CELL_BLACK_CIRCLE_TAG = "_BlackCircle"
    CELL_GREY_CIRCLE_TAG = "_GreyCircle"

    # Tags used to identify all items of a specific type within a cell
    CELL_ALL_PATHWAYS_TAG = "_AllPathways"
    CELL_ALL_LINES_TAG = "_AllLines"
    CELL_ALL_BLOCKS_TAG = "_AllBlocks"

    # Tags used to identify the different 'blocked' items in a cell
    CELL_LEFT_BLOCK_TAG = "_LeftBlock"
    CELL_RIGHT_BLOCK_TAG = "_RightBlock"
    CELL_TOP_BLOCK_TAG = "_Top"
    CELL_BOTTOM_BLOCK_TAG = "_Bottom"

    # Tags used to identify the different lines items in a cell
    CELL_LEFT_LINE_TAG = "_LeftLine"
    CELL_RIGHT_LINE_TAG = "_RightLine"
    CELL_TOP_LINE_TAG = "_TopLine"
    CELL_BOTTOM_LINE_TAG = "_BottomLine"

    def __init__(self, canvas, showProgress, showBlockedPaths, showDisabledCells):
        self.puzzleBoardCanvas = canvas
        self.puzzleBoard = None
        self.numRows = 0
        self.numCols = 0
        self.cellSelectionCallback = None
        self.showProgress = showProgress
        self.showBlockedPaths = showBlockedPaths
        self.showDisabledCells = showDisabledCells

    # Controls whether the solution-in-progress is shown
    def setShowProgress(self, isEnabled):
        self.showProgress = isEnabled
        self.__refreshCanvas()

    # Controls whether blocked paths are shown (with an 'X')
    def setShowBlockedPaths(self, isEnabled):
        self.showBlockedPaths = isEnabled
        self.__refreshCanvas()

    # Controls whether disabled cells are drawn differently
    def setShowDisabledCells(self, isEnabled):
        self.showDisabledCells = isEnabled
        self.__refreshCanvas()

    # Method for the application to register a callback, which is
    # invoked each time a cell is selected by the user
    def registerCellSelectionCallback(self, callback):
        self.cellSelectionCallback = callback

    # Method used to register the PuzzleBoard object which will be
    # displayed in the associated Canvas widget
    def registerPuzzleBoard(self, puzzleBoard):
        self.puzzleBoard = puzzleBoard

        numRows, numCols = puzzleBoard.getDimensions()

        # If the size of the canvas needs to change, then we will delete all of the
        # existing canvas items, then we will alter the size of the canvas and
        # create new canvas items (lines, blocks, circles, etc).
        #
        # However, if the size of the puzzle board did not change, then all we
        # need to do is reset it back to the initial state, and then set the
        # items to match the specified puzzle board.
        if ((numRows != self.numRows) or (numCols != self.numCols)):
            # print("Resizing canvas: ", numRows, numCols)
            self.numRows = numRows
            self.numCols = numCols

            # Delete any existing items in the canvas
            self.puzzleBoardCanvas.delete('all')

            # Calculate the new canvas height and width
            canvasHeight = numRows * self.ITEM_HEIGHT
            canvasWidth = numCols * self.ITEM_WIDTH
            self.puzzleBoardCanvas.config(width=canvasWidth, height=canvasHeight)

            self.color = 'Snow2'
            for row in range(0, numRows):
                for col in range(0, numCols):
                    x1 = col * self.ITEM_WIDTH
                    y1 = row * self.ITEM_HEIGHT
                    x2 = x1 + self.ITEM_WIDTH
                    y2 = y1 + self.ITEM_HEIGHT
                    middleX = x1 + (self.ITEM_WIDTH / 2)
                    middleY = y1 + (self.ITEM_HEIGHT / 2)
                    itemTagBase = self.__createBaseItemTag(row, col)

                    # We must set "width=0", to turn off the spacing reserved for a highlight border!
                    backgroundTag = itemTagBase + self.CELL_BACKGROUND_TAG
                    tags = (itemTagBase, backgroundTag)
                    item = self.puzzleBoardCanvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline=self.color,
                                                                   tags=tags, width=0)

                    # Create the dot for this cell; it is initially visible
                    # The set of tags must be a tuple!
                    dotTag = itemTagBase + self.CELL_DOT_TAG
                    allDotsTag = self.ALL_DOTS_TAG
                    tags = (itemTagBase, allDotsTag, dotTag)
                    item = self.__createBoardItem(x1, y1, self.BOARD_ITEM_DOT_SIZE, 'dark grey', tags, 'normal')

                    # Create the left line (which is also part of the right line for the cell on our left)
                    leftLineTag = itemTagBase + self.CELL_LEFT_LINE_TAG
                    allCellLinesTag = itemTagBase + self.CELL_ALL_LINES_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allLinesTag = self.ALL_LINES_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    leftCellRightLineTag = self.__createBaseItemTag(row, col - 1) + self.CELL_RIGHT_LINE_TAG
                    tags = (itemTagBase, allLinesTag, allPathwaysTag, leftLineTag, allCellLinesTag,
                            allCellPathwaysTag, leftCellRightLineTag)
                    item = self.puzzleBoardCanvas.create_line(middleX, middleY, x1, middleY,
                                                              width=self.CELL_LINE_WIDTH,
                                                              tags=tags, state='normal')

                    # Create the right line (which is also part of the left line for the cell on our right)
                    rightLineTag = itemTagBase + self.CELL_RIGHT_LINE_TAG
                    allCellLinesTag = itemTagBase + self.CELL_ALL_LINES_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allLinesTag = self.ALL_LINES_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    rightCellLeftLineTag = self.__createBaseItemTag(row, col + 1) + self.CELL_LEFT_LINE_TAG
                    tags = (itemTagBase, allLinesTag, allPathwaysTag, rightLineTag, allCellLinesTag,
                            allCellPathwaysTag, rightCellLeftLineTag)
                    item = self.puzzleBoardCanvas.create_line(middleX, middleY, x2, middleY,
                                                              width=self.CELL_LINE_WIDTH,
                                                              tags=tags, state='normal')

                    # Create the top line (which is also part of the bottom line for the cell above)
                    topLineTag = itemTagBase + self.CELL_TOP_LINE_TAG
                    allCellLinesTag = itemTagBase + self.CELL_ALL_LINES_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allLinesTag = self.ALL_LINES_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    topCellBottomLineTag = self.__createBaseItemTag(row - 1, col) + self.CELL_BOTTOM_LINE_TAG
                    tags = (itemTagBase, allLinesTag, allPathwaysTag, topLineTag, allCellLinesTag,
                            allCellPathwaysTag, topCellBottomLineTag)
                    item = self.puzzleBoardCanvas.create_line(middleX, middleY, middleX, y1,
                                                              width=self.CELL_LINE_WIDTH,
                                                              tags=tags, state='normal')

                    # Create the bottom line (which is also part of the top line for the cell below)
                    bottomLineTag = itemTagBase + self.CELL_BOTTOM_LINE_TAG
                    allCellLinesTag = itemTagBase + self.CELL_ALL_LINES_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allLinesTag = self.ALL_LINES_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    bottomCellTopLineTag = self.__createBaseItemTag(row + 1, col) + self.CELL_TOP_LINE_TAG
                    tags = (itemTagBase, allLinesTag, allPathwaysTag, bottomLineTag, allCellLinesTag,
                            allCellPathwaysTag, bottomCellTopLineTag)
                    item = self.puzzleBoardCanvas.create_line(middleX, middleY, middleX, y2,
                                                              width=self.CELL_LINE_WIDTH,
                                                              tags=tags, state='normal')

                    # Create the left block (which is also part of the right block for the cell on our left)
                    leftBlockTag = itemTagBase + self.CELL_LEFT_BLOCK_TAG
                    allCellBlocksTag = itemTagBase + self.CELL_ALL_BLOCKS_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allBlocksTag = self.ALL_BLOCKS_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    leftCellRightBlockTag = self.__createBaseItemTag(row, col - 1) + self.CELL_RIGHT_BLOCK_TAG
                    tags = (itemTagBase, allBlocksTag, allPathwaysTag, leftBlockTag, allCellBlocksTag,
                            allCellPathwaysTag, leftCellRightBlockTag)
                    item = self.puzzleBoardCanvas.create_line(x1 + self.CELL_BLOCKS_OFFSET,
                                                              middleY - self.CELL_BLOCKS_OFFSET, x1, middleY,
                                                              x1 + self.CELL_BLOCKS_OFFSET,
                                                              middleY + self.CELL_BLOCKS_OFFSET,
                                                              width=self.CELL_BLOCKS_WIDTH,
                                                              tags=tags, state='normal')

                    # Create the right block (which is also part of the left block for the cell on our right)
                    rightBlockTag = itemTagBase + self.CELL_RIGHT_BLOCK_TAG
                    allCellBlocksTag = itemTagBase + self.CELL_ALL_BLOCKS_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allBlocksTag = self.ALL_BLOCKS_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    rightCellLeftBlockTag = self.__createBaseItemTag(row, col + 1) + self.CELL_LEFT_BLOCK_TAG
                    tags = (itemTagBase, allBlocksTag, allPathwaysTag, rightBlockTag, allCellBlocksTag,
                            allCellPathwaysTag, rightCellLeftBlockTag)
                    item = self.puzzleBoardCanvas.create_line(x2 - self.CELL_BLOCKS_OFFSET,
                                                              middleY - self.CELL_BLOCKS_OFFSET,
                                                              x2, middleY,
                                                              x2 - self.CELL_BLOCKS_OFFSET,
                                                              middleY + self.CELL_BLOCKS_OFFSET,
                                                              width=self.CELL_BLOCKS_WIDTH,
                                                              tags=tags, state='normal')

                    # Create the top block (which is also part of the bottom block for the cell above)
                    topBlockTag = itemTagBase + self.CELL_TOP_BLOCK_TAG
                    allCellBlocksTag = itemTagBase + self.CELL_ALL_BLOCKS_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allBlocksTag = self.ALL_BLOCKS_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    topCellBottomBlockTag = self.__createBaseItemTag(row - 1, col) + self.CELL_BOTTOM_BLOCK_TAG
                    tags = (itemTagBase, allBlocksTag, allPathwaysTag, topBlockTag, allCellBlocksTag,
                            allCellPathwaysTag, topCellBottomBlockTag)
                    item = self.puzzleBoardCanvas.create_line(middleX - self.CELL_BLOCKS_OFFSET,
                                                              y1 + self.CELL_BLOCKS_OFFSET,
                                                              middleX, y1,
                                                              middleX + self.CELL_BLOCKS_OFFSET,
                                                              y1 + self.CELL_BLOCKS_OFFSET,
                                                              width=self.CELL_BLOCKS_WIDTH,
                                                              tags=tags, state='normal')

                    # Create the bottom block (which is also part of the top block for the cell below)
                    bottomBlockTag = itemTagBase + self.CELL_BOTTOM_BLOCK_TAG
                    allCellBlocksTag = itemTagBase + self.CELL_ALL_BLOCKS_TAG
                    allCellPathwaysTag = itemTagBase + self.CELL_ALL_PATHWAYS_TAG
                    allBlocksTag = self.ALL_BLOCKS_TAG
                    allPathwaysTag = self.ALL_PATHWAYS_TAG
                    bottomCellTopBlockTag = self.__createBaseItemTag(row + 1, col) + self.CELL_TOP_BLOCK_TAG
                    tags = (itemTagBase, allBlocksTag, allPathwaysTag, bottomBlockTag, allCellBlocksTag,
                            allCellPathwaysTag, bottomCellTopBlockTag)
                    item = self.puzzleBoardCanvas.create_line(middleX - self.CELL_BLOCKS_OFFSET,
                                                              y2 - self.CELL_BLOCKS_OFFSET,
                                                              middleX, y2,
                                                              middleX + self.CELL_BLOCKS_OFFSET,
                                                              y2 - self.CELL_BLOCKS_OFFSET,
                                                              width=self.CELL_BLOCKS_WIDTH,
                                                              tags=tags, state='normal')

                    # We create the black and white circle *after* the path lines, because we want both
                    # of these items to be higher in the stacking order than the path lines!

                    # Create the black circle for this cell; it is initially hidden
                    # The set of tags must be a tuple!
                    blackCircleTag = itemTagBase + self.CELL_BLACK_CIRCLE_TAG
                    allBlackCirclesTag = self.ALL_BLACK_CIRCLES_TAG
                    tags = (itemTagBase, allBlackCirclesTag, blackCircleTag)
                    item = self.__createBoardItem(x1, y1, self.BOARD_ITEM_BLACK_CIRCLE_SIZE, 'black', tags, 'normal')

                    # Create the white circle for this cell; it is initially hidden
                    # The set of tags must be a tuple!
                    whiteCircleTag = itemTagBase + self.CELL_WHITE_CIRCLE_TAG
                    allWhiteCirclesTag = self.ALL_WHITE_CIRCLES_TAG
                    tags = (itemTagBase, allWhiteCirclesTag, whiteCircleTag)
                    item = self.__createBoardItem(x1, y1, self.BOARD_ITEM_WHITE_CIRCLE_SIZE, 'white', tags, 'normal')
                    
                    greyCircleTag = itemTagBase + self.CELL_GREY_CIRCLE_TAG
                    allGreyCirclesTag = self.ALL_GREY_CIRCLES_TAG
                    tags = (itemTagBase, allGreyCirclesTag, greyCircleTag)
                    item = self.__createBoardItem(x1, y1, self.BOARD_ITEM_GREY_CIRCLE_SIZE, 'red', tags, 'normal')

                    # Add a listener for notifications that the item was "entered" by the mouse
                    self.puzzleBoardCanvas.tag_bind(itemTagBase, '<Enter>',
                                                    lambda event, tag=itemTagBase: self.__cellEnterHandler(event, tag))

                    # Add a listener for notifications that the item was selected by mouse button 1
                    self.puzzleBoardCanvas.tag_bind(itemTagBase, '<Button-1>',
                                                    lambda event, tag=itemTagBase: self.__cellSelectedHandler(event,
                                                                                                              tag))

        # Start with a clean slate:
        #       Hide all the white circles and black circles
        #       Hide all the lines and blocks
        #       Turn on all of the dots
        self.puzzleBoardCanvas.itemconfigure(self.ALL_BLACK_CIRCLES_TAG, state='hidden')
        self.puzzleBoardCanvas.itemconfigure(self.ALL_WHITE_CIRCLES_TAG, state='hidden')
        self.puzzleBoardCanvas.itemconfigure(self.ALL_GREY_CIRCLES_TAG, state='hidden')
        self.puzzleBoardCanvas.itemconfigure(self.ALL_PATHWAYS_TAG, state='hidden')
        self.puzzleBoardCanvas.itemconfigure(self.ALL_DOTS_TAG, state='normal')

        self.__refreshCanvas()

    # Public method for requesting that the Canvas widget be redrawn to match
    # the PuzzleBoard object
    def refreshCanvas(self):
        self.__refreshCanvas()

    # Internal method used to draw the appropriate "item" (black circle, white
    # circle or dat) at the specified cell in the Canvas widget
    def __setCircleAt(self, rowNum, colNum):
        if self.puzzleBoard.isBlackCircleAt(rowNum, colNum):
            self.__setBlackCircleAt(rowNum, colNum)
        elif self.puzzleBoard.isWhiteCircleAt(rowNum, colNum):
            self.__setWhiteCircleAt(rowNum, colNum)
        elif self.puzzleBoard.isGreyCircleAt(rowNum, colNum):
            self.__setGreyCircleAt(rowNum, colNum)
        else:
            self.__setDotAt(rowNum, colNum)

    # Internal method for turning on (visually) the cell components
    # associated with a black circle
    def __setBlackCircleAt(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        blackItemTag = baseTag + self.CELL_BLACK_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(blackItemTag, state='normal')
        whiteItemTag = baseTag + self.CELL_WHITE_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(whiteItemTag, state='hidden')
        greyItemTag = baseTag + self.CELL_GREY_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(greyItemTag, state='hidden')
        dotItemTag = baseTag + self.CELL_DOT_TAG
        self.puzzleBoardCanvas.itemconfigure(dotItemTag, state='hidden')

    # Internal method for turning on (visually) the cell components
    # associated with a white circle
    def __setWhiteCircleAt(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        blackItemTag = baseTag + self.CELL_BLACK_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(blackItemTag, state='hidden')
        whiteItemTag = baseTag + self.CELL_WHITE_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(whiteItemTag, state='normal')
        greyItemTag = baseTag + self.CELL_GREY_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(greyItemTag, state='hidden')
        dotItemTag = baseTag + self.CELL_DOT_TAG
        self.puzzleBoardCanvas.itemconfigure(dotItemTag, state='hidden')

    # Internal method for turning on (visually) the cell components
    # associated with a grey circle
    def __setGreyCircleAt(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        blackItemTag = baseTag + self.CELL_BLACK_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(blackItemTag, state='hidden')
        whiteItemTag = baseTag + self.CELL_WHITE_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(whiteItemTag, state='hidden')
        greyItemTag = baseTag + self.CELL_GREY_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(greyItemTag, state='normal')
        dotItemTag = baseTag + self.CELL_DOT_TAG
        self.puzzleBoardCanvas.itemconfigure(dotItemTag, state='hidden')

    # Internal method for turning on (visually) the cell components
    # associated with a dot
    def __setDotAt(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        blackItemTag = baseTag + self.CELL_BLACK_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(blackItemTag, state='hidden')
        whiteItemTag = baseTag + self.CELL_WHITE_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(whiteItemTag, state='hidden')
        greyItemTag = baseTag + self.CELL_GREY_CIRCLE_TAG
        self.puzzleBoardCanvas.itemconfigure(greyItemTag, state='hidden')
        dotItemTag = baseTag + self.CELL_DOT_TAG
        self.puzzleBoardCanvas.itemconfigure(dotItemTag, state='normal')

    # Internal method for drawing all of the line segments currently defined
    # in the PuzzleBoard object, for the specified cell.
    def __drawLines(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)

        leftLineTag = baseTag + self.CELL_LEFT_LINE_TAG
        if self.puzzleBoard.hasLineLeft(rowNum, colNum):
            state = 'normal'
        else:
            state = 'hidden'
        self.puzzleBoardCanvas.itemconfigure(leftLineTag, state=state)

        rightLineTag = baseTag + self.CELL_RIGHT_LINE_TAG
        if self.puzzleBoard.hasLineRight(rowNum, colNum):
            state = 'normal'
        else:
            state = 'hidden'
        self.puzzleBoardCanvas.itemconfigure(rightLineTag, state=state)

        topLineTag = baseTag + self.CELL_TOP_LINE_TAG
        if self.puzzleBoard.hasLineUp(rowNum, colNum):
            state = 'normal'
        else:
            state = 'hidden'
        self.puzzleBoardCanvas.itemconfigure(topLineTag, state=state)

        bottomLineTag = baseTag + self.CELL_BOTTOM_LINE_TAG
        if self.puzzleBoard.hasLineDown(rowNum, colNum):
            state = 'normal'
        else:
            state = 'hidden'
        self.puzzleBoardCanvas.itemconfigure(bottomLineTag, state=state)

    # Internal method which turns off (hides) all of the line segments for
    # the specified cell.
    def __hideLines(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)

        leftLineTag = baseTag + self.CELL_LEFT_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(leftLineTag, state='hidden')

        rightLineTag = baseTag + self.CELL_RIGHT_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(rightLineTag, state='hidden')

        topLineTag = baseTag + self.CELL_TOP_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(topLineTag, state='hidden')

        bottomLineTag = baseTag + self.CELL_BOTTOM_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(bottomLineTag, state='hidden')

    # Internal method for drawing all of the blocked paths currently defined
    # in the PuzzleBoard object, for the specified cell.
    def __drawBlocks(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)

        if (rowNum != 0):
            topBlockedTag = baseTag + self.CELL_TOP_BLOCK_TAG
            if self.puzzleBoard.isBlockedUp(rowNum, colNum):
                state = 'normal'
            else:
                state = 'hidden'
            self.puzzleBoardCanvas.itemconfigure(topBlockedTag, state=state)

        if (rowNum != self.numRows - 1):
            bottomBlockedTag = baseTag + self.CELL_BOTTOM_BLOCK_TAG
            if self.puzzleBoard.isBlockedDown(rowNum, colNum):
                state = 'normal'
            else:
                state = 'hidden'
            self.puzzleBoardCanvas.itemconfigure(bottomBlockedTag, state=state)

        if (colNum != 0):
            leftBlockedTag = baseTag + self.CELL_LEFT_BLOCK_TAG
            if self.puzzleBoard.isBlockedLeft(rowNum, colNum):
                state = 'normal'
            else:
                state = 'hidden'
            self.puzzleBoardCanvas.itemconfigure(leftBlockedTag, state=state)

        if (colNum != self.numCols - 1):
            rightBlockedTag = baseTag + self.CELL_RIGHT_BLOCK_TAG
            if self.puzzleBoard.isBlockedRight(rowNum, colNum):
                state = 'normal'
            else:
                state = 'hidden'
            self.puzzleBoardCanvas.itemconfigure(rightBlockedTag, state=state)

    # Internal method which turns off (hides) all of the blocked paths for
    # the specified cell.
    def __hideBlocks(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)

        topBlockedTag = baseTag + self.CELL_TOP_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(topBlockedTag, state='hidden')

        bottomBlockedTag = baseTag + self.CELL_BOTTOM_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(bottomBlockedTag, state='hidden')

        leftBlockedTag = baseTag + self.CELL_LEFT_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(leftBlockedTag, state='hidden')

        rightBlockedTag = baseTag + self.CELL_RIGHT_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(rightBlockedTag, state='hidden')

    # Internal method for redrawing the Canvas widget, to match the data
    # in the PuzzleBoard object
    def __refreshCanvas(self):
        for rowNum in range(0, self.numRows):
            for colNum in range(0, self.numCols):
                self.__setCircleAt(rowNum, colNum)
                if (self.showProgress):
                    self.__drawLines(rowNum, colNum)
                else:
                    self.__hideLines(rowNum, colNum)
                if (self.showBlockedPaths):
                    self.__drawBlocks(rowNum, colNum)
                else:
                    self.__hideBlocks(rowNum, colNum)

                # If enabled, then disabled cells are drawn with a stipple
                baseItemTag = self.__createBaseItemTag(rowNum, colNum)
                backgroundItemTag = baseItemTag + self.CELL_BACKGROUND_TAG
                if (self.puzzleBoard.isCellEnabled(rowNum, colNum) or not self.showDisabledCells):
                    self.puzzleBoardCanvas.itemconfigure(backgroundItemTag, stipple="")
                else:
                    self.puzzleBoardCanvas.itemconfigure(backgroundItemTag, stipple="gray25")

                # If enabled, then invalid cells are drawn with a red background
                backgroundItemTag = baseItemTag + self.CELL_BACKGROUND_TAG
                if (self.puzzleBoard.isCellValid(rowNum, colNum)):
                    self.puzzleBoardCanvas.itemconfigure(backgroundItemTag, fill=self.color)
                else:
                    self.puzzleBoardCanvas.itemconfigure(backgroundItemTag, fill="red")


    ######################################################################
    # Helper methods used during the construction of the Game Board canvas
    ######################################################################

    # Event handler for when the cursor enters a cell in the game board.
    # If a cell is disabled, then the cursor is changed to an 'X'
    def __cellEnterHandler(self, event, tag):
        rowNum, colNum = self.__mapTagIdToRowColNums(tag)

        if (self.puzzleBoard.isCellEnabled(rowNum, colNum)):
            self.puzzleBoardCanvas.config(cursor="")
        else:
            self.puzzleBoardCanvas.config(cursor="X_cursor")

    # Event handler for when Button-1 is pressed in a cell in the game board
    def __cellSelectedHandler(self, event, tag):
        rowNum, colNum = self.__mapTagIdToRowColNums(tag)

        # Invoke cell selection callback, if one is supplied
        if (self.cellSelectionCallback != None):
            self.cellSelectionCallback(rowNum, colNum)

    # Based on the parameters passed in, create a circle on the puzzle board canvas.
    # Can be a white circle, a black circle or a dot
    def __createBoardItem(self, x1, y1, circleSize, color, itemTags, state):
        itemX2 = x1 + self.ITEM_WIDTH - 1
        itemY2 = y1 + self.ITEM_HEIGHT - 1
        itemCenterX = x1 + (self.ITEM_WIDTH / 2)
        itemCenterY = y1 + (self.ITEM_HEIGHT / 2)
        circleX1 = itemCenterX - (circleSize / 2)
        circleY1 = itemCenterY - (circleSize / 2)
        circleX2 = circleX1 + circleSize
        circleY2 = circleY1 + circleSize
        item = self.puzzleBoardCanvas.create_oval(circleX1, circleY1, circleX2, circleY2, fill=color, tags=itemTags,
                                                  state=state, width=1, outline='black')
        return (item)

    ##########################
    # Internal helper methods
    ##########################

    # Using the specified row and column numbers, construct the base tag
    # string used to reference cell[rowNum, colNum]
    def __createBaseItemTag(self, rowNum, colNum):
        return ('C' + str(rowNum) + 'x' + str(colNum))

    # Given a tag id for a cell (i.e. "C5x7") use regular expressions to
    # extract out the row and column numbers
    def __mapTagIdToRowColNums(self, tag):
        # Match the pattern: "C<integer>x<integer>"
        regex = r"[C]([0-9]+)[x]([0-9]+)"

        # findall() returns a list of tuples.
        # We want the first list item, whose tuple then
        # contains the 2 numbers extracted from the
        # tag string.
        match = re.findall(regex, tag)
        firstMatch = match[0]
        rowNum, colNum = firstMatch
        return(int(rowNum), int(colNum))

    #################################################
    # Internal methods for enabling canvas items
    #################################################

    def __drawLineRight(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        rightLineTag = baseTag + self.CELL_RIGHT_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(rightLineTag, state='normal')

    def __drawLineLeft(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        leftLineTag = baseTag + self.CELL_LEFT_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(leftLineTag, state='normal')

    def __drawLineUp(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        topLineTag = baseTag + self.CELL_TOP_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(topLineTag, state='normal')

    def __drawLineDown(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        bottomLineTag = baseTag + self.CELL_BOTTOM_LINE_TAG
        self.puzzleBoardCanvas.itemconfigure(bottomLineTag, state='normal')

    def __blockRight(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        rightBlockTag = baseTag + self.CELL_RIGHT_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(rightBlockTag, state='normal')

    def __blockLeft(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        leftBlockTag = baseTag + self.CELL_LEFT_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(leftBlockTag, state='normal')

    def __blockTop(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        topBlockTag = baseTag + self.CELL_TOP_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(topBlockTag, state='normal')

    def __blockBottom(self, rowNum, colNum):
        baseTag = self.__createBaseItemTag(rowNum, colNum)
        bottomBlockTag = baseTag + self.CELL_BOTTOM_BLOCK_TAG
        self.puzzleBoardCanvas.itemconfigure(bottomBlockTag, state='normal')

    ###############################################
    # ------ End of private helper functions ------
    ###############################################
