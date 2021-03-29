class Cell():
    TYPE_DOT = 0
    TYPE_BLACK_CIRCLE = 1
    TYPE_WHITE_CIRCLE = 2

    def __init__(self, type = TYPE_DOT):
        self.type = type
        self.isCellEnabled = True
        self.isCellValid = True

    def clone(self):
        c = Cell(self.type)
        c.isCellEnabled = self.isCellEnabled
        c.isCellValid = self.isCellValid
        return(c)

    def reset(self):
        self.type = Cell.TYPE_DOT
        self.isCellEnabled = True
        self.isCellValid = True

    def isBlackCircle(self):
        return(self.type == Cell.TYPE_BLACK_CIRCLE)

    def isWhiteCircle(self):
        return(self.type == Cell.TYPE_WHITE_CIRCLE)

    def isDot(self):
        return(self.type == Cell.TYPE_DOT)

    def setAsBlackCircle(self):
        self.type = Cell.TYPE_BLACK_CIRCLE

    def setAsWhiteCircle(self):
        self.type = Cell.TYPE_WHITE_CIRCLE

    def setAsDot(self):
        self.type = Cell.TYPE_DOT

    def isEnabled(self):
        return(self.isCellEnabled)

    def setEnabled(self):
        self.isCellEnabled = True

    def setDisabled(self):
        self.isCellEnabled = False

    def isValid(self):
        return(self.isCellValid)

    def setValid(self):
        self.isCellValid = True

    def setInvalid(self):
        self.isCellValid = False

    def getType(self):
        return(self.type)

    def print(self):
        if self.type == Cell.TYPE_DOT:
            print("D", end = "")
        elif self.type == Cell.TYPE_BLACK_CIRCLE:
            print("B", end = "")
        elif self.type == Cell.TYPE_WHITE_CIRCLE:
            print("W", end = "")
        else:
            print("?", end = "")

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


