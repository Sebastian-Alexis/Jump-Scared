from PIL import Image, ImageTk
import tkinter as tk
import time


def update_image(label, frames, frame_idx):
    frame = frames[frame_idx]
    label.config(image=frame)
    label.image = frame
    label.after(frames[frame]['duration'], update_image,
                label, frames, (frame_idx + 1) % len(frames))


def show_gif(gif_path, duration):
    root = tk.Tk()
    root.overrideredirect(True)  # Removes the title bar
    # Places the window at the top left corner
    root.geometry("+{}+{}".format(0, 0))

    # Extract frames from GIF for animation
    with Image.open(gif_path) as img:
        frames = [{'image': ImageTk.PhotoImage(img.copy().convert(
            'RGBA')), 'duration': img.info['duration']} for _ in range(img.n_frames)]

    lbl = tk.Label(root)
    lbl.pack(fill=tk.BOTH, expand=tk.YES)

    # Start the GIF animation
    update_image(lbl, frames, 0)

    root.after(duration, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    duration = 5000
    show_gif("jumpscare_media/jumpscare.gif", duration)
