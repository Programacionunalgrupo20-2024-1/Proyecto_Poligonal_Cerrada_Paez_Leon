import tkinter as tk
from tkinter import ttk

def agregar_fila():
    # Obtener los datos de las entradas
    datos = [entry.get() for entry in entries]
    
    # Insertar una nueva fila en la tabla del frame derecho
    tree.insert("", "end", values=datos)
    
    # Limpiar las entradas después de agregar la fila
    for entry in entries:
        entry.delete(0, tk.END)

def eliminar_fila():
    # Obtener el ID de la última fila
    last_item = tree.get_children()[-1] if tree.get_children() else None
    
    if last_item:
        # Eliminar la última fila
        tree.delete(last_item)

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz con Frame a la Izquierda")

# Configurar la ventana para que se abra en pantalla completa
root.state('zoomed')  # Maximiza la ventana en Windows

# Crear un frame principal que ocupe toda la ventana
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky='nsew')

# Crear un frame para el grupo de casillas en la parte superior de la ventana
left_frame = tk.Frame(main_frame, bg="lightgrey")
left_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

# Crear un frame vacío para el resto de la ventana
right_frame = tk.Frame(main_frame, bg="white")
right_frame.grid(row=1, column=0, sticky='nsew')  # Ocupa el resto de la ventana

# Ajustar el peso de las filas y columnas para que el frame izquierdo ocupe la mitad superior
main_frame.grid_rowconfigure(0, weight=1)  # Fila superior
main_frame.grid_rowconfigure(1, weight=1)  # Fila inferior
main_frame.grid_columnconfigure(0, weight=1)

# Etiquetas y campos de texto en el frame izquierdo
labels = ["Delta", "Punto", "Ángulo", "Distancia", "Observación"]
entries = []

# Crear las etiquetas en la parte superior y los campos de texto en la parte inferior
for idx, label in enumerate(labels):
    tk.Label(left_frame, text=label, bg="lightgrey").grid(row=0, column=idx, padx=5, pady=5, sticky='ew')
    entry = tk.Entry(left_frame)
    entry.grid(row=1, column=idx, padx=5, pady=5, sticky='ew')
    entries.append(entry)

# Crear el frame para los botones y centrarlo en el frame izquierdo
button_frame = tk.Frame(left_frame, bg="lightgrey")
button_frame.grid(row=2, column=0, columnspan=len(labels), pady=10, sticky='ew')
button_frame.grid_columnconfigure(0, weight=1)  # Asegura que el botón se centre en la columna

# Crear los botones dentro del frame de botones
add_button = tk.Button(button_frame, text="Agregar Fila", command=agregar_fila)
add_button.pack(side="left", padx=5, pady=5, expand=True)

remove_button = tk.Button(button_frame, text="Eliminar Fila", command=eliminar_fila)
remove_button.pack(side="left", padx=5, pady=5, expand=True)

# Centrar el frame de botones en el frame izquierdo
left_frame.grid_rowconfigure(2, weight=0)  # Fila de botones no se expande
left_frame.grid_columnconfigure(0, weight=1)  # Columna de botones se expande

# Ajustar el peso de las columnas del frame izquierdo para que los campos de texto y los botones se expandan
for idx in range(len(labels)):
    left_frame.grid_columnconfigure(idx, weight=1)

# Crear la tabla (Treeview) en el frame derecho
tree = ttk.Treeview(right_frame, columns=labels, show='headings')
tree.grid(row=0, column=0, sticky='nsew')

# Definir los encabezados de la tabla
for label in labels:
    tree.heading(label, text=label)
    tree.column(label, width=150, anchor=tk.CENTER)

# Ajustar el peso de la columna para que la tabla se expanda
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(0, weight=1)

# Ejecutar el loop principal de la ventana
root.mainloop()
