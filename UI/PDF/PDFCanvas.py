from tkinter import *


def create_canvas_with_scrollbars(frame):
    scrolly = Scrollbar(frame, orient=VERTICAL)
    scrolly.grid(row=0, column=1, sticky=(N, S))

    scrollx = Scrollbar(frame, orient=HORIZONTAL)
    scrollx.grid(row=1, column=0, sticky=(W, E))

    output = Canvas(frame, bg='#ECE8F3', width=780, height=890)
    output.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    output.grid(row=0, column=0, sticky=(N, S, E, W))

    scrolly.configure(command=output.yview)
    scrollx.configure(command=output.xview)

    return output, scrolly, scrollx
