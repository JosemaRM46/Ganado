import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, Label, Canvas, Scrollbar, Frame
from PIL import Image, ImageTk

def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
            filenames.append(filename)
    return images, filenames

def compare_images(query_image_path, reference_folder, root):
    query_image = cv2.imread(query_image_path, cv2.IMREAD_GRAYSCALE)
    if query_image is None:
        print("Error: No se pudo cargar la imagen de consulta.")
        return
    
    ref_images, ref_filenames = load_images_from_folder(reference_folder)
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(query_image, None)
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    match_results = []
    
    for ref_img, filename in zip(ref_images, ref_filenames):
        kp2, des2 = orb.detectAndCompute(ref_img, None)
        if des2 is None:
            continue
        
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        
        match_percentage = len(matches) / len(kp1) if len(kp1) > 0 else 0
        
        if match_percentage >= 0.8:
            match_results.append((filename, ref_img, len(matches)))
    
    match_results.sort(key=lambda x: x[2], reverse=True)
    
    if match_results:
        show_results(query_image_path, match_results, root)
    else:
        print("No se encontraron coincidencias superiores al 80%.")

def show_results(query_image_path, matches, root):
    num_images = len(matches)
    if num_images == 1:
        window_width = 250
    elif num_images == 2:
        window_width = 480
    elif num_images == 3:
        window_width = 750
    elif num_images >= 4:
        window_width = 1000
    else:
        window_width = 1200
    
    root.geometry(f"{window_width}x550")
    
    canvas = Canvas(root)
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    img_query = Image.open(query_image_path).resize((200, 200))
    img_query = ImageTk.PhotoImage(img_query)
    
    label_query = Label(scrollable_frame, image=img_query, text="Imagen de consulta", compound=tk.TOP)
    label_query.image = img_query
    label_query.grid(row=0, column=0, columnspan=4, pady=10)
    label_titulo = Label(scrollable_frame, text="Imágenes que coinciden:", font=("Arial", 12, "bold"))
    label_titulo.grid(row=1, column=0, columnspan=4, pady=10)
    max_cols = 4
    
    for i, (filename, ref_img, match_count) in enumerate(matches):
        img = Image.fromarray(ref_img).resize((200, 200))
        img = ImageTk.PhotoImage(img)
        
        row = (i // max_cols) + 2
        col = i % max_cols
        
        label = Label(scrollable_frame, image=img, text=f"{filename} ({match_count} coincidencias)", compound=tk.TOP)
        label.image = img
        label.grid(row=row, column=col, padx=10, pady=10)
    
    root.mainloop()

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        root.deiconify()
        compare_images(file_path, "imagenes/imagenes_marcas/", root)

if __name__ == "__main__":
    select_image()