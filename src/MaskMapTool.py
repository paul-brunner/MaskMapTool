from tkinter import *
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import ImageTk, Image
import darkdetect
import sys
import os
import platform
import webbrowser

import map_creator

# variables for storing the paths leading to the maps
metallic_path = ""
occlusion_path = ""
detail_path = ""
smoothness_path = ""

# filetypes
files = [('png', '*.png')]

#
sizes = []

# Set color codes
if darkdetect.isDark():
    button_bg = "#d92121"
    background_color = "#121212"
    font_color = "#ffffff"
    textfield_bg = "#121212"
else:
    button_bg = "#ff4242"
    background_color = "#ededed"
    font_color = "#000000"
    textfield_bg = "#ededed"

background_color_rgb = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def resource_path(relative_path):
    # Thank you max: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# create the main application window
#root = Tk()
root = TkinterDnD.Tk()
root.title("Mask Map Tool")
root.geometry("600x400")
root.resizable(0, 0)
root.configure(background=background_color, borderwidth=10)
if platform.system() == "Windows":
    root.iconbitmap(resource_path("Assets/mask_icon.ico"))
elif platform.system() == "Linux":
    root.wm_iconphoto(True, PhotoImage(file=resource_path("Assets/mask_icon.png")))

# configure the grid

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)


def update_preview_image_label():
    global preview_image_label

    new_preview_image = map_creator.create_mask_map(metallic_path, occlusion_path, detail_path, smoothness_path)
    new_preview_image.thumbnail((128, 128))
    new_preview_photo = ImageTk.PhotoImage(new_preview_image)

    preview_image_label.destroy()
    preview_image_label = Label(root, image=new_preview_photo, width=128, height=128)
    preview_image_label.image = new_preview_photo
    preview_image_label.grid(row=4, column=2, rowspan=2)


def select_path(path):
    filepath = filedialog.askopenfile(mode="r", filetypes=files)

    if filepath is not None:
        filepath = str(filepath.name)
        change_path_update_preview(path, filepath)


def change_path_update_preview(path, filepath):
    global metallic_path, occlusion_path, detail_path, smoothness_path, files
    global metallic_image_label, occlusion_image_label, detail_image_label, smoothness_image_label
    global sizes

    try:
        new_Image = Image.open(filepath)
        new_Image.thumbnail((128, 128))
        new_Photo = ImageTk.PhotoImage(new_Image)

        sizes.append(new_Image.size)

        if all(x == sizes[0] for x in sizes):  # check if all images are of the same size
            if path == "metallic_path":
                metallic_path = filepath
                metallic_image_label.destroy()
                metallic_image_label = Label(root, image=new_Photo, width=128, height=128, bg=textfield_bg)
                metallic_image_label.image = new_Photo
                metallic_image_label.grid(row=1, column=0)
            elif path == "occlusion_path":
                occlusion_path = filepath
                occlusion_image_label.destroy()
                occlusion_image_label = Label(root, image=new_Photo, width=128, height=128, bg=textfield_bg)
                occlusion_image_label.image = new_Photo
                occlusion_image_label.grid(row=1, column=1)
            elif path == "detail_path":
                detail_path = filepath
                detail_image_label.destroy()
                detail_image_label = Label(root, image=new_Photo, width=128, height=128, bg=textfield_bg)
                detail_image_label.image = new_Photo
                detail_image_label.grid(row=1, column=2)
            elif path == "smoothness_path":
                smoothness_path = filepath
                smoothness_image_label.destroy()
                smoothness_image_label = Label(root, image=new_Photo, width=128, height=128, bg=textfield_bg)
                smoothness_image_label.image = new_Photo
                smoothness_image_label.grid(row=1, column=3)

            update_preview_image_label()
        else:
            messagebox.showerror("Error", "Image sizes must not differ from each other")

    except:
        messagebox.showinfo("Error", "Invalid filetype (This program only supports .png)")


