import tkinter as tk
import tkinter.filedialog as fd
from datetime import datetime
from ConfigMgr import *
from ErrorDialog import *
from PuzzleStateMachine import *
from PuzzleBoardFile import *
from Utilities import *
from BruteForceSolveWorkThread import *
from WorkingWindow import *
from Solver import *
from pathlib import *
import glob

class AutomatedTestEngine:
    # Configuration file tags
    __FILE_SECTION = 'File'
    __FILE_TEST_DIRECTORY = 'TestDirectory'

    def __init__(self):
        # Create the top-level application window
        self.mainWindow = tk.Tk()
        self.mainWindow.title("Maysu Solver Test Engine")

        # Retrieve the last used values, if there are any
        lastTestDirectoryUsed = ConfigMgr.getSettingValue(self.__FILE_SECTION, self.__FILE_TEST_DIRECTORY)
        if (lastTestDirectoryUsed == None):
            lastTestDirectoryUsed = ""

        # Create the primary window frame, into which all other UI widgets will be placed
        mainFrame = tk.Frame(master=self.mainWindow)
        mainFrame.pack(expand=True, fill=tk.BOTH)

        self.folderLabel = tk.Label(mainFrame, text="Test Folder:")
        self.folderLabel.grid(row=0, column=0, padx=(10, 30), pady=(10, 10))

        self.folderVar = tk.StringVar()
        self.folderVar.set(lastTestDirectoryUsed)
        self.folderValue = tk.Entry(mainFrame, width=52, textvariable=self.folderVar)
        self.folderValue.grid(row=0, column=1, padx=(0, 30), pady=(10, 10), sticky="W")

        self.browseFolderBtn = tk.Button(mainFrame, text="Browse", command=self.setTestFolder)
        self.browseFolderBtn.grid(row=0, column=2, ipadx = 10, padx=(10, 10), pady=(10, 10))

        self.resultsLabel = tk.Label(mainFrame, text="Test Results:")
        self.resultsLabel.grid(row=1, column=0)

        self.resultsFrame = tk.Frame(master=mainFrame)
        self.resultsFrame.grid(row=1, column=1, columnspan=2, sticky="W")

        self.testResults = tk.Listbox(self.resultsFrame, width=52, height=20)
        self.testResults.grid(row=0, column=0)
        self.testResultsScrollbar = tk.Scrollbar(self.resultsFrame, orient="vertical")
        self.testResultsScrollbar.config(command=self.testResults.yview)
        self.testResultsScrollbar.grid(row=0, column=1)
        self.testResults.config(yscrollcommand=self.testResultsScrollbar.set)

        btnFrame = tk.Frame(master=mainFrame)
        btnFrame.grid(row=2, columnspan=3)

        self.startBtn = tk.Button(btnFrame, text="Start", command=self.startTests)
        self.startBtn.grid(row=0, column=0, ipadx=20, padx=(10, 10), pady=(10, 10))

        self.cancelBtn = tk.Button(btnFrame, text="Cancel", command=self.stopTests)
        self.cancelBtn.grid(row=0, column=1, ipadx=20, padx=(10, 10), pady=(10, 10))
        self.cancelBtn['state'] = tk.DISABLED

        self.exitBtn = tk.Button(btnFrame, text="Exit", command=quit)
        self.exitBtn.grid(row=0, column=2, ipadx=20, padx=(10, 10), pady=(10, 10))

    def showWindow(self):
        self.mainWindow.mainloop()

    def setTestFolder(self):
        testDir = fd.askdirectory(parent=self.mainWindow, initialdir=self.folderVar.get(), title="Choose test folder", mustexist=tk.TRUE)
        if (testDir != ""):
            self.folderVar.set(testDir)

    def stopTests(self):
        self.cancelBtn['state'] = tk.DISABLED
        self.testsCancelled = True
        if (self.__bruteForceSolver != None):
            self.__bruteForceSolver.cancelWorkThread()

    def startTests(self):
        self.startBtn['state'] = tk.DISABLED
        self.testsCancelled = False
        self.testResults.delete(0, tk.END)

        # User must specify a valid folder with tests
        testFolder = self.folderVar.get()
        if (testFolder == None) or (testFolder == ""):
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Test Folder Error", "You must specify the test folder!")
            self.startBtn['state'] = tk.NORMAL
            return

        # Verify that the test folder exists
        if not (os.path.exists(testFolder)):
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Test Folder Error", "The test folder path is invalid!")
            self.startBtn['state'] = tk.NORMAL
            return

        # Verify that there are test cases in the folder
        folder = os.path.join(testFolder, "**/*.pbd")
        testCases = list(glob.iglob(folder, recursive=True))
        if (len(testCases) == 0):
            errorDialog = ErrorDialog(self.mainWindow)
            errorDialog.showDialog("Test Folder Error", "No test cases found!")
            self.startBtn['state'] = tk.NORMAL
            return

        ConfigMgr.setSettingValue(self.__FILE_SECTION, self.__FILE_TEST_DIRECTORY, testFolder)

        self.cancelBtn['state'] = tk.NORMAL
        self.browseFolderBtn['state'] = tk.DISABLED
        self.runTests(testCases)
        self.startBtn['state'] = tk.NORMAL
        self.cancelBtn['state'] = tk.DISABLED
        self.browseFolderBtn['state'] = tk.NORMAL

    def checkForThreadDone(self):
        if (self.__bruteForceSolver == None):
                return

        if not (self.__bruteForceSolver.isAlive()):
            # The work thread is done, so exit the nested mainloop
            self.mainWindow.quit()

        else:
            # Invoke the work thread's timer handler
            raiseParentWindow = self.__bruteForceSolver.timerHandler(self.mainWindow)

            if (raiseParentWindow):
                self.mainWindow.lift()

            # Reschedule checking for the thread completion
            self.mainWindow.after(100, self.checkForThreadDone)

    # Skip any test which is in a folder named "ignore"
    def skipThisTest(self, testPath):
        path = Path(testPath)
        for dir in path.parts:
            if (dir.lower() == "ignore"):
                return(True)

        return(False)

    def addTimestamp(self, label):
        # dd/mm/YY H:M:S
        dtString = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.testResults.insert(tk.END, label + dtString)
        self.testResults.see(tk.END)
        self.mainWindow.update()

    def runTests(self, testCases):
        solver = Solver()

        self.addTimestamp("Testing started at: ")

        for testCase in testCases:
            if (self.testsCancelled):
                break

            PuzzleStateMachine.reset()
            testCasePath, testCaseName = os.path.split(testCase)

            if (self.skipThisTest(testCasePath)):
                result = "Skipped - " + testCaseName
                self.testResults.insert(tk.END, result)
                self.testResults.see(tk.END)
                self.mainWindow.update()
                continue

            try:
                result = "<solving> - " + testCaseName
                self.testResults.insert(tk.END, result)
                self.testResults.see(tk.END)
                pb = PuzzleBoardFile.loadFile(testCase)
                solver.solve(pb)

                if (Utilities.checkIfPuzzleIsSolved(pb)):
                    result = "Solved - " + testCaseName
                else:
                    self.__bruteForceSolver = BruteForceSolveWorkThread(solver, pb)

                    self.__bruteForceSolver.start()

                    self.mainWindow.after(100, self.checkForThreadDone)
                    self.mainWindow.mainloop()

                    if (self.__bruteForceSolver.wasRequestCancelledByUser()):
                        result = "Cancelled - " + testCaseName
                        self.__bruteForceSolver = None
                        self.testResults.delete(tk.END)
                        self.testResults.insert(tk.END, result)
                        self.testResults.see(tk.END)
                        self.addTimestamp("Testing terminated at: ")
                        self.testResults.see(tk.END)
                        self.mainWindow.update()
                        return
                    else:
                        bruteForceResult = self.__bruteForceSolver.getBruteForceResults()
                        if (bruteForceResult != None):
                            result = "Solved - " + testCaseName
                        else:
                            result = "Unsolved - " + testCaseName
            except MasyuInvalidPuzzleFileException as mipfe:
                # Puzzle in the file was invalid
                result = "Invalid - " + testCaseName
            except Exception as e:
                result = "Error - " + testCaseName
            finally:
                self.__bruteForceSolver = None

            # embed in a try statement, in case the UI was closed
            try:
                self.testResults.delete(tk.END)
                self.testResults.insert(tk.END, result)
                self.testResults.see(tk.END)
                self.mainWindow.update()
            except Exception as e:
                exit()

        if (self.testsCancelled):
            self.addTimestamp("Testing cancelled at: ")
        else:
            self.addTimestamp("Testing completed at: ")


if __name__ == "__main__":
    basePath = os.path.expandvars('$APPDATA')
    appBasePath = os.path.join(basePath, 'MasyuSolver')
    settingsFileName = 'masyuTesterConfig.ini'
    ConfigMgr.loadSettings(appBasePath, settingsFileName)

    testUI = AutomatedTestEngine()
    testUI.showWindow()