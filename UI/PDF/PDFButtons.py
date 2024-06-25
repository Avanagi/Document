from tkinter import PhotoImage, Button, GROOVE
from tkinter import ttk


def create_buttons(frame, previous_page_command, next_page_command):
    uparrow_icon = PhotoImage(file='icons/uparrow.png')
    downarrow_icon = PhotoImage(file='icons/downarrow.png')

    uparrow = uparrow_icon.subsample(3, 3)
    downarrow = downarrow_icon.subsample(3, 3)

    upbutton = ttk.Button(frame, image=uparrow, command=previous_page_command)
    upbutton.image = uparrow
    upbutton.grid(row=0, column=1, padx=(330, 5), pady=8)

    downbutton = ttk.Button(frame, image=downarrow, command=next_page_command)
    downbutton.image = downarrow
    downbutton.grid(row=0, column=3, pady=8)

    page_label = ttk.Label(frame, text='pages')
    page_label.grid(row=0, column=4, padx=5)

    return upbutton, downbutton, page_label
