import tkinter as tk
from tkinter import ttk, messagebox
from math import fabs, atan, degrees
from calculos import decimal_a_dms, determinar_cuadrante, calcular_azimut

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz con Frame a la Izquierda")
        self.root.state('zoomed')

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        self.contenedor_superior = tk.Frame(self.main_frame, bg="lightgrey", bd=2, relief="solid")
        self.contenedor_superior.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 0))

        self.column_labels = ["Punto", "Norte", "Este", "Ángulo", "Cuadrante", "Azimut"]
        self._create_superior_container()

        self.left_frame = tk.Frame(self.main_frame, bg="lightgrey", bd=2, relief="solid")
        self.left_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))

        self.right_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="solid")
        self.right_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=(0, 10))

        self._create_left_frame()
        self._create_right_frame()

    def _create_superior_container(self):
        for i in range(len(self.column_labels)):
            self.contenedor_superior.grid_columnconfigure(i, weight=1)

        titulo_label = tk.Label(self.contenedor_superior, text="Azimut General", bg="lightgrey", font=("Arial", 12, "bold"))
        titulo_label.grid(row=0, column=0, columnspan=len(self.column_labels), pady=(5, 10), sticky='ew')

        for idx, label in enumerate(self.column_labels):
            label_widget = tk.Label(self.contenedor_superior, text=label, bg="lightgrey")
            label_widget.grid(row=1, column=idx, padx=5, pady=5, sticky='ew')

        self.top_entries = [None] * (2 * len(self.column_labels))  # Inicializa con None, suficiente para ambas filas
        for idx, label in enumerate(self.column_labels):
            if label in ["Punto", "Norte", "Este"]:
                entry = tk.Entry(self.contenedor_superior, width=20)
                entry.grid(row=2, column=idx, padx=5, pady=(0, 5), sticky='ew')
                self.top_entries[idx] = entry

                entry = tk.Entry(self.contenedor_superior, width=20)
                entry.grid(row=3, column=idx, padx=5, pady=(0, 5), sticky='ew')
                self.top_entries[len(self.column_labels) + idx] = entry

        self.diferencia_norte_label = tk.Label(self.contenedor_superior, text="Diferencia Norte", bg="lightgrey")
        self.diferencia_norte_label.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        self.diferencia_este_label = tk.Label(self.contenedor_superior, text="Diferencia Este", bg="lightgrey")
        self.diferencia_este_label.grid(row=4, column=2, padx=5, pady=5, sticky='ew')

        self.diferencia_norte_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey")
        self.diferencia_norte_value_label.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

        self.diferencia_este_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey")
        self.diferencia_este_value_label.grid(row=5, column=2, padx=5, pady=5, sticky='ew')

        self.angulo_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey")
        self.angulo_value_label.grid(row=2, column=3, padx=5, pady=5, sticky='ew')

        self.cuadrante_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey")
        self.cuadrante_label.grid(row=2, column=4, padx=5, pady=5, sticky='ew')

        self.azimut_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey")
        self.azimut_label.grid(row=2, column=5, padx=5, pady=5, sticky="ew")

        calcular_button = tk.Button(self.contenedor_superior, text="Calcular Diferencias", command=self.calcular_diferencias)
        calcular_button.grid(row=7, column=0, columnspan=len(self.column_labels), pady=10, sticky='ew')

    def _create_left_frame(self):
        tk.Label(self.left_frame, text="Cartera de campo", bg="lightgrey", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=6, pady=(5, 10), sticky='ew')

        # Configura la columna para que se expanda
        self.left_frame.grid_columnconfigure(0, weight=1)
        for col in range(1, 6):
            self.left_frame.grid_columnconfigure(col, weight=1)

        labels = ["Delta", "Punto", "Angulo OBS", "Distancia", "Observación"]
        self.left_entries = [None] * len(labels)  # Inicializa con None

        for idx, label in enumerate(labels):
            tk.Label(self.left_frame, text=label, bg="lightgrey").grid(row=1, column=idx, padx=5, pady=5, sticky='ew')
            entry = tk.Entry(self.left_frame)
            entry.grid(row=2, column=idx, padx=5, pady=5, sticky='ew')
            self.left_entries[idx] = entry

        button_frame = tk.Frame(self.left_frame, bg="lightgrey")
        button_frame.grid(row=3, column=0, columnspan=len(labels), pady=10, sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)

        add_button = tk.Button(button_frame, text="Agregar Fila", command=self.agregar_fila)
        add_button.pack(side="left", padx=5, pady=5, expand=True)

        remove_button = tk.Button(button_frame, text="Eliminar Fila", command=self.eliminar_fila)
        remove_button.pack(side="left", padx=5, pady=5, expand=True)

    def _create_right_frame(self):
        labels = ["Delta", "Punto", "Angulo OBS", "Distancia", "Observación"]
        self.tree = ttk.Treeview(self.right_frame, columns=labels, show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')

        for label in labels:
            self.tree.heading(label, text=label)
            self.tree.column(label, width=150, anchor=tk.CENTER)

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)

    def calcular_diferencias(self):
        try:
            norte_1 = float(self.top_entries[1].get())
            norte_2 = float(self.top_entries[7].get())
            este_1 = float(self.top_entries[2].get())
            este_2 = float(self.top_entries[8].get())

            diferencia_norte = norte_2 - norte_1
            diferencia_este = este_2 - este_1

            self.diferencia_norte_value_label.config(text=f"{diferencia_norte}")
            self.diferencia_este_value_label.config(text=f"{diferencia_este}")

            cuadrante = determinar_cuadrante(diferencia_este, diferencia_norte)
            self.cuadrante_label.config(text=f"{cuadrante}")

            if fabs(diferencia_norte) != 0:
                angulo_rad = atan(fabs(diferencia_este) / fabs(diferencia_norte))
                angulo_deg = degrees(angulo_rad)

                grados, minutos, segundos = decimal_a_dms(angulo_deg)
                self.angulo_value_label.config(text=f"{grados}° {minutos}′ {segundos:.2f}″")

                azimut = calcular_azimut(cuadrante, angulo_deg)
                azimut_grados, azimut_minutos, azimut_segundos = decimal_a_dms(azimut)
                self.azimut_label.config(text=f"{azimut_grados}° {azimut_minutos}′ {azimut_segundos:.2f}″")
            else:
                self.angulo_value_label.config(text="Indefinido")
                self.azimut_label.config(text="Indefinido")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos en las entradas de texto.")

    def agregar_fila(self):
        # Obtiene los datos de las entradas de texto en el left_frame
        datos = [entry.get() for entry in self.left_entries]

        print("Datos a agregar:", datos)

        # Verifica que todos los campos de entrada tengan un valor
        if all(datos):
            # Agrega una fila al Treeview con los datos
            self.tree.insert("", "end", values=datos)
        
            # Limpia los campos de texto después de agregar la fila
            for entry in self.left_entries:
                entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor, rellene todos los campos en la fila.")

    def eliminar_fila(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna fila para eliminar.")
