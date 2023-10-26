import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from screeninfo import get_monitors


class AnimatedGif(tk.Label):
    # A label that displays an animated GIF using the Pillow library
    def __init__(self, master, path, screen_width, screen_height):
        im = Image.open(path)
        seq = []
        for i in range(im.n_frames):
            resized_frame = im.copy().resize((screen_width, screen_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_frame)
            im.seek(i)
            seq.append((photo, im.info['duration']))
        self.frames = seq

        tk.Label.__init__(self, master, image=seq[0][0])
        self.image = seq[0][0]
        self.idx = 0
        self.cancel = None
        self.animation()

    def animation(self):
        self.config(image=self.frames[self.idx][0])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.frames[self.idx][1], self.animation)


def show_gif(gif_path):
    # Get the primary monitor's width and height
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height

    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    gif = AnimatedGif(root, gif_path, screen_width, screen_height)
    gif.pack(expand=True, fill=tk.BOTH)

    # Close after 4 seconds
    root.after(4000, root.destroy)

    root.mainloop()


if __name__ == '__main__':
    gif_path = "jumpscare_media/jumpscare.gif"
    show_gif(gif_path)
