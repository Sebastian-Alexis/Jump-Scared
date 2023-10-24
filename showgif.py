import tkinter as tk
from PIL import Image, ImageTk


class AnimatedGif(tk.Label):
    def __init__(self, master, path):
        im = Image.open(path)
        seq = []

        # Screen dimensions
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Process each frame and resize
        for i in range(im.n_frames):
            # Resize frame to screen size
            resized_frame = im.copy().resize((screen_width, screen_height), Image.ANTIALIAS)
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
    root = tk.Tk()
    root.overrideredirect(True)

    # Fullscreen mode
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    gif = AnimatedGif(root, gif_path)
    gif.pack(expand=True, fill=tk.BOTH)

    # Auto-close after 5s
    root.after(5000, root.destroy)

    root.mainloop()


if __name__ == "__main__":
    # TODO: Add arg parser for gif_path later?
    show_gif("jumpscare_media/jumpscare.gif")
