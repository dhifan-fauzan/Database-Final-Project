import tkinter as tinker
from view import mainMenu

class Application(tinker.Tk):
    
    def __init__(self):
        
        tinker.Tk.__init__(self)
        
        self.frame = None
        self.switchFrame(mainMenu)

    def switchFrame(self, nFrame):

        newFrame = nFrame(self)

        if self.frame is not None:
            self.frame.destroy()

        self.frame = newFrame
        self.frame.pack()

screen = Application()
screen.title("Green Grocery")
screen.mainloop()