from tkinter import Menu


def create_menu(master, open_file_command):
    menu = Menu(master)
    master.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="Settings", menu=filemenu)
    filemenu.add_command(label="Open File", command=open_file_command)
    filemenu.add_command(label="Exit", command=master.destroy)
    return menu
