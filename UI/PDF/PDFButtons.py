from tkinter import PhotoImage
from tkinter import ttk


def create_buttons(frame, previous_page_command, next_page_command):
    uparrow_icon = PhotoImage(file='Icons/uparrow.png')
    downarrow_icon = PhotoImage(file='Icons/downarrow.png')

    uparrow = uparrow_icon.subsample(3, 3)
    downarrow = downarrow_icon.subsample(3, 3)

    upbutton = ttk.Button(frame, image=uparrow, command=previous_page_command)
    upbutton.image = uparrow  # Keep a reference to avoid garbage collection
    upbutton.grid(row=0, column=1, padx=(330, 5), pady=8)

    downbutton = ttk.Button(frame, image=downarrow, command=next_page_command)
    downbutton.image = downarrow  # Keep a reference to avoid garbage collection
    downbutton.grid(row=0, column=3, pady=8)

    page_label = ttk.Label(frame, text='pages')
    page_label.grid(row=0, column=4, padx=5)

    return upbutton, downbutton, page_label
