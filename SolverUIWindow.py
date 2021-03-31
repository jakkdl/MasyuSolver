import tkinter as tk
from PuzzleBoard import *

class SolverUIWindow():

    # Define class variables here
    STATE_1 = 1     # Unchanged and never saved to a file
    STATE_2 = 2     # Changed and never saved to a file
    STATE_3 = 3     # Unchanged since the last 'open file' operation
    STATE_4 = 4     # Changed since the last 'open file' operation
    STATE_5 = 5     # Unchanged since the last 'save file' operation
    STATE_6 = 6     # Changed since the last 'save file' operation

    NUM_ITEMS = 3                   # Dot, White Circle and Black Circle
    ITEM_PADDING = 3                # Padding around each of the items
    ITEM_HIGHLIGHT_THICKNESS = 2    # Thickness of highlight drawn around active item
    ITEM_WIDTH = 30                 # Width of each item
    ITEM_HEIGHT = 30                # Height of each item
    MENU_ITEM_WHITE_CIRCLE_SIZE = 20      # Size of the white circle item
    MENU_ITEM_BLACK_CIRCLE_SIZE = 20      # Size of the black circle item
    MENU_ITEM_DOT_SIZE = 8               # Size of the dot item
    BOARD_ITEM_WHITE_CIRCLE_SIZE = 10  # Size of the white circle item
    BOARD_ITEM_BLACK_CIRCLE_SIZE = 10  # Size of the black circle item
    BOARD_ITEM_DOT_SIZE = 4  # Size of the dot item
    CELL_LINE_WIDTH = 2
    CELL_BLOCKS_WIDTH = 1
    CELL_BLOCKS_OFFSET = 5

    NO_ITEM = -1
    WHITE_ITEM = 0
    BLACK_ITEM = 1
    DOT_ITEM = 2

    ####################
    # Item tag patterns
    ####################

    # Tags used to identify all items of a given type
    ALL_PATHWAYS_TAG = "allPathways"
    ALL_LINES_TAG = "allLines"
    ALL_BLOCKS_TAG = "allBlocks"
    ALL_WHITE_CIRCLES_TAG = "allWhiteCircles"
    ALL_BLACK_CIRCLES_TAG = "allBlackCircles"
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
    CELL_BOTTOM_LINE_TAG= "_BottomLine"

    ############################################
    # -------- Start of menu bar handlers ------
    ############################################

    # Placeholder callback for menu items
    def __donothing(self):
        print("do nothing")

    # Test modifying the size of the puzzle board
    def __increaseMainCanvasSize(self, canvas):
        numRows = canvas.numRows
        numCols = canvas.numCols

        if (numRows > 7):
            numRows -= 2

        if (numCols < 14):
            numCols += 2

        pb = PuzzleBoard(size=(numRows, numCols))
        pb.print()
        self.registerPuzzleBoard(pb)

    # Test modifying the size of the Puzzle Board
    def __decreaseMainCanvasSize(self, canvas):
        numRows = canvas.numRows
        numCols = canvas.numCols

        if (numRows < 14):
            numRows += 2

        if (numCols > 7):
            numCols -= 2

        pb = PuzzleBoard(size=(numRows, numCols))
        pb.print()
        self.registerPuzzleBoard(pb)

    ############################################
    # -------- End of menu bar handlers --------
    ############################################

    ##########################################################
    # Helper functions associated with the item selection area
    ##########################################################

    # Returns the bounding box (x1, y1, x2, y2) for the indicated item.
    # This represents the "selectable" area for that particular item; it
    # is the area inside of where the highlight will be drawn.
    def __getItemBounds(self):
        x1 = 0
        y1 = 0
        x2 = (self.ITEM_WIDTH + (self.ITEM_HIGHLIGHT_THICKNESS * 2)) - 1
        y2 = (self.ITEM_HEIGHT + (self.ITEM_HIGHLIGHT_THICKNESS * 2)) - 1
        return(x1, y1, x2, y2)

    # Event handler for processing <button-1> events in one of the items;
    # causes the selected item to becoome the active item.
    def __itemSelectionHandler(self, event):

        item = event.widget
        self.__setActiveItem(item)

    # Draw the highlight around the indicated item.
    # If the item is already the selected item, then nothing needs to be done.
    def __setActiveItem(self, item):

        # If this is already the selected item, then do nothing
        if (item == self.selectedItem):
            return

        # Start by removing the highlight around the currently selected item (if there is one)
        if (self.selectedItem != None):
            self.selectedItem.itemconfigure('hilite', state='hidden')

        # Now draw the highlight around the selected item
        self.selectedItem = item
        item.itemconfigure('hilite', state='normal')

    # Create a single item in the item selection area
    def __createItem(self, parent, circleSize, circleColor):

        item = tk.Canvas(master=parent, relief=tk.FLAT, borderwidth=0, highlightthickness=0,
                                   height=(self.ITEM_HEIGHT + (2 * self.ITEM_HIGHLIGHT_THICKNESS)),
                                   width=(self.ITEM_WIDTH + (2 * self.ITEM_HIGHLIGHT_THICKNESS)),
                                   bg=self.itemCanvasColor)
        item.pack(side=tk.TOP)
        item.bind('<Button-1>', lambda event: self.__itemSelectionHandler(event))

        itemX1, itemY1, itemX2, itemY2 = self.__getItemBounds()
        print(itemX1, itemY1, itemX2, itemY2)
        itemCenterX = (itemX2 + 1) / 2
        itemCenterY = (itemY2 + 1) / 2
        x1 = itemCenterX - (circleSize / 2)
        y1 = itemCenterY - (circleSize / 2)
        x2 = x1 + circleSize
        y2 = y1 + circleSize
        item.create_oval(x1, y1, x2, y2, fill=circleColor)

        item.create_line(itemX1, itemY1, itemX2, itemY1,
                         itemX2, itemY2, itemX1, itemY2,
                         itemX1, itemY1, fill='red', tags=('hilite'))

        item.itemconfigure('hilite', state = 'hidden')

        return(item)

    # Create the 3 items in the item selection area
    def __createItems(self, parent):

        self.whiteItem = self.__createItem(parent, self.MENU_ITEM_WHITE_CIRCLE_SIZE, 'white')
        self.blackItem = self.__createItem(parent, self.MENU_ITEM_BLACK_CIRCLE_SIZE, 'black')
        self.dotItem = self.__createItem(parent, self.MENU_ITEM_DOT_SIZE, 'dark grey')

    ######################################################################
    # Helper methods used during the construction of the Game Board canvas
    ######################################################################

    # Event handler for when the cursor enters a cell in the game board
    def __cellEnterHandler(self, event, tag):
        print("Entered cell:", tag)

    # Event handler for when Button-1 is pressed in a cell in the game board
    def __cellSelectedHandler(self, event, tag):
        print("Button press in cell:", tag)

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
                                           state=state, width=0)
        return(item)

    # Using the specified row and column numbers, construct the base tag
    # string used to reference cell[rowNum, colNum]
    def __createBaseItemTag(self, rowNum, colNum):
        return('C' + str(rowNum) + 'x' + str(colNum))

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

    # TODO - must be implemented
    def __setToWhiteCircle(self, rowNum, colNum):
        print("not done")

    # TODO - must be implemented
    def __setToBlackCircle(self, rowNum, colNum):
        print("not done")

    # TODO - must be implemented
    def __setToDot(self, rowNum, colNum):
        print("not done")

    ###############################################
    # ------ End of private helper functions ------
    ###############################################

    #############################################
    # ------ Start of public class methods ------
    #############################################

    # Constructor method
    def __init__(self):
        self.numRows = 0
        self.numCols = 0

        useRealColors = True

        if (useRealColors):
            frame1Color = "light grey"
            self.itemCanvasColor = "grey"
            frame2Color = "light grey"
            puzzleBoardFrameColor = "light grey"
            puzzleBoardCanvasColor = "light grey"
            checkboxFrameColor = "light grey"
            checkboxColor = "light grey"
        else:
            frame1Color = "red"
            self.itemCanvasColor = "grey"
            frame2Color = "green"
            puzzleBoardFrameColor = "dark grey"
            puzzleBoardCanvasColor = "white"
            checkboxFrameColor = "blue"
            checkboxColor = "blue"

        # Initialize some instance variables
        self.state = SolverUIWindow.STATE_1
        self.puzzleBoardObject = None
        self.selectedItem = None

        # Create the top-level application window
        self.mainWindow = tk.Tk()
        self.mainWindow.title("Maysu Puzzle Solver")

        # Create the primary window frame, into which all other UI widgets will be placed
        mainFrame = tk.Frame(master=self.mainWindow)
        mainFrame.pack(expand=True, fill=tk.BOTH)

        # Create a frame for the 'items' selections
        frame1 = tk.Frame(master=mainFrame, height=100, width=30, bg=frame1Color)
        frame1.pack(fill=tk.Y, side=tk.LEFT)

        # Create a frame for holding the item canvas; that way, all of the border and highlight
        # spacing is managed by the frame and not the canvas
        itemFrame = tk.Frame(master=frame1, relief=tk.RAISED, borderwidth=5, bg=self.itemCanvasColor)

        # Create a Canvas, in which we will draw the items (dot, black circle and white circle)
        self.__createItems(itemFrame)
        self.__setActiveItem(self.dotItem)

        itemFrame.pack(fill=tk.X, side=tk.TOP, padx=15, pady=75)

        # Create a frame for holding the Puzzle Board and the checkboxes
        frame2 = tk.Frame(master=mainFrame, height=50, bg=frame2Color)
        frame2.pack(expand=True, fill=tk.BOTH, side=tk.TOP, ipadx=15, ipady=15)

        # Create the frame in which the Puzzle Board canvas will be created.
        # We need the frame because we want it to draw the border around the canvas;
        # otherwise, the canvas size is wrong, because it factors in border widths
        # and highlight thicknesses.
        puzzleBoardFrame = tk.Frame(master=frame2, relief=tk.RAISED, borderwidth=5, bg=puzzleBoardFrameColor)
        puzzleBoardFrame.pack(side=tk.TOP, pady=15)

        # Create the Canvas in which the Puzzle Board will be drawn
        puzzleBoardCanvas = tk.Canvas(master=puzzleBoardFrame, bg=puzzleBoardCanvasColor, height=300, width=300,
                                      highlightthickness=0, relief=tk.FLAT, borderwidth=0)
        puzzleBoardCanvas.pack(side=tk.TOP)
        self.puzzleBoardCanvas = puzzleBoardCanvas

        # Create a frame for holding the checkboxes
        checkboxFrame = tk.Frame(master=frame2, bg=checkboxFrameColor, relief=tk.GROOVE, borderwidth=5)
        checkboxFrame.pack(pady=10)

        showProgress = tk.IntVar()
        showProgressCheckbox = tk.Checkbutton(checkboxFrame, text="Show progress", variable=showProgress,
                                              bg=checkboxColor)
        showProgressCheckbox.pack(side=tk.TOP, anchor=tk.W)

        showBlockedPaths = tk.IntVar()
        showBlockedPaths = tk.Checkbutton(checkboxFrame, text="Show blocked paths", variable=showBlockedPaths,
                                          bg=checkboxColor)
        showBlockedPaths.pack(side=tk.BOTTOM, anchor=tk.W)

        showDisabledCells = tk.IntVar()
        showDisabledCells = tk.Checkbutton(checkboxFrame, text="Show disabled cells", variable=showDisabledCells,
                                           bg=checkboxColor)
        showDisabledCells.pack(side=tk.BOTTOM, anchor=tk.W)

        # Create the menubar components
        menubar = tk.Menu(self.mainWindow)

        # Create the 'File' menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.__donothing)
        filemenu.add_command(label="Open", command=lambda: self.__increaseMainCanvasSize(self))
        filemenu.add_command(label="Save", command=lambda: self.__decreaseMainCanvasSize(self))
        filemenu.add_command(label="Save As ..", command=self.__donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.mainWindow.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Create the 'Help' menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Instructions", command=self.__donothing)
        helpmenu.add_command(label="About", command=self.__donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # Attach the menubar to the main application window
        self.mainWindow.config(menu=menubar)

    # Method for displaying the solver UI window
    def showWindow(self):
        self.mainWindow.mainloop()

    # Method for assigning a PuzzleBoard object to this UI window.
    # The Puzzle Board canvas will be set to the necessary size,
    # the cells will be created, along with all of the other pieces
    # making up a cell: circles, dots, lines and blocks

    # Todo: all of the PuzzleBoardCanvas management code really needs to be extracted
    # into a separate (stand-alone) class, since it will also need to be used by the
    # Failure Anaylsis dialog.
    # Todo: it also needs an option for disabling cell selection, since the canvases
    # will be read-only in the Failure Analysis dialog.  Or .. it needs a way for
    # code to pass in callbacks which get invoked when a cell is selected.
    def registerPuzzleBoard(self, puzzleBoard):
        numRows, numCols = puzzleBoard.getDimensions()

        # If the size of the canvas needs to change, then we will delete all of the
        # existing canvas items, then we will alter the size of the canvas and
        # create new canvas items (lines, blocks, circles, etc).
        #
        # However, if the size of the puzzle board did not change, then all we
        # need to do is reset it back to the initial state, and then set the
        # items to match the specified puzzle board.
        if ((numRows != self.numRows) or (numCols != self.numCols)):
            print ("Resizing canvas: ", numRows, numCols)
            self.numRows = numRows
            self.numCols = numCols

            # Delete any existing items in the canvas
            self.puzzleBoardCanvas.delete('all')

            # Calculate the new canvas height and width
            canvasHeight = numRows * self.ITEM_HEIGHT
            canvasWidth = numCols * self.ITEM_WIDTH
            self.puzzleBoardCanvas.config(width=canvasWidth, height=canvasHeight)
            print(canvasWidth, "x", canvasHeight)

            color = 'red'
            for row in range (0, numRows):
                for col in range (0, numCols):
                    x1 = col * self.ITEM_WIDTH
                    y1 = row * self.ITEM_HEIGHT
                    x2 = x1 + self.ITEM_WIDTH
                    y2 = y1 + self.ITEM_HEIGHT
                    middleX = x1 + (self.ITEM_WIDTH / 2)
                    middleY = y1 + (self.ITEM_HEIGHT / 2)
                    itemTagBase = self.__createBaseItemTag(row, col)
                    print("Creating:", itemTagBase, ":", x1, y1, x2, y2)

                    # We must set "width=0", to turn off the spacing reserved for a highlight border!
                    backgroundTag = itemTagBase + self.CELL_BACKGROUND_TAG
                    tags = (itemTagBase, backgroundTag)
                    item = self.puzzleBoardCanvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color,
                                                            tags=tags, width=0)
                    print("BG: ", self.puzzleBoardCanvas.gettags(item))

                    # For testing purposed, alternate the color of the cells
                    if (color == 'green'):
                        color = 'red'
                    else:
                        color = 'green'

                    # Create the dot for this cell; it is initially visible
                    # The set of tags must be a tuple!
                    dotTag = itemTagBase + self.CELL_DOT_TAG
                    allDotsTag = self.ALL_DOTS_TAG
                    tags = (itemTagBase, allDotsTag, dotTag)
                    item = self.__createBoardItem(x1, y1, self.BOARD_ITEM_DOT_SIZE, 'dark grey', tags, 'normal')
                    print("Dot: ", self.puzzleBoardCanvas.gettags(item))

                    # Create the white circle for this cell; it is initially hidden
                    # The set of tags must be a tuple!
                    whiteCircleTag = itemTagBase + self.CELL_WHITE_CIRCLE_TAG
                    allWhiteCirclesTag = self.ALL_WHITE_CIRCLES_TAG
                    tags=(itemTagBase, allWhiteCirclesTag, whiteCircleTag)
                    item = self.__createBoardItem(x1, y1, self.BOARD_ITEM_WHITE_CIRCLE_SIZE, 'white', tags, 'normal')
                    print("WC: ", self.puzzleBoardCanvas.gettags(item))

                    # Create the black circle for this cell; it is initially hidden
                    # The set of tags must be a tuple!
                    blackCircleTag = itemTagBase + self.CELL_BLACK_CIRCLE_TAG
                    allBlackCirclesTag = self.ALL_BLACK_CIRCLES_TAG
                    tags = (itemTagBase, allBlackCirclesTag, blackCircleTag)
                    item = self.__createBoardItem(x1, y1, self.BOARD_ITEM_BLACK_CIRCLE_SIZE, 'black', tags, 'normal')
                    print("BC: ", self.puzzleBoardCanvas.gettags(item))

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

                    # Add a listener for notifications that the item was "entered" by the mouse
                    self.puzzleBoardCanvas.tag_bind(itemTagBase, '<Enter>',
                                                    lambda event, tag=itemTagBase: self.__cellEnterHandler(event, tag))

                    # Add a listener for notifications that the item was selected by mouse button 1
                    self.puzzleBoardCanvas.tag_bind(itemTagBase, '<Button-1>',
                                                    lambda event, tag=itemTagBase: self.__cellSelectedHandler(event, tag))

        # Start with a clean slate:
        #       Hide all the white circles and black circles
        #       Hide all the lines and blocks
        #       Turn on all of the dots
        self.puzzleBoardCanvas.itemconfigure(self.ALL_BLACK_CIRCLES_TAG, state='hidden')
        self.puzzleBoardCanvas.itemconfigure(self.ALL_WHITE_CIRCLES_TAG, state='hidden')
        self.puzzleBoardCanvas.itemconfigure(self.ALL_PATHWAYS_TAG, state='hidden')
        self.puzzleBoardCanvas.itemconfigure(self.ALL_DOTS_TAG, state='normal')

        # TODO: Set the canvas state to match the PuzzleBoard object state

        # TODO: debug only
        #self.__drawRightLine(2,3)
        #self.__blockRight(1,3)

    # ------ End of public class methods ------

# ------ Begin test code ------
if __name__ == '__main__':
    uiWindow = SolverUIWindow()
    pb = PuzzleBoard(size=(5,5))
    pb.print()
    uiWindow.registerPuzzleBoard(pb)
    uiWindow.showWindow()