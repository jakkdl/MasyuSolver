import tkinter as tk

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
    ITEM_WHITE_CIRCLE_SIZE = 20      # Size of the white circle item
    ITEM_BLACK_CIRCLE_SIZE = 20      # Size of the black circle item
    ITEM_DOT_SIZE = 8               # Size of the dot item

    NO_ITEM = -1
    WHITE_ITEM = 0
    BLACK_ITEM = 1
    DOT_ITEM = 2

    # -------- Start of menu bar handlers ------

    # Placeholder callback for menu items
    def donothing(self):
        print("do nothing")

    # Test increasing the size of the Puzzle Board canvas
    def increaseMainCanvasSize(self, canvas):
        currentWidth = canvas.winfo_width()
        currentHeight = canvas.winfo_height()
        print("Canvas size =", currentWidth, "x", currentHeight)
        currentWidth += 50
        currentHeight += 50
        canvas.config(width=currentWidth, height=currentHeight)

    # Test decreasing the size of the Puzzle Board Canvas
    def decreaseMainCanvasSize(self, canvas):
        currentWidth = canvas.winfo_width()
        currentHeight = canvas.winfo_height()
        print("Canvas size =", currentWidth, "x", currentHeight)
        currentWidth -= 50
        currentHeight -= 50
        canvas.config(width=currentWidth, height=currentHeight)

    # -------- End of menu bar handlers --------

    # ------ Start of private helper functions ------

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
            self.selectedItem.itemconfigure('hilite', fill=self.itemCanvasColor)

        # Now draw the highlight around the selected item
        self.selectedItem = item
        item.itemconfigure('hilite', fill='red')

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

        item.create_line(itemX1, itemY1, itemX2, itemY1, fill=self.itemCanvasColor, tags=('hilite'))
        item.create_line(itemX2, itemY1, itemX2, itemY2, fill=self.itemCanvasColor, tags=('hilite'))
        item.create_line(itemX2, itemY2, itemX1, itemY2, fill=self.itemCanvasColor, tags=('hilite'))
        item.create_line(itemX1, itemY2, itemX1, itemY1, fill=self.itemCanvasColor, tags=('hilite'))

        return(item)

    # Create the canvas widget for holding the 3 items, and then draw the items
    def __createItems(self, parent):

        self.whiteItem = self.__createItem(parent, self.ITEM_WHITE_CIRCLE_SIZE, 'white')
        self.blackItem = self.__createItem(parent, self.ITEM_BLACK_CIRCLE_SIZE, 'black')
        self.dotItem = self.__createItem(parent, self.ITEM_DOT_SIZE, 'dark grey')

    # ------ End of private helper functions ------

    # ------ Start of public class methods ------

    # Constructor method
    def __init__(self):
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
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=lambda: self.increaseMainCanvasSize(puzzleBoardCanvas))
        filemenu.add_command(label="Save", command=lambda: self.decreaseMainCanvasSize(puzzleBoardCanvas))
        filemenu.add_command(label="Save As ..", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.mainWindow.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Create the 'Help' menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Instructions", command=self.donothing)
        helpmenu.add_command(label="About", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # Attach the menubar to the main application window
        self.mainWindow.config(menu=menubar)

    # Method for displaying the solver UI window
    def showWindow(self):
        self.mainWindow.mainloop()

    # Method for assigning a PuzzleBoard object to this UI window
    def registerPuzzleBoard(self):
        print("Todo - save puzzle board object, resize canvas and force a refresh of the canvas")

    # ------ End of public class methods ------

# ------ Begin test code ------
if __name__ == '__main__':
    uiWindow = SolverUIWindow()
    uiWindow.showWindow()