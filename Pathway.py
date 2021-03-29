# This is a private class, used only by the PuzzleBoard class
#
class Pathway():
    TYPE_OPEN = 0
    TYPE_LINE = 1
    TYPE_BLOCKED = 2

    # Constructor with default type of 'TYPE_OPEN'
    #
    def __init__(self, type = TYPE_OPEN):
        self.type = type

    # Returns an exact copy of the pathway
    #
    def clone(self):
        return(Pathway(self.type))

    # Resets the pathway to Open
    #
    def reset(self):
        self.type = Pathway.TYPE_OPEN

    # Sets the pathway to Line
    #
    def setAsLine(self):
        self.type = Pathway.TYPE_LINE

    # Sets the pathway to Blocked
    #
    def setAsBlocked(self):
        self.type = Pathway.TYPE_BLOCKED

    # Sets the pathway to Open
    #
    def setAsOpen(self):
        self.type = Pathway.TYPE_OPEN

    # Returns 'true' if pathway is Line
    #
    def isLine(self):
        return(self.type == Pathway.TYPE_LINE)

    # Returns 'true' if pathway is Blocked
    #
    def isBlocked(self):
        return(self.type == Pathway.TYPE_BLOCKED)

    # Returns 'true' if pathway is Open
    #
    def isOpen(self):
        return(self.type == Pathway.TYPE_OPEN)

    # Returns the type of the Pathway
    #
    def getType(self):
        return(self.type)

    # Prints the type of the Pathway: 'O' for Open,
    # 'L' for Line, 'X' for Blocked,
    # or '?' for anything else
    #
    def print(self):
        if self.type == Pathway.TYPE_OPEN:
            print("O", end = "")
        elif self.type == Pathway.TYPE_LINE:
            print("L", end = "")
        elif self.type == Pathway.TYPE_BLOCKED:
            print("X", end = "")
        else:
            print("?", end = "")

if __name__ == "__main__":
    print("Running Tests")

    p = Pathway()
    if p.isOpen():
        print("Test 1 Passed")
    else:
        print("Test 1 Failed")

    p = Pathway(Pathway.TYPE_LINE)
    if p.isLine():
        print("Test 2 Passed")
    else:
        print("Test 2 Failed")

    p = Pathway(Pathway.TYPE_LINE)
    p.setAsBlocked()
    if p.isBlocked():
         print("Test 3 Passed")
    else:
         print("Test 3 Failed")

    p.reset()
    if p.isOpen():
         print("Test 4 Passed")
    else:
         print("Test 4 Failed")

    p2 = p.clone()
    p2.setAsBlocked()
    if p.getType() == p2.getType():
        print("Test 5 Failed")
    else:
        print("Test 5 Passed")