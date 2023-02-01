import tkinter as tk
# from tkinter import messagebox as mb
from PuzzleBoard import *
from GetPuzzleBoardSizeDialog import *
from CanvasManager import *
from PuzzleStateMachine import *
from MasyuExceptions import *
from Solver import *
from FileIO import *
from ErrorDialog import *
from WorkingWindow import *
from ProgressDialog import *
from NoSolutionDialog import *
from BruteForceSolveWorkThread import *
from DetermineCellsToDisableWorkThread import *
import threading

# This is the primary class for the solver; it is the class which should be
# run when you want to create and solve a puzzle

class SolverUIWindow():

    # Define class variables here
    STATE_1 = 1     # Unchanged and never saved to a file
    STATE_2 = 2     # Changed and never saved to a file
    STATE_3 = 3     # Unchanged since the last 'open file' operation
    STATE_4 = 4     # Changed since the last 'open file' operation
    STATE_5 = 5     # Unchanged since the last 'save file' operation
    STATE_6 = 6     # Changed since the last 'save file' operation

    NUM_ITEMS = 4                   # Dot, White Circle and Black Circle
    ITEM_PADDING = 3                # Padding around each of the items
    ITEM_HIGHLIGHT_THICKNESS = 2    # Thickness of highlight drawn around active item
    ITEM_WIDTH = 30                 # Width of each item
    ITEM_HEIGHT = 30                # Height of each item
    MENU_ITEM_WHITE_CIRCLE_SIZE = 20      # Size of the white circle item
    MENU_ITEM_BLACK_CIRCLE_SIZE = 20      # Size of the black circle item
    MENU_ITEM_DOT_SIZE = 8               # Size of the dot item
    MENU_ITEM_GREY_CIRCLE_SIZE = 20

    NO_ITEM = -1
    WHITE_ITEM = 0
    BLACK_ITEM = 1
    GREY_ITEM = 2
    DOT_ITEM = 3

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN =3

    ############################################
    # -------- Start of menu bar handlers ------
    ############################################

    # Placeholder callback for menu items
    def __donothing(self):
        print("do nothing")

    # Open a puzzle board file, validate it and then attempt to solve it
    def __fileOpenHandler(self):
        # Call FileIO class to save existing puzzle board and then load a new one
        try:
            status, newPuzzleBoard = FileIO.fileOpen(self.mainWindow, self.puzzleBoardObject)
            if (status):
                self.registerPuzzleBoard(newPuzzleBoard)

                self.__setWindowTitle(PuzzleStateMachine.getFileName())

                # Force active item to dot
                self.__setActiveItem(self.dotItem)

                # Determine which cells to disable (smart placement mode)
                self.__determineCellsToDisableInThread()

                try:
                    self.solver.solve(newPuzzleBoard)
                    print("File -> Open successful")

                    self.enableSmartPlacement['state'] = tk.NORMAL

                    # Check to see if the puzzle was solved
                    if (Utilities.checkIfPuzzleIsSolved(newPuzzleBoard)):
                        print("puzzle solved")
                        newPuzzleBoard.setSolved()
                        self.bruteForceBtn['state'] = tk.DISABLED
                    else:
                        print("puzzle not solved")
                        newPuzzleBoard.setUnsolved()
                        self.bruteForceBtn['state'] = tk.NORMAL
                except Exception as e:
                    # The Loaded Puzzle Board generated an exception
                    errorDialog = ErrorDialog(self.mainWindow)
                    errorDialog.showDialog("Invalid Puzzle File", str(e))

                    numRows, numCols = newPuzzleBoard.getDimensions()
                    newPuzzleBoard = PuzzleBoard(size=(numRows, numCols))
                    PuzzleStateMachine.reset()
                    self.registerPuzzleBoard(newPuzzleBoard)
                    self.__setWindowTitle(None)

                    # Determine which cells to disable
                    self.__determineCellsToDisableInThread()

                    self.enableSmartPlacement['state'] = tk.NORMAL

                self.puzzleBoardCanvasManager.refreshCanvas()

            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save As")
        except MasyuFileOpenException as mfoe:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Opening Puzzle File", str(mfoe))
            print("Exception during File -> Open")
        except MasyuInvalidPuzzleFileException as mipfe:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Invalid Puzzle File", str(mipfe))
            print("Attempted to load invalid puzzle file")

    # Exit the application; but prompt the user first, if there are unsaved changes
    def __fileExitMenuHandler(self):
        # Call FileIO class to save existing puzzle board then exit
        try:
            status, unusedReturnValue = FileIO.fileExit(self.mainWindow, self.puzzleBoardObject)
            if(status):
                print("File -> Exit was successful")
                self.mainWindow.destroy()
            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Exit")

    # Allow the user to select the file into which the puzzle will be saved.
    # This will then become the filename associated with this puzzle.
    def __fileSaveAsMenuHandler(self):
        # Call FileIO class to save existing puzzle board but allow the user to specify a new filename
        try:
            status, unusedReturnValue = FileIO.fileSaveAs(self.mainWindow, self.puzzleBoardObject)
            if(status):
                print("File -> Save As successful")
                self.__setWindowTitle(PuzzleStateMachine.getFileName())
            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save As")

    # Save the puzzle board in the current file, and if there isn't a current filename
    # associated with the puzzle board, then prompt the user to specify a filename
    def __fileSaveMenuHandler(self):
        # Call FileIO class to save existing puzzle board using the name already associated
        # with this puzzle board
        try:
            status, unusedReturnValue = FileIO.fileSave(self.mainWindow, self.puzzleBoardObject)
            if(status):
                print("File -> Save successful")
                self.__setWindowTitle(PuzzleStateMachine.getFileName())
            # Else the request was cancelled during the save request
        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save")

    # Prompt the user to save any unsaved changes (if there are any), and then prompt
    # them to define the size for the new (and empty) puzzle board
    def __fileNewMenuHandler(self):
        try:
            status, unusedReturnValue = FileIO.fileNew(self.mainWindow, self.puzzleBoardObject)
            if not (status):
                return

        except MasyuFileSaveException as mfse:
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Error Saving Puzzle File", str(mfse))
            print("Exception during File -> Save")
            return

        resizeResults = GetPuzzleBoardSizeDialog(self.mainWindow)
        rowVal, colVal = resizeResults.showDialog(self.numRows, self.numCols)
        print ("new puzzle size:", rowVal, colVal)
        if ((rowVal != -1) and (colVal != -1)):
            # Reset the State Machine
            PuzzleStateMachine.reset()
            self.__setWindowTitle(None)

            self.bruteForceBtn['state'] = tk.DISABLED

            pb = PuzzleBoard(size=(rowVal, colVal))
            self.registerPuzzleBoard(pb)

            # Determine which cells to disable
            self.__determineCellsToDisableInThread()

            # Force a refresh
            self.puzzleBoardCanvasManager.refreshCanvas()

            self.enableSmartPlacement['state'] = tk.NORMAL

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

    # Update the window title to include the puzzle name (if there is one)
    def __setWindowTitle(self, puzzleName):
        if (puzzleName == None):
            puzzleName = "<unnamed>"

        self.mainWindow.title("Maysu: " + puzzleName)

    # Event handler for processing <button-1> events in one of the items;
    # causes the selected item to become the active item.  If smart placement
    # mode is enabled, then it also determines which cells to disable.
    def __itemSelectionHandler(self, event):

        item = event.widget

        if (item != self.selectedItem):
            self.__setActiveItem(item)

            # Determine which cells to disable
            self.__determineCellsToDisableInThread()

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
                         itemX1, itemY1, fill='grey', tags=('hilite'))

        item.itemconfigure('hilite', state = 'hidden')

        return(item)

    # Create the 3 items in the item selection area
    def __createItems(self, parent):

        self.whiteItem = self.__createItem(parent, self.MENU_ITEM_WHITE_CIRCLE_SIZE, 'white')
        self.blackItem = self.__createItem(parent, self.MENU_ITEM_BLACK_CIRCLE_SIZE, 'black')
        self.greyItem = self.__createItem(parent, self.MENU_ITEM_GREY_CIRCLE_SIZE, 'grey')
        self.dotItem = self.__createItem(parent, self.MENU_ITEM_DOT_SIZE, 'dark grey')

    # Callback for the 'show progress' checkbox.
    # Controls whether the solution work is displayed
    def __showProgressCallback(self):
        self.puzzleBoardCanvasManager.setShowProgress(self.showProgressVar.get())

    # Callback for the 'show blocked paths' checkbox.
    # Controls whether the blocked pathways are displayed
    def __showBlockedPathsCallback(self):
        self.puzzleBoardCanvasManager.setShowBlockedPaths(self.showBlockedPathsVar.get())

    # Callback for the 'smart placement' checkbox.
    # Smart placement is slow and time consuming, because it analyzes each cell (based
    # on the currently selected item), to determine which cells must be disabled, because
    # the selected item cannot be placed there.  Disabling 'smart placement' mode speeds
    # things up, but then the user is not given visual feedback that a cell is disabled.
    # Instead, they will be notified when they try to change a cell, that that placement
    # is invalid (and not allowed).  It still prevents them from creating an invalid
    # puzzle!
    def __smartPlacementModeCallback(self):
        if not (self.smartPlacementModeVar.get()):
            for rowNum in range(0, self.numRows):
                for colNum in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
        else:
            self.__determineCellsToDisableInThread()

        self.puzzleBoardCanvasManager.setShowDisabledCells(self.smartPlacementModeVar.get())

    # When 'smart placement' mode is enabled, this will spawn a thread, which does
    # the time-intensive work of analyzing the puzzle to determine which cells to
    # disable; if 'smart placement' mode is disabled, then all cells are enabled.
    def __determineCellsToDisableInThread(self):
        # If smart placement mode is disabled, then simply enable all the cells
        # on the puzzle board
        if not (self.smartPlacementModeVar.get()):
            for rowNum in range(0, self.numRows):
                for colNum in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
            return

        # If the selected item is the 'dot', then there are no restrictions on
        # where it can be placed, so enable all the cells.
        if (self.selectedItem in (self.dotItem, self.greyItem)):
            for rowNum in range (0, self.numRows):
                for colNum in range (0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(rowNum, colNum)
            return

        if (self.selectedItem == self.blackItem):
            selectedItem = Cell.TYPE_BLACK_CIRCLE
        else:
            selectedItem = Cell.TYPE_WHITE_CIRCLE

        # Create a thread for doing the time-intensive work; otherwise,
        # the main UI will appear frozen and unresponsive
        determineCellsToDisable = DetermineCellsToDisableWorkThread(self.solver, self.puzzleBoardObject, selectedItem)

        workingWindow = WorkingWindow(self.mainWindow, determineCellsToDisable)

        determineCellsToDisable.start()
        workingWindow.showWindow()

    # This is the command attached to the 'Solve' button.  It attempts to
    # solve the puzzle using a brute force approach.  The work is done in
    # a different thread, to keep the UI from becoming unresponsive.

    def __tryBruteForceSolvingInThread(self):
        self.bruteForceBtn['state'] = tk.DISABLED

        self.__bruteForceSolver = BruteForceSolveWorkThread(self.solver, self.puzzleBoardObject)

        self.__workingWindow = WorkingWindow(self.mainWindow, self.__bruteForceSolver)

        self.__bruteForceSolver.start()
        self.__workingWindow.showWindow()

        bruteForceResult = self.__bruteForceSolver.getBruteForceResults()
        if (bruteForceResult != None):
            print("puzzle solved")
            bruteForceResult.setSolved()
            self.registerPuzzleBoard(bruteForceResult)

        else:
            print("No solution found")
            self.bruteForceBtn['state'] = tk.NORMAL
            dialog = NoSolutionDialog(self.mainWindow)
            dialog.showDialog()

    ###############################################
    # ------ End of private helper functions ------
    ###############################################

    #############################################
    # ------ Start of public class methods ------
    #############################################

    # Callback invoked when a cell in the puzzle board has been selected.
    # Saves a copy of the current puzzle board (in case the cell change
    # ends up being invalid), before changing the cell and then invoking
    # the solver.
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

            savedPuzzleBoard = self.puzzleBoardObject.cloneAll()

            # Set cell to active item
            if (self.selectedItem == self.blackItem):
                self.puzzleBoardObject.setBlackCircleAt(rowNum, colNum)
            elif (self.selectedItem == self.whiteItem):
                self.puzzleBoardObject.setWhiteCircleAt(rowNum, colNum)
            elif (self.selectedItem == self.greyItem):
                self.puzzleBoardObject.setGreyCircleAt(rowNum, colNum)
            else:
                self.puzzleBoardObject.setDotAt(rowNum, colNum)

            # Force a refresh of the canvas, so the user sees the item
            # placed where they selected
            self.puzzleBoardCanvasManager.refreshCanvas()

            self.puzzleBoardObject.clearSolution()
            for r in range(0, self.numRows):
                for c in range(0, self.numCols):
                    self.puzzleBoardObject.setCellEnabled(r, c)
                    self.puzzleBoardObject.setCellValid(r, c)

            # Determine which cells to disable
            self.__determineCellsToDisableInThread()

            # call the solver
            try:
                self.solver.solve(self.puzzleBoardObject)

                if not (self.smartPlacementModeVar.get()):
                    self.enableSmartPlacement['state'] = tk.DISABLED

                # Need to update the solver state (see state diagram)
                PuzzleStateMachine.puzzleChanged()

                # Check to see if the puzzle was solved
                if (Utilities.checkIfPuzzleIsSolved(self.puzzleBoardObject)):
                    print("puzzle solved")
                    self.puzzleBoardObject.setSolved()
                    self.bruteForceBtn['state'] = tk.DISABLED
                else:
                    print("puzzle not solved")
                    self.puzzleBoardObject.setUnsolved()
                    self.bruteForceBtn['state'] = tk.NORMAL

                self.puzzleBoardCanvasManager.refreshCanvas()

            except MasyuSolverException as e:
                # puzzle is invalid
                self.puzzleBoardObject.setCellInvalid(rowNum, colNum)
                self.puzzleBoardCanvasManager.refreshCanvas()
                errorDialog = ErrorDialog(self.mainWindow)
                errorDialog.showDialog("Invalid Item Placement", "Cannot place item in the selected cell")
                self.registerPuzzleBoard(savedPuzzleBoard)
                raise

    # Constructor method
    def __init__(self):
        self.numRows = 0
        self.numCols = 0

        frame1Color = "light grey"
        self.itemCanvasColor = "teal"
        frame2Color = "light grey"
        puzzleBoardFrameColor = "light grey"
        puzzleBoardCanvasColor = "light grey"
        checkboxFrameColor = "light grey"
        checkboxColor = "light grey"

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

        itemFrame.pack(fill=tk.X, side=tk.TOP, padx=15, pady=(75, 0))

        # Create a frame for holding the Puzzle Board and the checkboxes
        frame2 = tk.Frame(master=mainFrame, height=50, bg=frame2Color)
        frame2.pack(expand=True, fill=tk.BOTH, side=tk.TOP, ipadx=15, ipady=15)

        # Create the frame in which the Puzzle Board canvas will be created.
        # We need the frame because we want it to draw the border around the canvas;
        # otherwise, the canvas size is wrong, because it factors in border widths
        # and highlight thicknesses.
        puzzleBoardFrame = tk.Frame(master=frame2, relief=tk.RAISED, borderwidth=5, bg=puzzleBoardFrameColor)
        puzzleBoardFrame.pack(side=tk.TOP, pady=(15, 0))

        # Create the Canvas in which the Puzzle Board will be drawn
        puzzleBoardCanvas = tk.Canvas(master=puzzleBoardFrame, bg=puzzleBoardCanvasColor, height=300, width=300,
                                      highlightthickness=0, relief=tk.FLAT, borderwidth=0)
        puzzleBoardCanvas.pack(side=tk.TOP)
        self.puzzleBoardCanvas = puzzleBoardCanvas

        # Create a frame for holding the checkboxes
        checkboxFrame = tk.Frame(master=frame2, bg=checkboxFrameColor, relief=tk.GROOVE, borderwidth=5)
        checkboxFrame.pack(pady=(15, 0))

        self.smartPlacementModeVar = tk.BooleanVar()
        self.smartPlacementModeVar.set(True)
        self.enableSmartPlacement = tk.Checkbutton(checkboxFrame, text="Smart placement mode",
                                              variable=self.smartPlacementModeVar,
                                              bg=checkboxColor, command=self.__smartPlacementModeCallback)
        self.enableSmartPlacement.pack(side=tk.BOTTOM, anchor=tk.W)

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

        # Create a frame for holding the push buttons
        buttonFrame = tk.Frame(master=frame2, bg=checkboxFrameColor, relief=tk.FLAT, borderwidth=0)
        buttonFrame.pack(pady=(15, 0))

        self.bruteForceBtn = tk.Button(master=buttonFrame, state=tk.DISABLED, text="Solve", padx=30,
                                       command=self.__tryBruteForceSolvingInThread)
        self.bruteForceBtn.pack()

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
        # helpmenu = tk.Menu(menubar, tearoff=0)
        # helpmenu.add_command(label="Instructions", command=self.__donothing)
        # helpmenu.add_command(label="About", command=self.__donothing)
        # menubar.add_cascade(label="Help", menu=helpmenu)

        # Attach the menubar to the main application window
        self.mainWindow.config(menu=menubar)

        # Create the puzzle board canvas manager, and register our puzzle board canvas
        self.puzzleBoardCanvasManager = CanvasManager(self.puzzleBoardCanvas, self.showProgressVar.get(),
                                                      self.showBlockedPathsVar.get(), self.smartPlacementModeVar.get())
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

# ------ Begin main application code ------
if __name__ == '__main__':
    basePath = os.path.expandvars('$APPDATA')
    appBasePath = os.path.join(basePath, 'MasyuSolver')
    settingsFileName = 'masyuSolverConfig.ini'
    ConfigMgr.loadSettings(appBasePath, settingsFileName)
    uiWindow = SolverUIWindow()
    pb = PuzzleBoard()
    uiWindow.registerPuzzleBoard(pb)
    uiWindow.showWindow()
