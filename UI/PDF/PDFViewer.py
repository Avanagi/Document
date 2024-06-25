from tkinter import filedialog as fd
import os
from UI.PDF.Miner import PDFMiner
from UI.PDF.Menu import create_menu
from UI.PDF.Frames import *
from UI.PDF.PDFCanvas import create_canvas_with_scrollbars
from UI.PDF.PDFButtons import create_buttons
from UI.Functional.RightInterface import create_right_interface


class PDFViewer:
    def __init__(self, master):
        self.path = None
        self.fileisopen = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None
        self.master = master

        self.menu = create_menu(self.master, self.open_file)
        self.top_frame = create_top_frame(self.master)
        self.bottom_frame = create_bottom_frame(self.master)
        self.right_frame = create_right_frame(self.master)

        self.output, self.scrolly, self.scrollx = create_canvas_with_scrollbars(self.top_frame)

        self.upbutton, self.downbutton, self.page_label = create_buttons(
            self.bottom_frame, self.previous_page, self.next_page
        )

        (self.text_entry, self.accept_button, self.text_display,
         self.highlight_button, self.clear_button) = create_right_interface(
            self.right_frame, self.accept_text, self.highlight_area, self.clear_highlights
        )

    def open_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            self.path = filepath
            filename = os.path.basename(self.path)
            self.miner = PDFMiner(self.path)
            data, numPages = self.miner.get_metadata()
            self.current_page = 0
            if numPages:
                self.name = data.get('title', filename[:-4])
                self.author = data.get('author', None)
                self.numPages = numPages
                self.fileisopen = True
                self.display_page()
                self.master.title(self.name)

    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page)
            self.output.delete("all")
            self.output.image = self.img_file

            canvas_width = self.output.winfo_width()
            canvas_height = self.output.winfo_height()

            img_width = self.img_file.width()
            img_height = self.img_file.height()

            x = (canvas_width // 2) - (img_width // 2)
            y = (canvas_height // 2) - (img_height // 2)

            self.output.create_image(x, y, anchor='nw', image=self.img_file)

            self.stringified_current_page = self.current_page + 1
            self.page_label['text'] = f"{self.stringified_current_page} of {self.numPages}"

            region = self.output.bbox(ALL)
            self.output.configure(scrollregion=region)

    def next_page(self):
        if self.fileisopen:
            if self.current_page < self.numPages - 1:
                self.current_page += 1
                self.display_page()

    def previous_page(self):
        if self.fileisopen:
            if self.current_page > 0:
                self.current_page -= 1
                self.display_page()

    def accept_text(self):
        input_text = self.text_entry.get()
        self.text_display.config(state=NORMAL)
        self.text_display.delete(1.0, END)
        self.text_display.insert(END, input_text)
        self.text_display.config(state=DISABLED)

    def highlight_area(self):
        pass

    def clear_highlights(self):
        pass
