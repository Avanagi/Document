from tkinter import ttk
from tkinter import *


def create_top_frame(master):
    top_frame = ttk.Frame(master, width=800, height=910)
    top_frame.grid(row=0, column=0)
    top_frame.grid_propagate(False)
    return top_frame


def create_bottom_frame(master):
    bottom_frame = ttk.Frame(master, width=800, height=100)
    bottom_frame.grid(row=1, column=0)
    bottom_frame.grid_propagate(False)
    return bottom_frame


def create_right_frame(master):
    right_frame = ttk.Frame(master, width=680, height=960)
    right_frame.grid(row=0, column=1, rowspan=2, sticky=(N, S, E, W))
    right_frame.grid_propagate(False)
    return right_frame
