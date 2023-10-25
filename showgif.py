import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from screeninfo import get_monitors
import subprocess
import sys
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


def show_gif_on_screen(gif_path, screen_width, screen_height, x, y):
    root = tk.Tk()
    root.overrideredirect(True)

    # Set window size and position based on provided screen dimensions and coordinates
    root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

    gif = AnimatedGif(root, gif_path, screen_width, screen_height)
    gif.pack(expand=True, fill=tk.BOTH)

    # Auto-close after 5s
    root.after(5000, root.destroy)

    root.mainloop()


# ... [other imports]

# ... [rest of the code]

if __name__ == '__main__':
    # Path to the GIF you want to display
    gif_path = "path_to_your_gif.gif"

    # Get info about all connected monitors
    monitors = get_monitors()

    # Limiting the number of monitors for safety
    max_monitors = 2
    for monitor in monitors[:max_monitors]:
        try:
            # Spawn a new process to show GIF on each monitor
            cmd = ["python3", __file__, gif_path, str(monitor.width), str(
                monitor.height), str(monitor.x), str(monitor.y)]
            subprocess.Popen(cmd)

            # Introduce a delay
            time.sleep(2)
        except Exception as e:
            print(f"Error encountered: {e}")
            break
    else:
        # If this is a child process
        gif_path = sys.argv[1]
        screen_width = int(sys.argv[2])
        screen_height = int(sys.argv[3])
        x = int(sys.argv[4])
        y = int(sys.argv[5])
        show_gif_on_screen(gif_path, screen_width, screen_height, x, y)
