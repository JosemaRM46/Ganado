import cv2
import numpy as np
import os

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

def compare_images(query_image_path, reference_folder):
    # Cargar imagen de consulta
    query_image = cv2.imread(query_image_path, cv2.IMREAD_GRAYSCALE)
    if query_image is None:
        print("Error: No se pudo cargar la imagen de consulta.")
        return
    
    # Cargar imágenes de referencia
    ref_images, ref_filenames = load_images_from_folder(reference_folder)
    
    # Inicializar ORB detector
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
    else:
        print("No se encontraron coincidencias lo suficientemente buenas.")
    
if __name__ == "__main__":
    query_image_path = "imagenes/imagenes_comparar/images.jpg"
    reference_folder = "imagenes/imagenes_marcas/"
    compare_images(query_image_path, reference_folder)
