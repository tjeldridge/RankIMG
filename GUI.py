import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font


class GUI:
    def __init__(self, image_one: str, image_two: str, title: str = "Select Best Image"):
        self.root = tk.Tk()
        self.image1 = Image.open(image_one)
        self.image2 = Image.open(image_two)
        self.title = title
        self.button_pressed = None

    def __enter__(self):
        self.generate_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(exc_type, exc_val, exc_tb)

    def generate_window(self):
        self.root.title(self.title)

        # get the image sizes
        self.image1 = check_and_resize(self.image1)
        self.image2 = check_and_resize(self.image2)
        w1, h1 = self.image1.size
        w2, h2 = self.image2.size
        h = max([h1, h2]) + 100

        # position coordinates of root 'upper left corner'
        x = 0
        y = 0

        # make the root window the size of the image
        self.root.geometry("%dx%d+%d+%d" % (w1 + w2, h, x, y))

        # Generate Frames
        topframe = tk.Frame(self.root)
        topframe.pack(side=tk.TOP)
        bottomframe = tk.Frame(self.root)
        bottomframe.pack(side=tk.BOTTOM)

        # button images
        button1img = ImageTk.PhotoImage(self.image1)
        button2img = ImageTk.PhotoImage(self.image2)
        # buttons
        button1 = tk.Button(topframe, image=button1img, command=lambda: self.select("One"))
        button2 = tk.Button(topframe, image=button2img, command=lambda: self.select("Two"))
        button3 = tk.Button(bottomframe, text="Tie", width=w1+w2, height=50, command=lambda: self.select("Three"))
        # button 3 font
        buttonfont = font.Font(size=50, weight="bold")
        button3['font'] = buttonfont
        # pack buttons
        button1.pack(side=tk.LEFT, anchor="nw", fill=tk.NONE, expand=tk.NO)
        button2.pack(side=tk.RIGHT, anchor="ne", fill=tk.NONE, expand=tk.NO)
        button3.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        # generate window
        self.root.mainloop()

    def select(self, x):
        self.button_pressed = x
        self.root.destroy()


def check_dimension(val: int, maxval: int = 800):
    if val > maxval:
        return maxval
    else:
        return val


def check_and_resize(image: Image.open):
    init_w, init_h = image.size
    ratio = init_w / init_h
    temp_w = check_dimension(init_w, maxval=600)
    temp_h = int(temp_w // ratio)
    h = check_dimension(temp_h, maxval=800)
    w = int(ratio * h)
    if any([init_w != w, init_h != h]):
        image = image.resize((w, h), Image.ANTIALIAS)
    return image

# End
