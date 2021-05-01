import tkinter as tk
from PuzzleBoard import *
from GetPuzzleBoardSizeDialog import *
from CanvasManager import *
from PuzzleStateMachine import *
from MasyuExceptions import *
from Solver import *
from FileIO import *

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

    NO_ITEM = -1
    WHITE_ITEM = 0
    BLACK_ITEM = 1
    DOT_ITEM = 2

    ############################################
    # -------- Start of menu bar handlers ------
    ############################################

    # Placeholder callback for menu items
    def __donothing(self):
        print("do nothing")

    def __fileOpenHandler(self):
        # Call FileIO class to save existing puzzle board and then load a new one
        try:
            status, newPuzzleBoard = FileIO.fileOpen(self.puzzleBoardObject)
            if (status):
                self.registerPuzzleBoard(newPuzzleBoard)

                self.__setWindowTitle(PuzzleStateMachine.getFileName())

                # Force active item to dot
                self.__setActiveItem(self.dotItem)

                # Determine which cells to disable
                self.__determineCellsToDisable()

                try:
                    self.solver.solve(newPuzzleBoard)
                    print("File -> Open successful")
                except Exception as e:
                    # The Loaded Puzzle Board generated an exception
                    numRows, numCols = newPuzzleBoard.getDimensions()
                    newPuzzleBoard = PuzzleBoard(size=(numRows, numCols))
                    PuzzleStateMachine.reset()
                    self.registerPuzzleBoard(newPuzzleBoard)
                    self.__setWindowTitle(None)
                    # Determine which cells to disable
                    self.__determineCellsToDisable()
                    mb.showerror("Invalid Puzzle File", message=e)

                self.puzzleBoardCanvasManager.refreshCanvas()

            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            mb.showerror("Error Saving Puzzle File", message=mfse)
            print("Exception during File -> Save As")
        except MasyuFileOpenException as mfoe:
            mb.showerror("Error Opening Puzzle File", message=mfoe)
            print("Exception during File -> Open")
        except MasyuInvalidPuzzleFileException as mipfe:
            mb.showerror("Invalid Puzzle File", message=mipfe)
            print("Attempted to load invalid puzzle file")

    def __fileExitMenuHandler(self):
        # Call FileIO class to save existing puzzle board then exit
        try:
            status, unusedReturnValue = FileIO.fileExit(self.puzzleBoardObject)
            if(status):
                print("File -> Exit was successful")
                self.mainWindow.destroy()
            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            mb.showerror("Error Saving Puzzle File", message=mfse)
            print("Exception during File -> Exit")

    def __fileSaveAsMenuHandler(self):
        # Call FileIO class to save existing puzzle board but allow the user to specify a new filename
        try:
            status, unusedReturnValue = FileIO.fileSaveAs(self.puzzleBoardObject)
            if(status):
                print("File -> Save As successful")
                self.__setWindowTitle(PuzzleStateMachine.getFileName())
            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            mb.showerror("Error Saving Puzzle File", message=mfse)
            print("Exception during File -> Save As")

    def __fileSaveMenuHandler(self):
        # Call FileIO class to save existing puzzle board using the name already associated
        # with this puzzle board
        try:
            status, unusedReturnValue = FileIO.fileSave(self.puzzleBoardObject)
            if(status):
                print("File -> Save successful")
                self.__setWindowTitle(PuzzleStateMachine.getFileName())
            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            mb.showerror("Error Saving Puzzle File", message=mfse)
            print("Exception during File -> Save")

    def __fileNewMenuHandler(self):
        try:
            status, unusedReturnValue = FileIO.fileNew(self.puzzleBoardObject)
            if not (status):
                return

        except MasyuFileSaveException as mfse:
            mb.showerror("Error Saving Puzzle File", message=mfse)
            print("Exception during File -> Save")
            return

        resizeResults = GetPuzzleBoardSizeDialog(self.mainWindow)
        rowVal, colVal = resizeResults.showDialog(self.numRows, self.numCols)
        print ("new puzzle size:", rowVal, colVal)
        if ((rowVal != -1) and (colVal != -1)):
            # Reset the State Machine
            PuzzleStateMachine.reset()
            self.__setWindowTitle(None)

            pb = PuzzleBoard(size=(rowVal, colVal))
            self.registerPuzzleBoard(pb)

            # Determine which cells to disable
            self.__determineCellsToDisable()

            # Force a refresh
            self.puzzleBoardCanvasManager.refreshCanvas()

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

    def __setWindowTitle(self, puzzleName):
        if (puzzleName == None):
            puzzleName = "<unnamed>"

        self.mainWindow.title("Maysu: " + puzzleName)

    # Event handler for processing <button-1> events in one of the items;
    # causes the selected item to becoome the active item.
    def __itemSelectionHandler(self, event):

        item = event.widget

        if (item != self.selectedItem):
            self.__setActiveItem(item)

            # Determine which cells to disable
            self.__determineCellsToDisable()

            self.puzzleBoardCanvasManager.refreshCanvas()


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

    def __showProgressCallback(self):
        self.puzzleBoardCanvasManager.setShowProgress(self.showProgressVar.get())

    def __showBlockedPathsCallback(self):
        self.puzzleBoardCanvasManager.setShowBlockedPaths(self.showBlockedPathsVar.get())

    def __showDisabledCellsCallback(self):
        if not (self.showDisabledCellsVar.get()):
            for rowNum in range(0, self.numRows):
                for colNum in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)

        self.puzzleBoardCanvasManager.setShowDisabledCells(self.showDisabledCellsVar.get())


    def __determineCellsToDisable(self):
        if not (self.showDisabledCellsVar.get()):
            for rowNum in range(0, self.numRows):
                for colNum in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
            return

        if (self.selectedItem == self.dotItem):
            for rowNum in range (0, self.numRows):
                for colNum in range (0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)

        else:
            clonedPuzzleBoard = self.puzzleBoardObject.cloneBoardOnly()

            for rowNum in range (0, self.numRows):
                for colNum in range (0, self.numCols):
                    # Save the current cell type
                    if (clonedPuzzleBoard.isBlackCircleAt(rowNum, colNum)):
                        currentCell = Cell.TYPE_BLACK_CIRCLE
                    elif (clonedPuzzleBoard.isWhiteCircleAt(rowNum, colNum)):
                        currentCell = Cell.TYPE_WHITE_CIRCLE
                    else:
                        currentCell = Cell.TYPE_DOT

                    # Set cell to active item
                    if (self.selectedItem == self.blackItem):
                        clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                    elif (self.selectedItem == self.whiteItem):
                        clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                    else:
                        clonedPuzzleBoard.setDotAt(rowNum, colNum)

                    try:
                        self.solver.solve(clonedPuzzleBoard)
                    except MasyuSolverException as e:
                        self.puzzleBoardObject.setCellDisabled(rowNum, colNum)
                    else:
                        self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
                    finally:
                        if (currentCell == Cell.TYPE_BLACK_CIRCLE):
                            clonedPuzzleBoard.setBlackCircleAt(rowNum, colNum)
                        elif (currentCell == Cell.TYPE_WHITE_CIRCLE):
                            clonedPuzzleBoard.setWhiteCircleAt(rowNum, colNum)
                        else:
                            clonedPuzzleBoard.setDotAt(rowNum, colNum)

                        clonedPuzzleBoard.clearSolution()



    ###############################################
    # ------ End of private helper functions ------
    ###############################################

    #############################################
    # ------ Start of public class methods ------
    #############################################

    def __cellSelectionCallBack(self, rowNum, colNum):
        if not (self.puzzleBoardObject.isCellEnabled(rowNum, colNum)):
            self.mainWindow.bell()
        else:
            if ((self.selectedItem == self.blackItem) and
                    (self.puzzleBoardObject.isBlackCircleAt(rowNum, colNum))):
                return

            if ((self.selectedItem == self.whiteItem) and
                    (self.puzzleBoardObject.isWhiteCircleAt(rowNum, colNum))):
                return

            if ((self.selectedItem == self.dotItem) and
                    (self.puzzleBoardObject.isDotAt(rowNum, colNum))):
                return

            self.puzzleBoardObject.clearSolution()
            for r in range(0, self.numRows):
                for c in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(r, c)
                    self.puzzleBoardObject.setCellValid(r, c)

            # Set cell to active item
            if (self.selectedItem == self.blackItem):
                self.puzzleBoardObject.setBlackCircleAt(rowNum, colNum)
            elif (self.selectedItem == self.whiteItem):
                self.puzzleBoardObject.setWhiteCircleAt(rowNum, colNum)
            else:
                self.puzzleBoardObject.setDotAt(rowNum, colNum)

            # Set puzzleBoard state to unsolved
            self.puzzleBoardObject.setUnsolved()

            # Need to update the solver state (see state diagram)
            PuzzleStateMachine.puzzleChanged()

            # Determine which cells to disable
            self.__determineCellsToDisable()

            #call the solver
            try:
                self.solver.solve(self.puzzleBoardObject)
            except MasyuSolverException as e:
                # puzzle is invalid
                self.puzzleBoardObject.setCellInvalid(rowNum, colNum)
                self.puzzleBoardObject.setInvalid()

            self.puzzleBoardCanvasManager.refreshCanvas()

            # TODO: check for solved puzzle


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
        self.__setWindowTitle(None)

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.__fileExitMenuHandler)

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

        self.showProgressVar = tk.BooleanVar()
        self.showProgressVar.set(True)
        showProgressCheckbox = tk.Checkbutton(checkboxFrame, text="Show progress", variable=self.showProgressVar,
                                              bg=checkboxColor, command=self.__showProgressCallback)
        showProgressCheckbox.pack(side=tk.TOP, anchor=tk.W)

        self.showBlockedPathsVar = tk.BooleanVar()
        self.showBlockedPathsVar.set(True)
        showBlockedPaths = tk.Checkbutton(checkboxFrame, text="Show blocked paths", variable=self.showBlockedPathsVar,
                                          bg=checkboxColor, command=self.__showBlockedPathsCallback)
        showBlockedPaths.pack(side=tk.BOTTOM, anchor=tk.W)

        self.showDisabledCellsVar = tk.BooleanVar()
        self.showDisabledCellsVar.set(True)
        showDisabledCells = tk.Checkbutton(checkboxFrame, text="Smart placement mode", variable=self.showDisabledCellsVar,
                                           bg=checkboxColor, command=self.__showDisabledCellsCallback)
        showDisabledCells.pack(side=tk.BOTTOM, anchor=tk.W)

        # Create the menubar components
        menubar = tk.Menu(self.mainWindow)

        # Create the 'File' menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.__fileNewMenuHandler)
        filemenu.add_command(label="Open", command=self.__fileOpenHandler)
        filemenu.add_command(label="Save", command=self.__fileSaveMenuHandler)
        filemenu.add_command(label="Save As ..", command=self.__fileSaveAsMenuHandler)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.__fileExitMenuHandler)
        menubar.add_cascade(label="File", menu=filemenu)

        # Create the 'Help' menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Instructions", command=self.__donothing)
        helpmenu.add_command(label="About", command=self.__donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # Attach the menubar to the main application window
        self.mainWindow.config(menu=menubar)

        # Create the puzzle board canvas manager, and register our puzzle board canvas
        self.puzzleBoardCanvasManager = CanvasManager(self.puzzleBoardCanvas, self.showProgressVar.get(),
                                                      self.showBlockedPathsVar.get(), self.showDisabledCellsVar.get())
        self.puzzleBoardCanvasManager.registerCellSelectionCallback(self.__cellSelectionCallBack)

        self.solver = Solver()


    # Method for displaying the solver UI window
    def showWindow(self):
        self.mainWindow.mainloop()

    # Method for assigning a PuzzleBoard object to this UI window.
    # The Puzzle Board canvas will be set to the necessary size,
    # the cells will be created, along with all of the other pieces
    # making up a cell: circles, dots, lines and blocks
    def registerPuzzleBoard(self, puzzleBoard):
        self.puzzleBoardCanvasManager.registerPuzzleBoard(puzzleBoard)
        self.puzzleBoardObject = puzzleBoard
        self.numRows, self.numCols = puzzleBoard.getDimensions()

    # ------ End of public class methods ------

# ------ Begin test code ------
if __name__ == '__main__':
    basePath = os.path.expandvars('$APPDATA')
    appBasePath = os.path.join(basePath, 'MasyuSolver')
    settingsFileName = 'masyuSolverConfig.ini'
    ConfigMgr.loadSettings(appBasePath, settingsFileName)
    uiWindow = SolverUIWindow()
    pb = PuzzleBoard()
    runTests = False
    if (runTests):
        pb.setBlackCircleAt(1, 1)
        pb.setWhiteCircleAt(4, 2)
        pb.markBlockedUp(1, 1)
        pb.markBlockedLeft(1, 1)
        pb.markBlockedUp(4, 2)
        pb.drawLineRight(1, 1)
        pb.drawLineRight(1, 2)
        pb.drawLineDown(1, 1)
        pb.drawLineDown(2, 1)
        pb.drawLineLeft(4, 2)
        pb.drawLineRight(4, 2)
        pb.print()
        print(pb.getLines(1, 1))
        print(pb.getBlockedPaths(1, 1))
        print(pb.getOpenPaths(1, 1))
        print("is solved =", pb.isSolved())
        print("is unsolved =", pb.isUnsolved())
        print("is invalid =",pb.isInvalid())
        pb.setSolved()
        print("is solved =", pb.isSolved())
        print("is unsolved =", pb.isUnsolved())
        print("is invalid =", pb.isInvalid())
        pb.setInvalid()
        print("is solved =", pb.isSolved())
        print("is unsolved =", pb.isUnsolved())
        print("is invalid =", pb.isInvalid())
        pb.setUnsolved()
        print("is solved =", pb.isSolved())
        print("is unsolved =", pb.isUnsolved())
        print("is invalid =", pb.isInvalid())

        print("is Enabled =", pb.isCellEnabled(0, 0))
        print("is Valid =", pb.isCellValid(1, 1))
        pb.setCellDisabled(0, 0)
        pb.setCellInvalid(1, 1)
        print("is Enabled =", pb.isCellEnabled(0, 0))
        print("is Valid =", pb.isCellValid(1, 1))
        pb.setCellEnabled(0, 0)
        pb.setCellValid(1, 1)
        print("is Enabled =", pb.isCellEnabled(0, 0))
        print("is Valid =", pb.isCellValid(1, 1))
        # pb.setCellInvalid(0, 0)

    uiWindow.registerPuzzleBoard(pb)
    uiWindow.showWindow()
