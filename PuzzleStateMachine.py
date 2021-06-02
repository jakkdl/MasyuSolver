# This class is used to keep track of the "state" of the current Puzzle Board.
# The state is important to know when the user tries to exit, open a saved Puzzle
# Board or simply create a new Puzzle Board; if the current Puzzle Board has
# unsaved changes, then the State Machine will track that, and will let us know
# that we need to ask the user whether to save the changes, before moving on.
#
# The different puzzle states are:
#   1) Unmodified and never saved to a file (new puzzle board)
#   2) Modified, but never saved to a file
#   3) Unmodified since the last 'file->open' operation
#   4) Modified since the last 'file->open' operation
#   5) Unmodified since the last 'file->save' operation
#   6) Modified since the last 'file->save' operation
#
# The state also enables us to track whether there is already a filename
# associated with the puzzle; if there is, then "file->save" can simply
# save to the associated file; if there isn't, then "file->save" needs to
# behave like "file->save as" (and prompt the user for the filename)

class PuzzleStateMachine():

    # Class variables
    __STATE1 = 1    # Unmodified and never saved to a file (new puzzle board)
    __STATE2 = 2    # Modified, but never saved to a file
    __STATE3 = 3    # Unmodified since the last 'file->open' operation
    __STATE4 = 4    # Modified since the last 'file->open' operation
    __STATE5 = 5    # Unmodified since the last 'file->save' operation
    __STATE6 = 6    # Modified since the last 'file->save' operation

    # Initial state: State 1, and no associated filename
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

