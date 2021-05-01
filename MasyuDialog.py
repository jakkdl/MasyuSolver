class MasyuDialog():
    # Constructor method
    def __init__(self, parentWindow):
        self.__parentWindow = parentWindow
        self.__dialogWindow = None

    def showDialog(self, dialogWindow):
        # Apparently a common hack to get the window size. Temporarily hide the
        # window to avoid update_idletasks() drawing the window in the wrong
        # position.
        self.__dialogWindow = dialogWindow
        self.__dialogWindow.withdraw()
        self.__dialogWindow.update_idletasks()

        dialogX = self.__parentWindow.winfo_x() + (self.__parentWindow.winfo_width() / 2) - (self.__dialogWindow.winfo_width() / 2)
        dialogY = self.__parentWindow.winfo_y() + (self.__parentWindow.winfo_height() / 2) - (self.__dialogWindow.winfo_height() / 2)

        if (dialogX < 0):
            dialogX = 0

        if (dialogY < 0):
            dialogY = 0

        screenWidth = self.__parentWindow.winfo_screenwidth()
        screenHeight = self.__parentWindow.winfo_screenheight()

        if ((dialogX + self.__dialogWindow.winfo_width()) >= screenWidth):
            dialogX = screenWidth - self.__dialogWindow.winfo_width()

        if ((dialogY + self.__dialogWindow.winfo_height()) >= screenHeight):
            dialogY = screenHeight - self.__dialogWindow.winfo_height()

        self.__dialogWindow.geometry("+%d+%d" % (dialogX, dialogY))
        self.__dialogWindow.deiconify()

        # Now display the dialog as an application modal dialog; which means all of the
        # other application windows will not respond to user input, until the user closes
        # this dialog!
        self.__dialogWindow.focus_set()  # take over input focus for this application
        self.__dialogWindow.grab_set()  # disable other windows while this dialog is open
        self.__dialogWindow.wait_window()  # and wait here until the dialog window is destroyed