def save_mask_map_as():
    global files

    if len(sizes) > 0:
        path = str(filedialog.asksaveasfilename(filetypes=files))
        if path:
            if path[-4:] != ".png":
                path += ".png"
            mask_map = map_creator.create_mask_map(metallic_path, occlusion_path, detail_path, smoothness_path)
            mask_map.save(path)


def clear_selected_maps():
    global metallic_path, occlusion_path, detail_path, smoothness_path
    global metallic_image_label, occlusion_image_label, detail_image_label, smoothness_image_label, preview_image_label
    global no_file_photo, preview_empty_photo
    global sizes

    metallic_path = ""
    occlusion_path = ""
    detail_path = ""
    smoothness_path = ""

    sizes = []

    metallic_image_label.destroy()
    metallic_image_label = Label(root, image=no_file_photo, width=128, height=128)
    metallic_image_label.image = no_file_photo
    metallic_image_label.drop_target_register(DND_FILES)
    metallic_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("metallic_path", e.data))
    metallic_image_label.grid(row=1, column=0)

    occlusion_image_label.destroy()
    occlusion_image_label = Label(root, image=no_file_photo, width=128, height=128)
    occlusion_image_label.image = no_file_photo
    occlusion_image_label.drop_target_register(DND_FILES)
    occlusion_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("occlusion_path", e.data))
    occlusion_image_label.grid(row=1, column=1)

    detail_image_label.destroy()
    detail_image_label = Label(root, image=no_file_photo, width=128, height=128)
    detail_image_label.image = no_file_photo
    detail_image_label.drop_target_register(DND_FILES)
    detail_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("detail_path", e.data))
    detail_image_label.grid(row=1, column=2)

    smoothness_image_label.destroy()
    smoothness_image_label = Label(root, image=no_file_photo, width=128, height=128)
    smoothness_image_label.image = no_file_photo
    smoothness_image_label.drop_target_register(DND_FILES)
    smoothness_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("smoothness_path", e.data))
    smoothness_image_label.grid(row=1, column=3)

    preview_image_label.destroy()
    preview_image_label = Label(root, image=preview_empty_photo, width=128, height=128)
    preview_image_label.image = preview_empty_photo
    preview_image_label.grid(row=4, column=2, rowspan=2)


# ----- create and place tkinter graphical interface objects on grid -----
no_file_image = Image.open(resource_path("Assets/no_file.png"))
no_file_photo = ImageTk.PhotoImage(no_file_image)

select_file_image = Image.open(resource_path("Assets/select_file_image.png"))
select_file_photo = ImageTk.PhotoImage(select_file_image)


# metallic text
metallic_label = Label(root, text="Metallic", bg=textfield_bg, fg=font_color)
metallic_label.grid(row=0, column=0)

# metallic image placeholder
metallic_image_label = Label(root, image=no_file_photo, width=128, height=128)
metallic_image_label.image = no_file_photo
metallic_image_label.drop_target_register(DND_FILES)
metallic_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("metallic_path", e.data))
metallic_image_label.grid(row=1, column=0)

# metallic select button
select_metallic_path_button = Button(root, bg=background_color, activebackground=background_color, borderwidth=0, width=128, height=38, image=select_file_photo, highlightthickness=0, command=lambda: select_path("metallic_path"))
select_metallic_path_button.drop_target_register(DND_FILES)
select_metallic_path_button.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("metallic_path", e.data))
select_metallic_path_button.grid(row=2, column=0, pady=1)


# occlusion text
occlusion_label = Label(root, text="Ambient Occlusion", bg=textfield_bg, fg=font_color)
occlusion_label.grid(row=0, column=1)

# occlusion image placeholder
occlusion_image_label = Label(root, image=no_file_photo, width=128, height=128)
occlusion_image_label.image = no_file_photo
occlusion_image_label.drop_target_register(DND_FILES)
occlusion_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("occlusion_path", e.data))
occlusion_image_label.grid(row=1, column=1)

