import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Ruta de la carpeta donde se guardarán las imágenes y archivos txt
CARPETA_DESTINO = "imagenes/imagenes_marcas"

# Función para seleccionar una imagen y guardar con la info
def guardar_imagen():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.png;*.jpeg")])
    if not ruta_imagen:
        return
    
    # Pedir ID y nombre del dueño
    id_dueño = entry_id.get().strip()
    nombre_dueño = entry_nombre.get().strip()
    
    if not id_dueño or not nombre_dueño:
        messagebox.showerror("Error", "Debe ingresar ID y Nombre del dueño")
        return
    
    # Crear el nuevo nombre de archivo
    extension = os.path.splitext(ruta_imagen)[1]
    nuevo_nombre = f"{id_dueño}{extension}"
    destino_imagen = os.path.join(CARPETA_DESTINO, nuevo_nombre)
    
    # Copiar la imagen a la carpeta destino
    shutil.copy(ruta_imagen, destino_imagen)
    
    # Crear el archivo de texto con la información
    destino_txt = os.path.join(CARPETA_DESTINO, f"{id_dueño}.txt")
    with open(destino_txt, "w") as f:
        f.write(f"ID: {id_dueño}\n")
        f.write(f"Nombre: {nombre_dueño}\n")
    
    messagebox.showinfo("Éxito", "Imagen y datos guardados correctamente")
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Registrar Imagen de Marca")

# Etiquetas y campos de entrada
tk.Label(root, text="ID del Ganado:").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Nombre del Dueño:").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack()

# Botón para seleccionar imagen
tk.Button(root, text="Seleccionar Imagen y Guardar", command=guardar_imagen).pack()

# Ejecutar la aplicación
root.mainloop()
