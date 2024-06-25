from tkinter import *


def create_right_interface(frame, accept_text_command, highlight_area_command,
                           clear_highlights_command):
    text_entry = Entry(frame, width=70)
    text_entry.grid(row=0, column=0, padx=0, pady=10)

    accept_button = Button(frame, text="Apply Prompt", command=accept_text_command)
    accept_button.grid(row=0, column=1, padx=0, pady=10)

    text_display = Text(frame, height=35, width=80, state=DISABLED)
    text_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    highlight_button = Button(frame, text="Highlight Area", command=highlight_area_command)
    highlight_button.grid(row=2, column=0, padx=10, pady=10)

    clear_button = Button(frame, text="Clear Highlights", command=clear_highlights_command)
    clear_button.grid(row=2, column=1, padx=10, pady=10)

    return text_entry, accept_button, text_display, highlight_button, clear_button
