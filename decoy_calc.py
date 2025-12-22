import tkinter as tk
class Calculator:
    def __init__(self, win):
        self.win = win
        win.title("Calculator")
        win.geometry("300x400")
        win.resizable(False, False)
