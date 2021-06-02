import tkinter as tk
from threading import Thread
import time

# This is a modal dialog, but one which has no window manager decorations at all.
# It's purpose is to provide the user with some feedback that the program is still
# alive .. just busy doing something!  This is typically used when a time-consuming
# operation is being done in another thread.  However, sometimes the work done in the
# thread completes quickly.  To prevent the 'working' window from popping up for a
# second, and then going away, we delay (for 0.5 seconds), before actually showing
# the "working" window.
class WorkingWindow():

    # Base message displayed in the 'working' window
    WORKING_MESSAGE = "WORKING "

    # Controls the delay between when we update the dots showing progress
    INITIAL_DOT_COUNTER_VALUE = 10

    # Controls the delay before we start showing the "working" window
    INITIAL_ITERATION_COUNTER_VALUE = 5

    # Controls the maximum number of dots shown
    MAX_DOTS = 5

    # User has selected the cancel button, so signal to the thread
    # process that it should stop what it was doing.
    def __cancelButtonCallback(self):
        self.cancelButton['state'] = tk.DISABLED

        print("cancel")
        self.__workThread.cancelWorkThread()

    def __init__(self, parentWindow, workThread):
        # Each thread completion check occurs at approximately 0.1
        # second increments .. so 5 of those would equal 0.5 seconds.
        # It is after that amount of time that we will show the "working"
        # window, if the work thread is still alive
        self.iterationCounter = self.INITIAL_ITERATION_COUNTER_VALUE
        self.dotCounter = self.INITIAL_DOT_COUNTER_VALUE
        self.numDots = 0

        # Store the handle to the thread, so we can detect when it is done
        self.__workThread = workThread

        # Store the handle to the parent window, so we can re-enable it when the
        # work is done.
        self.parentWindow = parentWindow

        # Create the "working" dialog window
        self.dialogWindow = tk.Toplevel(master=parentWindow)
        self.dialogWindow.wm_overrideredirect(True)
        self.messageFrame = tk.Frame(master=self.dialogWindow, relief=tk.RAISED, borderwidth=5)
        self.messageFrame.pack(expand=True, fill=tk.BOTH)
        self.workingMessage = tk.StringVar()
        self.workingMessage.set(self.WORKING_MESSAGE + "      ")
        self.message = tk.Label(master=self.messageFrame, textvariable=self.workingMessage)
        self.message.pack(side=tk.TOP, padx=20, pady=20, anchor=tk.SW)

        # Only display a Cancel button if a callback was provided.
        if (self.__workThread.supportsCancelRequest()):
            self.cancelButton = tk.Button(master=self.messageFrame, text="Cancel", command=self.__cancelButtonCallback, width=10)
            self.cancelButton.pack(side=tk.TOP, pady=(0,15))
        else:
            self.cancelButton = None

    # Our only option for detecting when the thread has completed (so that
    # we can stop showing the "working" window), is to periodically poll
    # the status of the thread.
    def checkForThreadDone(self):
        if not (self.__workThread.isAlive()):
            # The work thread is done, so remove the "waiting" window
            self.dialogWindow.destroy()

        else:
            # Check if we need to make the "working" window visible
            if (self.iterationCounter > 0):
                self.iterationCounter -= 1
                if (self.iterationCounter == 0):
                    # Force the window visible, by removing the
                    # geometry constraint we had applied
                    self.dialogWindow.geometry("")
                    self.dialogWindow.geometry(self.savedGeometry)

            self.dotCounter -= 1
            if (self.dotCounter <= 0):
                # Change the message in the "working" window, to give
                # the user a feeling that all is well (and not locked up)
                self.numDots += 1
                if (self.numDots > self.MAX_DOTS):
                    self.numDots = 0

                message = self.WORKING_MESSAGE
                for i in range(self.numDots):
                    message = message + "."

                self.messageFrame.pack_propagate(False)
                self.workingMessage.set(message)

                # Reset the dot counter for the next pass
                self.dotCounter = self.INITIAL_DOT_COUNTER_VALUE

            # Invoke the work thread's timer handler
            raiseParentWindow = self.__workThread.timerHandler(self.dialogWindow)

            if (raiseParentWindow):
                self.parentWindow.lift()
                self.dialogWindow.lift()

            # Reschedule checking for the thread completion
            self.dialogWindow.after(100, self.checkForThreadDone)

    # To prevent the "working" window from flashing (if the work
    # completes quickly, we will initially show the "working"
    # window with a (0x0) dimension (effectively making it appear
    # invisible for the first 0.5 seconds.  If after that time,
    # the time-intensive work is still going, then we'll resize
    # the "working" window, so the user can see it.
    def showWindow(self):

        # Apparently a common hack to get the window size. Temporarily hide the
        # window to avoid update_idletasks() drawing the window in the wrong
        # position.
        self.dialogWindow.withdraw()
        #self.dialogWindow.config(cursor='watch')
        self.dialogWindow.update_idletasks()

        dialogX = self.parentWindow.winfo_x() + (self.parentWindow.winfo_width() / 2) - (self.dialogWindow.winfo_width() / 2)
        dialogY = self.parentWindow.winfo_y() + (self.parentWindow.winfo_height() / 2) - (self.dialogWindow.winfo_height() / 2)

        if (dialogX < 0):
            dialogX = 0

        if (dialogY < 0):
            dialogY = 0

        screenWidth = self.parentWindow.winfo_screenwidth()
        screenHeight = self.parentWindow.winfo_screenheight()

        if ((dialogX + self.dialogWindow.winfo_width()) >= screenWidth):
            dialogX = screenWidth - self.dialogWindow.winfo_width()

        if ((dialogY + self.dialogWindow.winfo_height()) >= screenHeight):
            dialogY = screenHeight - self.dialogWindow.winfo_height()

        # We can't set the geometry now, because we want the window to
        # initially be invisible.  So we will save the calculated geometry,
        # and set it once we want the window to be displayed
        self.savedGeometry = "+%d+%d" % (dialogX, dialogY)

        # Initially make the window so small that the user doesn't see it.  This
        # is done to prevent the window from "flashing", during those rare times
        # when the time-intensive operation isn't actually time-intensive.  Only
        # after a certain amount of time will we resize the "working" window, so
        # the user will see it.
        self.dialogWindow.geometry("0x0")

        self.dialogWindow.deiconify()

        # disable the main window; seems to be necessary, because otherwise the
        # user can still move the main window, causing it to appear "disconnected"
        # from the modal dialog!
        self.parentWindow.attributes('-disabled', True)

        # Now display the dialog as an application modal dialog; which means all of the
        # other application windows will not respond to user input, until we close
        # this dialog (once the work thread has completed).
        self.dialogWindow.focus_set()  # take over input focus for this application
        self.dialogWindow.grab_set()  # disable other windows while this dialog is open

        # Set a 100 mSec timer, which will allow us to check if the work thread
        # has completed
        self.dialogWindow.after(100, self.checkForThreadDone)

        # Wait for the modal dialog to be destroyed
        self.dialogWindow.wait_window()

        # Re-enable the main window; otherwise, the user won't be
        # able to interact with it, even though the modal dialog
        # is no longer active!  We also need to force the window
        # to the top of the stacking order, because the re-enabling
        # seems to cause it to sink to the bottom of the stacking order!
        self.parentWindow.attributes('-disabled', False)
        self.parentWindow.lift()
