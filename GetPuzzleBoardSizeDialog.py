import tkinter as tk

class GetPuzzleBoardSizeDialog():

    # This is the callback handler for the "OK" button.
    # It will save off the values from the Spinbox widgets,
    # before destroying the dialog window, causing input to once
    # again be sent to other windows for this application.
    def __processOKButton(self):
        # Return the values from the Spinbox widgets
        self.numRows = self.rowVar.get()
        self.numCols = self.colVar.get()

        # We must destroy our dialog window, in order to allow other windows to
        # again receive input
        self.dialogWindow.destroy()

    # This is the callback handler for the "Cancel" button.
    # It destroy the dialog window, causing input to once
    # again be sent to other windows for this application.
    def __processCancelButton(self):
        # Operation was cancelled
        self.numRows = -1
        self.numCols = -1

        # We must destroy our dialog window, in order to allow other windows to
        # again receive input
        self.dialogWindow.destroy()

    # Class constructor.  The only parameters are the max/min values (constraints)
    # for the row and column Spinbox widgets (as tuples).  If the constraints aren't
    # provided, then they will default to: (5, 15)
    def __init__(self, rowConstraints=(5, 15), colConstraints=(5, 15)):
        # Initialize the return values
        self.numRows = -1
        self.numCols = -1

        # Save off copies of the row and column constraints (max and min values)
        self.rowMin, self.rowMax = rowConstraints
        self.colMin, self.colMax = colConstraints

    # Method causing the modal dialog to be displayed.  When the dialog
    # is dismissed, it will return a tuple representing the selected
    # (row, col) values .. or (-1, -1) if the user cancelled the dialog.
    # It takes as optional parameters, the initial value to which the
    # row and column Spinbox should be set; defaults to the min value
    # if the initial value was not specified.
    def showDialog(self, initialRow=-1, initialCol=-1):

        # If either the initialRow or initialCol value was not provided, then
        # we will use the 'min' value
        if (initialRow == -1):
            initialRow = self.rowMin

        if (initialCol == -1):
            initialCol = self.colMin

        # Create a new window, which will represent our modal dialog
        self.dialogWindow = tk.Toplevel()
        self.dialogWindow.title("Entire Puzzle Board Size")

        # Remove the maximize window frame options; can't seem to remove
        # the minimize option, which is nuts!
        self.dialogWindow.resizable(False, False)

        # NOTE: after each widget is created, a call is made to the pack()
        # method.  The "Pack" object is a layout manager, and the parameters
        # provide the layout manager with "hints" about how we would like the
        # widgets laid out in the parent widget.

        # Create a frame for holding all of the other dialog widgets; the parent
        #  of the frame will be the dialogWindow object we just created.
        # Configure the frame to fill the width and height of the dialog window
        mainFrame = tk.Frame(master=self.dialogWindow)
        mainFrame.pack(expand=True, fill=tk.BOTH)

        # Create another frame (inside the mainFrame), where we will place the
        # widgets which allow the user to specify the Puzzle Board size.
        # We anchor this frame at the top of the mainFrame, and we want it to
        # fill (occupy) with full width (X) of the mainFrame.
        # We use a "LabelFrame" because it allows us to include a label which
        # is displayed with the frame!
        inputFrame = tk.LabelFrame(master=mainFrame, text="New Puzzle Size")
        inputFrame.pack(fill=tk.X, side=tk.TOP, pady=5, padx=10)

        # We will use 2 Spinbox widgets to collect the new PuzzleBoard size.
        # Each of the Spinbox widgets will be constrained to the range of
        # values specified by the code which invoked us.
        rowFrame = tk.Frame(master=inputFrame)
        rowFrame.pack(fill=tk.X, side=tk.TOP, padx=15)
        rowLabel = tk.Label(master=rowFrame, text="Number of rows:")
        rowLabel.pack(side=tk.LEFT, pady=10)
        self.rowVar = tk.IntVar()               # Variable for setting/getting spinner value
        self.rowVar.set(initialRow)
        numRowsSpinbox = tk.Spinbox(master=rowFrame, from_=self.rowMin, to=self.rowMax, textvariable=self.rowVar)
        numRowsSpinbox.pack(side=tk.RIGHT, pady=10)

        colFrame = tk.Frame(master=inputFrame)
        colFrame.pack(fill=tk.X, side=tk.TOP, padx=15)
        colLabel = tk.Label(master=colFrame, text="Number of columns:")
        colLabel.pack(side=tk.LEFT, pady=10, anchor=tk.SW)
        self.colVar = tk.IntVar()  # Variable for setting/getting spinner value
        self.colVar.set(initialCol)
        self.numColsSpinbox = tk.Spinbox(master=colFrame, from_=self.colMin, to=self.colMax, textvariable=self.colVar)
        self.numColsSpinbox.pack(side=tk.RIGHT, pady=10)

        # Create another frame (inside the mainFrame, but anchored below the
        # inputFrame, in which the OK/Cancel buttons will be placed
        buttonFrame = tk.Frame(master=mainFrame)
        buttonFrame.pack(fill=tk.X, side=tk.LEFT, padx=40, pady=10, ipadx=30)

        okButton = tk.Button(master=buttonFrame, text="OK", command=self.__processOKButton)
        okButton.pack(side=tk.LEFT, ipadx=30)
        cancelButton = tk.Button(master=buttonFrame, text="Cancel", command=self.__processCancelButton)
        cancelButton.pack(side=tk.RIGHT, ipadx=30)

        # Now display the dialog as an application modal dialog; which means all of the
        # other application windows will not respond to user input, until the user closes
        # this dialog!
        self.dialogWindow.focus_set()       # take over input focus for this application
        self.dialogWindow.grab_set()        # disable other windows while this dialog is open
        self.dialogWindow.wait_window()     # and wait here until the dialog window is destroyed

        # Return the values from the dialog as a tuple (or (-1, -1) if cancelled)
        return((self.numRows, self.numCols))

if __name__ == "__main__":
    currentRowValue = -1
    currentColValue = -1

    def showResizeDialog():
        global currentRowValue
        global currentColValue
        resizeResults = GetPuzzleBoardSizeDialog()
        rowVal, colVal = resizeResults.showDialog(currentRowValue, currentColValue)
        print("Dialog return value =", rowVal, "x", colVal)
        # Save the values, unless the user cancelled the dialog
        if ((rowVal != -1) and (colVal != -1)):
            currentRowValue = rowVal
            currentColValue = colVal

    mainWindow = tk.Tk()
    mainWindow.title("Modal Dialog test")

    testButtonsFrame = tk.Frame(master=mainWindow)
    testButtonsFrame.pack(expand=True, fill=tk.BOTH, padx=20)

    resizeDialogButton = tk.Button(master=testButtonsFrame, text="Show Resize Dialog", command=showResizeDialog)
    resizeDialogButton.pack(side=tk.TOP, pady=5)

    mainWindow.mainloop()