from UI.PDF.PDFViewer import PDFViewer
from UI.PDF.WindowSetup import setup_window


def main():
    root = setup_window()
    app = PDFViewer(root)
    root.mainloop()


if __name__ == '__main__':
    main()
