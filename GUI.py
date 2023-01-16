import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font


class GUI:
    def __init__(self, image_one: str, image_two: str):
        self.root = tk.Tk()
        self.image1 = ImageTk.PhotoImage(Image.open(image_one))
        self.image2 = ImageTk.PhotoImage(Image.open(image_two))
        self.image1_score = 0.5
        self.image2_score = 0.5

    def __enter__(self):
        self.generate_window()
        return self.image1_score, self.image2_score

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(exc_type, exc_val, exc_tb)

    def generate_window(self):
        self.root.title('Select Best Image')

        # get the image sizes
        w1 = self.image1.width()
        h1 = self.image1.height()
        w2 = self.image2.width()
        h2 = self.image2.height()
        h = max([h1, h2]) + 100

        # position coordinates of root 'upper left corner'
        x = 0
        y = 0

        # make the root window the size of the image
        self.root.geometry("%dx%d+%d+%d" % (w1 + w2, h, x, y))

        topframe = tk.Frame(self.root)
        topframe.pack(side=tk.TOP)
        bottomframe = tk.Frame(self.root)
        bottomframe.pack(side=tk.BOTTOM)

        # root has no image argument, so use a label as a panel
        panel1 = tk.Button(topframe, image=self.image1, command=lambda: self.select(1))
        panel2 = tk.Button(topframe, image=self.image2, command=lambda: self.select(2))
        button3 = tk.Button(bottomframe, text="Tie", width=w1+w2, height=50, command=lambda: self.select(3))
        buttonfont = font.Font(size=50, weight="bold")
        button3['font'] = buttonfont
        # self.display = self.image1
        panel1.pack(side=tk.LEFT, anchor="nw", fill=tk.NONE, expand=tk.NO)
        panel2.pack(side=tk.RIGHT, anchor="ne", fill=tk.NONE, expand=tk.NO)
        button3.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        self.root.mainloop()

    def select(self, x):
        if x == 1:
            self.image1_score = 1
            self.image2_score = 0
        elif x == 2:
            self.image1_score = 0
            self.image2_score = 1
        else:
            self.image1_score = 0.5
            self.image2_score = 0.5
        self.root.destroy()


def main():
    imageFile = "01584-3235428827-masterpiece, best quality, art by granblue fantasy, (masterpiece_1.2)," \
                " (intricate_details_1.2), colorful, beautiful hair, detail.png"
    with GUI(imageFile, imageFile) as app:
        print(app)


if __name__ == '__main__':
    main()
