import tkinter as tk
from main import Blockchain, Transaction

class BlockchainGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Blockchain GUI")
        self.label = tk.Label(self.window, text="Blockchain!")
        self.label.pack()

    def run(self):
        self.window.mainloop()

        

if __name__ == "__main__":
    gui = BlockchainGUI()
    gui.run()