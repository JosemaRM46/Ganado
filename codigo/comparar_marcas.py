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
    best_match = None
    best_match_count = 0
    best_filename = ""
    
    for ref_img, filename in zip(ref_images, ref_filenames):
        kp2, des2 = orb.detectAndCompute(ref_img, None)
        if des2 is None:
            continue
        
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        
        if len(matches) > best_match_count:
            best_match_count = len(matches)
            best_match = ref_img
            best_filename = filename
    
    if best_match is not None:
        print(f"La mejor coincidencia es: {best_filename} con {best_match_count} coincidencias.")
        show_results(query_image_path, os.path.join(reference_folder, best_filename), root)
    else:
        print("No se encontraron coincidencias lo suficientemente buenas.")

def show_results(query_image_path, best_match_path, root):
    img1 = Image.open(query_image_path).resize((400, 400))
    img2 = Image.open(best_match_path).resize((400, 400))
    
    img1 = ImageTk.PhotoImage(img1)
    img2 = ImageTk.PhotoImage(img2)
    
    label1 = Label(root, image=img1)
    label1.image = img1
    label1.grid(row=0, column=0)
    
    label2 = Label(root, image=img2)
    label2.image = img2
    label2.grid(row=0, column=1)
    
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
