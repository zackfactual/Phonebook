from tkinter import *
import tkinter as tk

# import other modules for access
import phonebook_gui
import phonebook_func

# ParentWindow class inherits from TKinter frame class
class ParentWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        # define master frame configuration
        self.master = master
        self.master.minsize(500, 300)
        self.master.maxsize(500, 300)

        # center app on user's screen
        phonebook_func.center_window(self, 500, 300)
        self.master.title("Phonebook")
        self.master.configure(bg='#F0F0F0')

        # if user Xs out
        self.master.protocol("WM_DELETE_WINDOW", lambda: phonebook_func.ask_quit(self))

        # load GUI widgets from separate module
        phonebook_gui.load_gui(self)


if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()