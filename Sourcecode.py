
import tkinter as tk
import random
import sys


MAX_WINDOWS = 100
STARTING_WINDOWS = 1
MOVE_DELAY_MS = 20
MIN_SPEED = 3
MAX_SPEED = 10
FLICKER_DELAY_MS = 500

windows = []
root = tk.Tk()
root.withdraw()

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

def close_all(event=None):
    for w in windows[:]:
        try:
            w.destroy()
        except Exception:
            pass
    windows.clear()
    try:
        root.quit()
    except Exception:
        pass
    sys.exit(0)

def spawn_window(x=None, y=None):
    if len(windows) >= MAX_WINDOWS:
        return None

    w = tk.Toplevel(root)
    w.overrideredirect(True)
    w.attributes('-topmost', True)
    w.resizable(False, False)

    W, H = 260, 90
    if x is None:
        x = random.randint(0, max(0, screen_w - W))
    if y is None:
        y = random.randint(0, max(0, screen_h - H))

    w.geometry(f"{W}x{H}+{x}+{y}")

    label = tk.Label(w,
                     text="YOU\nARE\nAN IDIOT",
                     font=("Impact", 28),
                     justify='center',
                     fg='white',
                     bg='black',
                     bd=4,
                     relief='raised')
    label.pack(fill='both', expand=True)
    w.label = label

    dx = random.choice([-1, 1]) * random.randint(MIN_SPEED, MAX_SPEED)
    dy = random.choice([-1, 1]) * random.randint(MIN_SPEED, MAX_SPEED)

    def on_left_click(ev):
        geom = w.geometry().split('+')
        cur_x = int(geom[1])
        cur_y = int(geom[2])
        spawn_window(cur_x + 20, cur_y + 20)

    def on_right_click(ev):
        try:
            windows.remove(w)
        except ValueError:
            pass
        w.destroy()

    def on_escape(ev):
        close_all()

    label.bind("<Button-1>", on_left_click)
    w.bind("<Button-1>", on_left_click)
    label.bind("<Button-3>", on_right_click)
    w.bind("<Button-3>", on_right_click)
    w.bind("<Escape>", on_escape)
    label.bind("<Escape>", on_escape)

   
    def move():
        nonlocal dx, dy
        try:
            geom = w.geometry().split('+')
            size = geom[0].split('x')
            cur_w = int(size[0])
            cur_h = int(size[1])
            cur_x = int(geom[1])
            cur_y = int(geom[2])
        except Exception:
            return

        nx = cur_x + dx
        ny = cur_y + dy

        if nx <= 0 or nx + cur_w >= screen_w:
            dx = -dx
        if ny <= 0 or ny + cur_h >= screen_h:
            dy = -dy

        try:
            w.geometry(f"{cur_w}x{cur_h}+{nx}+{ny}")
        except Exception:
            return

        if w.winfo_exists():
            w.after(MOVE_DELAY_MS, move)
        else:
            try:
                windows.remove(w)
            except ValueError:
                pass

    
    def flicker():
        if not w.winfo_exists():
            return
        current_bg = label.cget("bg")
        if current_bg == "black":
            label.config(bg="white", fg="black")
        else:
            label.config(bg="black", fg="white")
        w.after(FLICKER_DELAY_MS, flicker)

    windows.append(w)
    w.after(10, move)
    w.after(FLICKER_DELAY_MS, flicker)
    return w

def main():
    for _ in range(STARTING_WINDOWS):
        spawn_window()
    try:
        root.mainloop()
    except KeyboardInterrupt:
        close_all()

if __name__ == "__main__":
    main()

