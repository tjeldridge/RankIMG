from os import listdir
from random import shuffle
import tkinter as tk
from tkinter import filedialog


class OpenDir:
    def __init__(self, directory: str = None):
        self.directory = select_directory(directory)
        self.allfiles = []
        self.randomfiles = []
        self.run()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run(self):
        self.find_img_type(".png")
        self.find_img_type(".jpg")
        self.randomize()

    def find_img_type(self, extension: str = ".jpg"):
        extlen = len(extension)
        allfiles = listdir(self.directory)
        self.allfiles.extend([file for file in allfiles if file[-extlen:] == extension])

    def randomize(self):
        self.randomfiles = self.allfiles.copy()
        shuffle(self.randomfiles)
        return self.randomfiles


def checkslash(directory: str):
    if directory[-1:] == "/":
        fixed_dir = directory
    else:
        fixed_dir = directory + "/"
    return fixed_dir


def select_directory(directory: str = None):
    if directory is None:
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        root.destroy()
    return directory

# End
