from tkinter import ttk


def create_top_frame(master):
    top_frame = ttk.Frame(master, width=800, height=900)
    top_frame.grid(row=0, column=0)
    top_frame.grid_propagate(False)
    return top_frame


def create_bottom_frame(master):
    bottom_frame = ttk.Frame(master, width=800, height=110)
    bottom_frame.grid(row=1, column=0)
    bottom_frame.grid_propagate(False)
    return bottom_frame
