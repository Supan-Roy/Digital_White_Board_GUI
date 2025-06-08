from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
from PIL import ImageGrab
import os
import datetime

root = Tk()
root.title("Digital White Board")
root.geometry("1050x570+150+50")
root.config(bg="#f2f3f5")
root.resizable(False, False)

current_x = 0
current_y = 0
color = "black"
undo_stack = []
redo_stack = []
image_refs = []
image_id = None
filename = None


def locate_xy(work):
    global current_x, current_y
    current_x = work.x
    current_y = work.y

def addline(work):
    global current_x, current_y
    line = canvas.create_line((current_x, current_y, work.x, work.y), width=float(get_current_value()), fill=color, capstyle="round", smooth=True)
    undo_stack.append(line)
    redo_stack.clear()
    current_x, current_y = work.x, work.y

def show_color(new_color):
    global color
    color = new_color

def use_eraser():
    global color
    color = "white"

def new_canvas():
    canvas.delete("all")
    undo_stack.clear()
    redo_stack.clear()
    display_pallete()

selected_image_id = None
drag_data = {"x": 0, "y": 0}

def insertimage():
    global filename
    filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select Image",
        filetypes=(("PNG files", "*.png"), ("all files", "*.*"))
    )

    if filename:
        f_image = tk.PhotoImage(file=filename)
        image_refs.append(f_image)
        image_id = canvas.create_image(180, 50, image=f_image, anchor="nw")
        canvas.tag_bind(image_id, "<Button-1>", on_image_click)
        canvas.tag_bind(image_id, "<B1-Motion>", on_image_drag)

def on_image_click(event):
    global selected_image_id
    selected_image_id = canvas.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def on_image_drag(event):
    global drag_data, selected_image_id
    dx = event.x - drag_data["x"]
    dy = event.y - drag_data["y"]
    canvas.move(selected_image_id, dx, dy)
    drag_data["x"] = event.x
    drag_data["y"] = event.y

def move_image(event):
    global image_id
    canvas.coords(image_id, event.x, event.y)


def save_canvas():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"drawing_{timestamp}.png"

    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
    print(f"Canvas saved as {filename}")

def undo():
    if undo_stack:
        item = undo_stack.pop()
        canvas.delete(item)
        redo_stack.append(item)

def redo():
    if redo_stack:
        pass
def clear_screen():
    canvas.delete("all")
    undo_stack.clear()
    redo_stack.clear()
    image_refs.clear()
    display_pallete()

# Icon
image_icon = PhotoImage(file="materials/icon.png")
root.iconphoto(False, image_icon)

# Sidebar
color_box = PhotoImage(file="materials/color section.png")
Label(root, image=color_box, bg="#f2f3f5").place(x=10, y=20)

# Eraser
eraser = PhotoImage(file="materials/eraser.png")
Button(root, image=eraser, bg="#f2f3f5", command=use_eraser).place(x=30, y=400)

# Import Image
importImage = PhotoImage(file="materials/addimage.png")
Button(root, image=importImage, bg="white", command=insertimage).place(x=30, y=450)

# Save Canvas Button
save_icon = PhotoImage(file="materials/save.png")
Button(root, image=save_icon, bg="white", command=save_canvas).place(x=980, y=520)

# Clear Screen Button (left of Save)
clear_icon = PhotoImage(file="materials/clear.png")  # You can use any image you have
Button(root, image=clear_icon, bg="white", command=clear_screen).place(x=920, y=520)


# Undo and Redo Buttons (optional icons can be used)
Button(root, text="Undo", command=undo).place(x=30, y=300)
Button(root, text="Redo", command=redo).place(x=30, y=350)

# Colors section
colors = Canvas(root, bg="#fff", width="37", height=307, bd=0)
colors.place(x=30, y=60)

def display_pallete():
    palette = ["black", "gray", "brown4", "red", "orange", "yellow", "lightgreen", "green", "blue", "purple"]
    for i, col in enumerate(palette):
        y1 = 10 + i * 30
        y2 = y1 + 20
        rect = colors.create_rectangle((10, y1, 30, y2), fill=col)
        colors.tag_bind(rect, '<Button-1>', lambda e, c=col: show_color(c))

display_pallete()

# Main Canvas
canvas = Canvas(root, width=930, height=500, background="white", cursor="hand2")
canvas.place(x=100, y=10)
canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', addline)

# Slider
current_value = tk.DoubleVar()

def get_current_value():
    return '{:.2f}'.format(current_value.get())

def slider_changed(event):
    value_label.configure(text=get_current_value())

slider = ttk.Scale(root, from_=1, to=10, orient=HORIZONTAL, command=slider_changed, variable=current_value)
slider.place(x=53, y=530)

value_label = ttk.Label(root, text=get_current_value())
value_label.place(x=27, y=550)

root.mainloop()
