# This is a private class, used only by the PuzzleBoard class.
#
class Cell():
    TYPE_DOT = 0
    TYPE_BLACK_CIRCLE = 1
    TYPE_WHITE_CIRCLE = 2
    TYPE_GREY_CIRCLE = 3

    # Constructor with default type of 'TYPE_DOT'
    #
    def __init__(self, type = TYPE_DOT):
        self.type = type
        self.isCellEnabled = True
        self.isCellValid = True
        self.wasProcessed = False

    # Returns an exact copy of the cell
    #
    def clone(self):
        c = Cell(self.type)
        c.isCellEnabled = self.isCellEnabled
        c.isCellValid = self.isCellValid
        return(c)

    def setProcessedFlag(self):
        self.wasProcessed = True

    def clearProcessedFlag(self):
        self.wasProcessed = False

    def wasCellProcessed(self):
        return (self.wasProcessed)

    # Resets the cell to: DOT, Valid, and Enabled
    #
    def reset(self):
        self.type = Cell.TYPE_DOT
        self.isCellEnabled = True
        self.isCellValid = True

    # Returns 'true' if cell is a BlACK CIRCLE
    #
    def isBlackCircle(self):
        return(self.type == Cell.TYPE_BLACK_CIRCLE)

    # Returns 'true' if cell is a WHITE CIRCLE
    #
    def isWhiteCircle(self):
        return(self.type == Cell.TYPE_WHITE_CIRCLE)
    def isGreyCircle(self):
        return(self.type == Cell.TYPE_GREY_CIRCLE)

    # Returns 'true' if cell is a DOT
    #
    def isDot(self):
        return(self.type == Cell.TYPE_DOT)

    # Sets the cell to a BLACK CIRCLE
    #
    def setAsBlackCircle(self):
        self.type = Cell.TYPE_BLACK_CIRCLE

    # Sets the cell to a WHITE CIRCLE
    #
    def setAsWhiteCircle(self):
        self.type = Cell.TYPE_WHITE_CIRCLE
    def setAsGreyCircle(self):
        self.type = Cell.TYPE_GREY_CIRCLE

    # Sets the cell to a DOT
    #
    def setAsDot(self):
        self.type = Cell.TYPE_DOT

    # Returns 'true' if cell is Enabled
    #
    def isEnabled(self):
        return(self.isCellEnabled)

    # Marks the cell as Enabled
    #
    def setEnabled(self):
        self.isCellEnabled = True

    # Marks the cell as Disabled
    #
    def setDisabled(self):
        self.isCellEnabled = False

    # Returns 'true' if the cell is Valid
    #
    def isValid(self):
        return(self.isCellValid)

    # Marks the cell as Valid
    #
    def setValid(self):
        self.isCellValid = True

    # Marks the cell as Invalid
    #
    def setInvalid(self):
        self.isCellValid = False

    # Returns the cell type
    #
    def getType(self):
        return(self.type)

    # Prints the cell type: 'D' for DOT,
    # 'B' for BLACK CIRCLE, 'W' for WHITE CIRCLE,
    # or '?' for anything else
    #
    def print(self):
        if self.type == Cell.TYPE_DOT:
            print("D", end="")
        elif self.type == Cell.TYPE_BLACK_CIRCLE:
            print("B", end="")
        elif self.type == Cell.TYPE_WHITE_CIRCLE:
            print("W", end="")
        else:
            print("?", end="")

if __name__ == "__main__":
    print("Running Tests")

    c = Cell()
    if c.isDot() and c.isValid() and c.isEnabled():
        print ("Test 1 passed")
    else:
        print("Test 1 failed")

    c = Cell(Cell.TYPE_WHITE_CIRCLE)
    if c.isWhiteCircle() and c.isValid() and c.isEnabled():
        print ("Test 2 passed")
    else:
        print("Test 2 failed")

    c = Cell(Cell.TYPE_BLACK_CIRCLE)
    c.setInvalid()
    if c.isBlackCircle() and not c.isValid() and c.isEnabled():
        print("Test 3 passed")
    else:
        print("Test 3 failed")

    c = Cell(Cell.TYPE_BLACK_CIRCLE)
    c.setDisabled()
    if c.isBlackCircle() and c.isValid() and not c.isEnabled():
        print("Test 4 passed")
    else:
        print("Test 4 failed")


