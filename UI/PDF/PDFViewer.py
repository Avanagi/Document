from tkinter import filedialog as fd
from tkinter import *
from UI.PDF.Miner import PDFMiner
from UI.PDF.Menu import create_menu
from UI.PDF.Frames import create_top_frame, create_bottom_frame, create_right_frame
from UI.PDF.PDFCanvas import create_canvas_with_scrollbars
from UI.PDF.PDFButtons import create_buttons
from UI.Functional.RightInterface import create_right_interface
from PIL import Image, ImageGrab

import os
import re
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'..\\Tesseract\\tesseract.exe'


class PDFViewer:
    def __init__(self, master):
        self.path = None
        self.fileisopen = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None
        self.master = master
        self.text = ""
        self.master.bind("<ButtonPress-1>", self.mouse_event)
        self.master.bind("<ButtonRelease-1>", self.mouse_event)

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

        self.x_p, self.y_p = None, None
        self.x_r, self.y_r = None, None
        self.highlight_canvas = None

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

            region = self.output.bbox("all")
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
        cleaned_text = self.text.strip().lstrip(",'").rstrip(",':")

        if input_text == "Головная":
            if self.text.strip() in self.name:
                self.text_display.insert(END, "All good. Описание внутри файла совпадает с названием файла\n")
            else:
                self.text_display.insert(END, "Unlucky. Описание внутри файла НЕ совпадает с названием файла\n")
                print("\n" + self.text)
        if input_text == "Документация":
            folder_path = os.path.dirname(self.path)
            print(folder_path)
            if os.path.isdir(folder_path):
                files = os.listdir(folder_path)
                print(files)
                print(cleaned_text)
                found = False
                for file in files:
                    if re.search(re.escape(cleaned_text), file, re.IGNORECASE):
                        found = True
                        break
                if found:
                    self.text_display.insert(END, f"Файл с названием, содержащим '{cleaned_text}', найден в папке.\n")
                else:
                    self.text_display.insert(END, f"Файл с названием, содержащим '{cleaned_text}', не найден в папке.\n")
            else:
                self.text_display.insert(END, "Указанная папка не существует.\n")

        else:
            self.text_display.insert(END, self.text)

        self.text_display.config(state=DISABLED)

    def highlight_area(self):
        try:
            self.upbutton.config(state=DISABLED)
            self.downbutton.config(state=DISABLED)

            canvas_width = self.output.winfo_width()
            canvas_height = self.output.winfo_height()
            img_width = self.output.image.width()
            img_height = self.output.image.height()

            if self.highlight_canvas:
                # Update existing canvas
                self.highlight_canvas.destroy()

            self.highlight_canvas = Canvas(self.master, width=canvas_width, height=canvas_height, bd=0,
                                           highlightthickness=0)
            self.highlight_canvas.place(x=0, y=0)

            x = (canvas_width // 2) - (img_width // 2)
            y = (canvas_height // 2) - (img_height // 2)

            self.highlight_canvas.create_image(x, y, anchor='nw', image=self.output.image)
            self.highlight_canvas.image = self.output.image
        except:
            print("Вы не выбрали pdf-файл для проверки. Выберите файл в Setting -> Open FIle.")

    def clear_highlights(self):
        self.upbutton.config(state=NORMAL)
        self.downbutton.config(state=NORMAL)
        if self.highlight_canvas:
            self.highlight_canvas.destroy()
            self.highlight_canvas = None

    def mouse_event(self, event):
        event_type = event.type

        if event_type == EventType.ButtonPress:
            if self.highlight_canvas:
                self.highlight_canvas.delete('rectangle')

            self.x_p, self.y_p = event.x, event.y

        elif event_type == EventType.ButtonRelease:
            if self.highlight_canvas:
                self.x_r, self.y_r = event.x, event.y

                if any([self.x_p is not None, self.y_p is not None, self.x_r is not None, self.y_r is not None]):
                    x1 = min(self.x_p, self.x_r)
                    y1 = min(self.y_p, self.y_r)
                    x2 = max(self.x_p, self.x_r)
                    y2 = max(self.y_p, self.y_r)

                    canvas_width = self.output.winfo_width()
                    canvas_height = self.output.winfo_height()

                    if x1 < 0 or y1 < 0 or x2 > canvas_width or y2 > canvas_height:
                        x1 = max(0, min(x1, canvas_width))
                        y1 = max(0, min(y1, canvas_height))
                        x2 = max(0, min(x2, canvas_width))
                        y2 = max(0, min(y2, canvas_height))

                    self.highlight_canvas.create_rectangle(x1, y1, x2, y2, outline='gray', width=2, tags='rectangle',
                                                           dash=(3, 3), fill='', stipple='gray50')

                    filename = r"..\rectangle_capture.png"
                    self.save_rectangle(x1, y1, x2, y2, filename)

    def save_rectangle(self, x1, y1, x2, y2, filename):
        try:
            canvas_x = self.highlight_canvas.winfo_rootx()
            canvas_y = self.highlight_canvas.winfo_rooty()

            x1 += canvas_x
            y1 += canvas_y
            x2 += canvas_x
            y2 += canvas_y

            screen_width = self.highlight_canvas.winfo_screenwidth()
            screen_height = self.highlight_canvas.winfo_screenheight()

            x1 = max(0, min(x1, screen_width))
            y1 = max(0, min(y1, screen_height))
            x2 = max(0, min(x2, screen_width))
            y2 = max(0, min(y2, screen_height))

            if x2 > x1 and y2 > y1:
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

                screenshot.save(filename)
                print(f"Saved rectangle area to {filename}")

                image = Image.open(filename)
                self.text = pytesseract.image_to_string(image, lang='rus')
                if self.text:
                    text_filename = r"..\rectangle_capture.txt"
                    with open(text_filename, 'w', encoding='utf-8') as f:
                        f.write(self.text)
                    print(f"Saved recognized text to {text_filename}")

                    self.accept_text()
            else:
                print("Rectangle has zero area.")

        except Exception as e:
            print(f"Error saving rectangle area: {e}")

    def is_inside_canvas(self, x1, y1, x2, y2):
        screen_width = self.highlight_canvas.winfo_screenwidth()
        screen_height = self.highlight_canvas.winfo_screenheight()

        x1 = max(0, min(x1, screen_width))
        y1 = max(0, min(y1, screen_height))
        x2 = max(0, min(x2, screen_width))
        y2 = max(0, min(y2, screen_height))
        if x2 > x1 and y2 > y1:
            return True
