import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PuzzleStateMachine import *
from ConfigMgr import *
from PuzzleBoardFile import *


class FileIO():
    # Class variables
    __MODE_NEW = 1
    __MODE_OPEN = 2
    __MODE_SAVE = 3
    __MODE_SAVE_AS = 4
    __MODE_EXIT = 5

    # Configuration file tags
    __FILE_SECTION = 'File'
    __FILE_DIRECTORY = 'Directory'

    # The following are the public methods for this class
    # The only parameter they take is the current puzzleBoard, since there
    # is a possibility that it may need to be saved, if there are unsaved changes
    #
    # Each of the public IO methods returns a tuple (status, puzzleBoard) or and exception:
    #
    # (True, puzzleBoard): op was successful; returns new puzzleBoard, if created, or None
    # (False, None): op was canceled by user
    # MasyuSaveFileException: error while saving current puzzleBoard
    # MasyuOpenFileException: error while opening puzzleBoard file
    # MasyuInvalidPuzzleFileException: invalid puzzleBoard in loaded file

    @classmethod
    # File -> New
    def fileNew(cls, puzzleBoard):
        return (cls.__processIO(cls.__MODE_NEW, puzzleBoard))

    @classmethod
    # File -> Open
    def fileOpen(cls, puzzleBoard):
        return (cls.__processIO(cls.__MODE_OPEN, puzzleBoard))

    @classmethod
    # File -> Save
    def fileSave(cls, puzzleBoard):
        return (cls.__processIO(cls.__MODE_SAVE, puzzleBoard))

    @classmethod
    # File -> Save As
    def fileSaveAs(cls, puzzleBoard):
        return (cls.__processIO(cls.__MODE_SAVE_AS, puzzleBoard))

    @classmethod
    # File -> Exit
    def fileExit(cls, puzzleBoard):
        return (cls.__processIO(cls.__MODE_EXIT, puzzleBoard))

    ###########################################################################################################
    # The following is a private "work" method, which does all of the common work
    ###########################################################################################################

    @classmethod
    # The 'mode' parameter can be set to one of the above values, and indicates which menu operation
    # is being requested. The 'puzzleBoard' parameter is the current puzzleboard.
    def __processIO(cls, mode, puzzleBoard):
        # Start out assuming that the current puzzle won't be saved
        saveCurrentPuzzle = False

        # If we are processing File -> Open, File -> New, or File -> Exit, then we need to check
        # if the current puzzle has unsaved changes.  If it does, then we need to ask the user
        # if they want to save them or discard them
        if ((mode == cls.__MODE_OPEN) or (mode == cls.__MODE_NEW) or (mode == cls.__MODE_EXIT)):
            # TODO: Not implemented
            print("Not implemented")

        elif ((mode == cls.__MODE_SAVE) or (mode == cls.__MODE_SAVE_AS)):
            # Make sure that we save the current puzzle!
            saveCurrentPuzzle = True

        # If there were changes needing to be saved, and the user said they wanted to
        # save the changes (or if this was a File -> Save or File -> Save As request)
        # then the saving happens now.
        if (saveCurrentPuzzle):
            # If there isn't a filename already associated with the current puzzle
            # (or if this is a File -> Save As request), then we need to ask the
            # user to select the folder and filename into which the puzzle will be saved
            currentFilename = PuzzleStateMachine.getFileName()
            lastDirectoryUsed = ConfigMgr.getSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY)

            if ((mode == cls.__MODE_SAVE_AS) or (currentFilename == None)):
                # User needs to choose directory and filename
                saveFilePath = fd.asksaveasfilename(initialdir = lastDirectoryUsed)

                if (saveFilePath == ''):
                    return ((False, None))

                if not (saveFilePath.endswith('.' + PuzzleBoardFile.FILE_EXTENSION)):
                    saveFilePath += '.' + PuzzleBoardFile.FILE_EXTENSION

            else:
                # There is already a filename associated with this puzzle board, so use it
                saveFilePath = os.path.join(lastDirectoryUsed, currentFilename)

            # Now write the data to the file!
            try:
                PuzzleBoardFile.saveToFile(saveFilePath, puzzleBoard)

            except Exception as e:
                raise MasyuFileSaveException("Error while saving puzzle file") from e

            else:
                # Success!
                # Update the saved filename and path information
                lastDirectoryUsed, currentFilename = os.path.split(saveFilePath)

                # Update the state Mgr
                PuzzleStateMachine.fileSavedAs(currentFilename)

                # Update the Config Mgr
                ConfigMgr.setSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY, lastDirectoryUsed)

                # If this was a File -> Save or File -> Save As request, then we are done!
                # If it was a File -> Exit request, then we can now exit the application.
                if ((mode == cls.__MODE_SAVE) or (mode == cls.__MODE_SAVE_AS)):
                    return((True, None))

                elif (mode == cls.__MODE_EXIT):
                    return((True, None))

        # Now it is time to move onto loading the new puzzle file

        # Get the last directory used (from the Config mgr)
        lastDirectoryUsed = ConfigMgr.getSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY)

        # Display a 'file open' dialog, to find out which file to open
        supportedFileTypes = [(PuzzleBoardFile.FILE_EXTENSION, "*." + PuzzleBoardFile.FILE_EXTENSION)]
        fileToOpen = fd.askopenfilename(initialdir=lastDirectoryUsed, filetypes=supportedFileTypes, defaultextension=supportedFileTypes)
        if (fileToOpen == ""):
            return ((False, None))

        lastDirectoryUsed, currentFilename = os.path.split(fileToOpen)

        # Read the puzzle board data from the file
        try:
            newPuzzleBoard = PuzzleBoardFile.loadFile(fileToOpen)
        except MasyuInvalidPuzzleFileException as mipfe:
            # Puzzle in the file was invalid
            raise
        except Exception as e:
            raise MasyuFileOpenException ("Error during open file") from e
        else:
            # Successful load!
            # Update the directory stored in the Config Mgr, and update the
            # State Mgr state (and filename)
            PuzzleStateMachine.fileOpened(currentFilename)
            ConfigMgr.setSettingValue(cls.__FILE_SECTION, cls.__FILE_DIRECTORY, lastDirectoryUsed)

            # Return the new puzzle board
            return((True, newPuzzleBoard))