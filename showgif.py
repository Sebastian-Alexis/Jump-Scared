import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from screeninfo import get_monitors
import time


class AnimatedGif(tk.Label):
    def __init__(self, master, path, screen_width, screen_height):
        im = Image.open(path)
        seq = []

        # Process each frame and resize
        for i in range(im.n_frames):
            # Resize frame to screen size
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


def show_gif_on_screen(master, gif_path, screen_width, screen_height, x, y):
    master.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
    gif = AnimatedGif(master, gif_path, screen_width, screen_height)
    gif.pack(expand=True, fill=tk.BOTH)
    master.after(5000, master.destroy)  # Auto-close after 5s


if __name__ == '__main__':
    gif_path = "jumpscare_media/jumpscare.gif"

    root = tk.Tk()
    root.withdraw()  # Hide the main root window

    monitors = get_monitors()
    windows = []

    for monitor in monitors:
        window = tk.Toplevel(root)
        window.withdraw()  # Hide the window initially
        windows.append(window)
        show_gif_on_screen(window, gif_path, monitor.width,
                           monitor.height, monitor.x, monitor.y)

    # Simulate some delay or your logic here
    time.sleep(5)  # For example, after 3 seconds, show all the windows

    for window in windows:
        window.deiconify()  # Show the window

    root.mainloop()