# occlusion select button
select_occlusion_path_button = Button(root, bg=background_color, activebackground=background_color, borderwidth=0, width=128, height=38, image=select_file_photo, highlightthickness=0, command=lambda: select_path("occlusion_path"))
select_occlusion_path_button.drop_target_register(DND_FILES)
select_occlusion_path_button.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("occlusion_path", e.data))
select_occlusion_path_button.grid(row=2, column=1)


# detail text
normal_label = Label(root, text="Detail Mask", bg=textfield_bg, fg=font_color)
normal_label.grid(row=0, column=2)

# detail image placeholder
detail_image_label = Label(root, image=no_file_photo, width=128, height=128)
detail_image_label.image = no_file_photo
detail_image_label.drop_target_register(DND_FILES)
detail_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("detail_path", e.data))
detail_image_label.grid(row=1, column=2)

# detail select button
select_detail_path_button = Button(root, bg=background_color, activebackground=background_color, borderwidth=0, width=128, height=38, image=select_file_photo, highlightthickness=0, command=lambda: select_path("detail_path"))
select_detail_path_button.drop_target_register(DND_FILES)
select_detail_path_button.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("detail_path", e.data))
select_detail_path_button.grid(row=2, column=2)


# smoothness text
smoothness_label = Label(root, text="Smoothness", bg=textfield_bg, fg=font_color)
smoothness_label.grid(row=0, column=3)

# smoothness image placeholder
smoothness_image_label = Label(root, image=no_file_photo, width=128, height=128)
smoothness_image_label.image = no_file_photo
smoothness_image_label.drop_target_register(DND_FILES)
smoothness_image_label.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("smoothness_path", e.data))
smoothness_image_label.grid(row=1, column=3)

# smoothness select button
select_smoothness_path_button = Button(root, bg=background_color, activebackground=background_color, borderwidth=0, width=128, height=38, image=select_file_photo, highlightthickness=0, command=lambda: select_path("smoothness_path"))
select_smoothness_path_button.drop_target_register(DND_FILES)
select_smoothness_path_button.dnd_bind('<<Drop>>', lambda e: change_path_update_preview("smoothness_path", e.data))
select_smoothness_path_button.grid(row=2, column=3)


icon_image = Image.open(resource_path("Assets/mask_icon.png"))
icon_photo = ImageTk.PhotoImage(icon_image)
icon_image_label = Button(root, image=icon_photo, width=128, height=128, bg=background_color, activebackground=background_color, borderwidth=0, relief=SUNKEN, highlightthickness=0, command=lambda: webbrowser.open("https://github.com/WorldOfPaul/Mask-Map-Tool"))
icon_image_label.grid(row=4, column=0, rowspan=2, columnspan=2)

# mask map preview text
preview_label = Label(root, text="Mask Map Preview", bg=textfield_bg, fg=font_color)
preview_label.grid(row=3, column=2)

# mask map preview image placeholder
preview_empty_image = Image.new(mode="RGBA", size=(128, 128), color=background_color_rgb)
preview_empty_photo = ImageTk.PhotoImage(preview_empty_image)
preview_image_label = Label(root, image=preview_empty_photo, width=128, height=128)
preview_image_label.image = preview_empty_photo
preview_image_label.grid(row=4, column=2, rowspan=2)

# save mask map select button
save_button_image = Image.open(resource_path("Assets/save_button_image.png"))
save_button_photo = ImageTk.PhotoImage(save_button_image)
save_button = Button(root, bg=background_color, activebackground=background_color, borderwidth=0, width=128, height=60, image=save_button_photo, highlightthickness=0, command=lambda: save_mask_map_as())
save_button.photo = save_button_photo
save_button.grid(row=4, column=3)

# clear selection button
clear_button_image = Image.open(resource_path("Assets/clear_button_image.png"))
clear_button_photo = ImageTk.PhotoImage(clear_button_image)
clear_button = Button(root, bg=background_color, activebackground=background_color, borderwidth=0, width=128, height=60, image=clear_button_photo, highlightthickness=0, command=lambda: clear_selected_maps())
clear_button.photo = clear_button_photo
clear_button.grid(row=5, column=3)


root.mainloop()
