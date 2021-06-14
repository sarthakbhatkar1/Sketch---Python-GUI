import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter.filedialog import askopenfile
import PIL
import numpy as np
import imageio
import scipy.ndimage
import cv2
from tkinter import filedialog

root = tk.Tk()
root.title("Image2Sketch")
root.configure(bg='#696969')
canvas = tk.Canvas(root, width=600, height=700)
canvas.grid(columnspan=3, rowspan=6)

# functions required 
def rgb2gray(rgb):
	return np.dot(rgb[..., :3], [0.2989, 0.5870, .1140])

def dodge(front, back):
	final_sketch = front*255/(255-back)
	final_sketch[final_sketch > 255] = 255
	final_sketch[back == 255] = 255
	return final_sketch.astype('uint8')

def sketch(image):
    gray = rgb2gray(image)
    i = 255 - gray
    blur = scipy.ndimage.filters.gaussian_filter(i, sigma=13)
    r = dodge(blur, gray)
    return r

def open_file():
    browse_text.set("LOADING")
    file = askopenfile(parent=root, mode='rb', title="Choose an Image", filetype=[
                       ('image files', '.png'), ('image files', '.jpg'), ('image files', '.jpeg')])
    if file:
        browse_text.set("FILE LOADED")
        image = imageio.imread(file)
        new_img = sketch(image)
        global save_image
        save_image = new_img
        new_img = ImageTk.PhotoImage(image=PIL.Image.fromarray(new_img))
        new_img_label = tk.Label(image=new_img)
        new_img_label.image = new_img
        new_img_label.grid(columnspan=3, column=1, row=5)

def save_img():
    global save_image
    save_image = Image.fromarray(save_image)
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    save_image.save(filename)
    save_text.set("SAVED")


# logo
logo = Image.open('Images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

# Instructions
instruction = tk.Label(root, text="Select an Image", font="Raleway")
instruction.grid(columnspan=3, column=0, row=1)

# Browse button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: open_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=1, row=1)

# Save button
save_text = tk.StringVar()
save_btn = tk.Button(root, textvariable=save_text, command=lambda: save_img(
), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
save_text.set("Save")
save_btn.grid(column=1, row=4)
root.mainloop()
