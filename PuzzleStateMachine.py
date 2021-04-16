class PuzzleStateMachine():

    # Class variables
    __STATE1 = 1
    __STATE2 = 2
    __STATE3 = 3
    __STATE4 = 4
    __STATE5 = 5
    __STATE6 = 6

    __lastFileName = None
    __state = __STATE1

    @classmethod
    # Called when File --> New happens; resets the last saved filename and restores the
    # state to __STATE1
    def reset(cls):
        cls.__state = cls.__STATE1
        cls.__lastFileName = None

    @classmethod
    # This should be called after File --> Open has taken place.  It sets the state to
    # __STATE3, and also saves the filename associated with the loaded file.
    def fileOpened(cls, fileName):
        cls.__state = cls.__STATE3
        cls.__lastFileName = fileName

    @classmethod
    # This should be called after a puzzle board has been saved using the File --> Save As
    # menu item, or after saving an unnamed puzzle board for the first time.  It will set
    # the state to __STATE5, and will also save the filename associated with the current
    # puzzle
    def fileSavedAs(cls, fileName):
        cls.__state = cls.__STATE5
        cls.__lastFileName = fileName

    @classmethod
    # This should be called anytime the current puzzle board is changed by the user.
    # If the current state is __STATE1, then the new state will be __STATE2.
    # If the current state is __STATE3, then the new state will be __STATE4.
    # If the current state is __STATE5, then the new state will be __STATE6.
    # For any other state, no change will take place (because the state is already set to
    # reflect that the puzzle has been changed)
    def puzzleChanged(cls):

        if (cls.__state == cls.__STATE1):
            cls.__state = cls.__STATE2
        elif (cls.__state == cls.__STATE3):
            cls.__state = cls.__STATE4
        elif (cls.__state == cls.__STATE5):
            cls.__state = cls.__STATE6

    @classmethod
    # Returns 'True' if the state indicates that the puzzle has changed; otherwise, it
    # returns 'False'
    def hasPuzzleChanged(cls):
        return ((cls.__state == cls.__STATE2) or (cls.__state == cls.__STATE4) or
                (cls. __state == cls.__STATE6))

    @classmethod
    # Returns the last file name used while saving or opening a puzzle board.  The
    # file name may be 'None', if there wasn't yet a save or open request
    def getFileName(cls):
        return(cls.__lastFileName)

