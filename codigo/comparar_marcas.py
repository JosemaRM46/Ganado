import cv2
import os
import tkinter as tk
from tkinter import filedialog, Label, Canvas, Scrollbar, Frame, Button, Entry
from PIL import Image, ImageTk

def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):  # Filtrar solo imágenes
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
                filenames.append(filename)
    return images, filenames

def load_image_info(image_filename, folder):
    txt_filename = os.path.splitext(image_filename)[0] + ".txt"
    txt_path = os.path.join(folder, txt_filename)
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            return f.read()
    return "ID: Desconocido\nNombre: Desconocido"

def compare_images(query_image_path, reference_folder, root, threshold):
    query_image = cv2.imread(query_image_path, cv2.IMREAD_GRAYSCALE)
    if query_image is None:
        print("Error: No se pudo cargar la imagen de consulta.")
        return
    
    ref_images, ref_filenames = load_images_from_folder(reference_folder)
    orb = cv2.ORB_create(nfeatures=1000)
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
        
        if match_percentage >= threshold:
            info = load_image_info(filename, reference_folder)
            match_results.append((filename, ref_img, len(matches), info))
    
    match_results.sort(key=lambda x: x[2], reverse=True)
    
    show_results(query_image_path, match_results, root, threshold)

def show_results(query_image_path, matches, root, threshold):
    for widget in root.winfo_children():
        widget.destroy()

    frame_top = Frame(root)
    frame_top.pack(anchor="nw", padx=10, pady=10)
    
    btn_select_new = Button(frame_top, text="Seleccionar otra imagen", command=select_image)
    btn_select_new.pack(side="left", padx=5)
    
    global entry_threshold
    entry_threshold = Entry(frame_top, width=5)
    entry_threshold.pack(side="left", padx=5)
    entry_threshold.delete(0, tk.END)
    entry_threshold.insert(0, str(threshold))
    
    label_threshold = Label(frame_top, text="Nivel de coincidencia")
    label_threshold.pack(side="left", padx=5)
    
    canvas = Canvas(root)
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    scrollable_frame.images = []
    
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    img_query = Image.open(query_image_path).resize((200, 200))
    img_query = ImageTk.PhotoImage(img_query)
    scrollable_frame.images.append(img_query)
    
    label_query = Label(scrollable_frame, image=img_query, text="Imagen de consulta", compound=tk.TOP)
    label_query.image = img_query
    label_query.grid(row=0, column=0, columnspan=4, pady=10)
    
    label_titulo = Label(scrollable_frame, text="Imágenes que coinciden:", font=("Arial", 12, "bold"))
    label_titulo.grid(row=1, column=0, columnspan=4, pady=10)
    
    max_cols = 2
    for i, (filename, ref_img, match_count, info) in enumerate(matches):
        img = Image.fromarray(ref_img).resize((200, 200))
        img = ImageTk.PhotoImage(img)
        scrollable_frame.images.append(img)
        
        row = (i // max_cols) * 2 + 2
        col = i % max_cols
        
        label = Label(scrollable_frame, image=img, text=f"{filename} ({match_count} coincidencias)", compound=tk.TOP)
        label.image = img
        label.grid(row=row, column=col, padx=10, pady=10)
        
        label_info = Label(scrollable_frame, text=info, font=("Arial", 10))
        label_info.grid(row=row + 1, column=col, padx=10, pady=5)

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            threshold = float(entry_threshold.get())
        except ValueError:
            threshold = 0.95
        compare_images(file_path, "imagenes/imagenes_marcas/", root, threshold)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Comparador de imágenes")
    
    frame_top = Frame(root)
    frame_top.pack(anchor="nw", padx=10, pady=10)
    
    btn_select = Button(frame_top, text="Seleccionar imagen", command=select_image)
    btn_select.pack(side="left", padx=5)
    
    entry_threshold = Entry(frame_top, width=5)
    entry_threshold.pack(side="left", padx=5)
    entry_threshold.insert(0, "0.95")
    
    label_threshold = Label(frame_top, text="Nivel de coincidencia")
    label_threshold.pack(side="left", padx=5)
    
    root.mainloop()
