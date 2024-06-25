from tkinter import Tk


def setup_window():
    root = Tk()
    root.title('PDF Analyzer')
    root.geometry('1480x960')
    root.resizable(width=0, height=0)
    return root
