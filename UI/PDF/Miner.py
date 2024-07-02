import math
import fitz
from tkinter import PhotoImage


class PDFMiner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = fitz.open(self.filepath)
        self.first_page = self.pdf.load_page(0)
        self.width, self.height = self.first_page.rect.width, self.first_page.rect.height
        zoomdictionary = {900: 0.6, 800: 0.8, 700: 0.91, 600: 1.05, 500: 1.05,
                          400: 1.5, 300: 1.73, 200: 2.5, 100: 2.8, 50: 3.0, 10: 3.5}
        width = int(math.floor(self.width / 100.0) * 100)
        self.zoom = zoomdictionary[width]

    def get_metadata(self):
        metadata = self.pdf.metadata
        numPages = self.pdf.page_count
        return metadata, numPages

    def get_page(self, page_num):
        page = self.pdf.load_page(page_num)
        if self.zoom:
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat)
        else:
            pix = page.get_pixmap()
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        imgdata = px1.tobytes("ppm")
        return PhotoImage(data=imgdata)

    def get_text(self, page_num):
        page = self.pdf.load_page(page_num)
        text = page.getText('text')
        return text
