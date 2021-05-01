from MasyuDialog import *
import tkinter as tk

class UnsavedChangesDialog(MasyuDialog):

    # Class constructor

    def __init__(self, parentWindow):
        super().__init__(parentWindow)
        self.__topLevel = None
        self.__result = None

    def yesHandler(self):
        self.__result = True
        self.__topLevel.destroy()

    def noHandler(self):
        self.__result = False
        self.__topLevel.destroy()

    def cancelHandler(self):
        self.__result = None
        self.__topLevel.destroy()

    def showDialog(self):
        toplevel = tk.Toplevel()
        toplevel.resizable(0,0)
        self.__topLevel = toplevel

        toplevel.title("Save Changes?")

        l1 = tk.Label(toplevel, image="::tk::icons::question")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
        l2 = tk.Label(toplevel, text="There are unsaved changes.\nWould you like to save before continuing?")
        l2.grid(row=0, column=1, columnspan=4, pady=(7, 10), sticky="w")

        b1 = tk.Button(toplevel, text="Yes", command=self.yesHandler, width=10)
        b1.grid(row=1, column=1, padx=(2, 35), pady=(0,15), sticky="e")
        b2 = tk.Button(toplevel, text="No", command=self.noHandler, width=10)
        b2.grid(row=1, column=2, padx=(2, 35), pady=(0,15), sticky="e")
        b3 = tk.Button(toplevel, text="Cancel", command=self.cancelHandler, width=10)
        b3.grid(row=1, column=3, padx=(2, 35), pady=(0,15), sticky="e")

        self.__result = None
        super().showDialog(toplevel)
        return(self.__result)