from MasyuDialog import *
import tkinter as tk

class NoSolutionDialog(MasyuDialog):
    # Class constructor

    def __init__(self, parentWindow):
        super().__init__(parentWindow)
        self.__topLevel = None

    def okHandler(self):
        self.__topLevel.destroy()

    def showDialog(self):
        toplevel = tk.Toplevel()
        toplevel.resizable(0, 0)
        self.__topLevel = toplevel

        toplevel.title('No solution found')

        l1 = tk.Label(toplevel, image="::tk::icons::warning")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
        l2 = tk.Label(toplevel, text='Unable to find a solution')
        l2.grid(row=0, column=1, columnspan=4, padx=(0, 30), pady=(7, 10), sticky="w")

        b2 = tk.Button(toplevel, text="OK", command=self.okHandler, width=10)
        b2.grid(row=1, column=2, padx=(2, 35), pady=(0, 15), sticky="e")

        super().showDialog(toplevel)