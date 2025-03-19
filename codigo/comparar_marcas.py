import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, Label
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
    img1 = Image.open(query_image_path).resize((400, 400))
    img1 = ImageTk.PhotoImage(img1)
    
    label1 = Label(root, image=img1)
    label1.image = img1
    label1.grid(row=0, column=0)
    
    for i, (filename, ref_img, match_count) in enumerate(matches):
        img2 = Image.fromarray(ref_img).resize((400, 400))
        img2 = ImageTk.PhotoImage(img2)
        
        label2 = Label(root, image=img2, text=f"{filename} ({match_count} coincidencias)", compound=tk.TOP)
        label2.image = img2
        label2.grid(row=0, column=i+1)
    
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
