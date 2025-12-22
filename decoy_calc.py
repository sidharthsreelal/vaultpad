import tkinter as tk

class Calculator:
    def __init__(self, win):
        self.win = win
        win.title("Calculator")
        win.geometry("300x400")
        win.resizable(False, False)
        
        self.displaytext = tk.StringVar()
        self.screen = tk.Entry(win, textvariable=self.displaytext, font=('Arial', 20), bd=10,
                               insertwidth=2, width=14, borderwidth=4, justify='right')
        self.screen.grid(row=0, column=0, columnspan=4, pady=10)
        self.displaytext.set("0")

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
