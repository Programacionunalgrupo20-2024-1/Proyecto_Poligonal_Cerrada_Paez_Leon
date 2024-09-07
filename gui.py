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
        self.contenedor_superior.grid(row=0, column=0, sticky='ew', padx=5, pady=(5, 0))

        self.column_labels = ["Punto", "Norte", "Este", "Ángulo", "Cuadrante", "Azimut"]
        self._create_superior_container()

        self.left_frame = tk.Frame(self.main_frame, bg="lightgrey", bd=2, relief="solid")
        self.left_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=(0, 5))

        self.right_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="solid")
        self.right_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=(0, 5))

        self._create_left_frame()
        self._create_right_frame()

    def _create_superior_container(self):
        # Configura las columnas con peso para ajustar el tamaño
        for i in range(len(self.column_labels)):
            self.contenedor_superior.grid_columnconfigure(i, weight=1)

        # Configura las filas con peso bajo para ajustar el tamaño
        for i in range(8):
            self.contenedor_superior.grid_rowconfigure(i, weight=1)

        # Define el tamaño mínimo del Frame
        self.contenedor_superior.config(width=50)

        # Título con fuente más grande
        titulo_label = tk.Label(self.contenedor_superior, text="Azimut General", bg="lightgrey", font=("Arial", 10, "bold"))
        titulo_label.grid(row=0, column=0, columnspan=len(self.column_labels), padx=3, pady=0, sticky='ew')

        # Etiquetas con fuente más grande
        for idx, label in enumerate(self.column_labels):
            label_widget = tk.Label(self.contenedor_superior, text=label, bg="lightgrey", font=("Arial", 8))
            label_widget.grid(row=1, column=idx, padx=1, pady=1, sticky='ew')

        self.top_entries = [None] * (2 * len(self.column_labels))
        for idx, label in enumerate(self.column_labels):
            if label in ["Punto", "Norte", "Este"]:
                entry = tk.Entry(self.contenedor_superior, font=("Arial", 8), width=8)
                entry.grid(row=2, column=idx, padx=1, pady=1, sticky='ew')
                self.top_entries[idx] = entry

                entry = tk.Entry(self.contenedor_superior, font=("Arial", 8), width=8)
                entry.grid(row=3, column=idx, padx=1, pady=1, sticky='ew')
                self.top_entries[len(self.column_labels) + idx] = entry

        # Etiquetas de diferencias con fuente más grande
        self.diferencia_label = tk.Label(self.contenedor_superior, text="DIFERENCIA", bg="lightgrey", font=("Arial", 10, "bold"))
        self.diferencia_label.grid(row=5,  column=0, padx=1, pady=1, sticky='w')

        self.diferencia_norte_label = tk.Label(self.contenedor_superior, text="Norte", bg="lightgrey", font=("Arial", 8))
        self.diferencia_norte_label.grid(row=4, column=1, padx=1, pady=1, sticky='ew')

        self.diferencia_este_label = tk.Label(self.contenedor_superior, text="Este", bg="lightgrey", font=("Arial", 8))
        self.diferencia_este_label.grid(row=4, column=2, padx=1, pady=1, sticky='ew')

        self.diferencia_norte_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 8))
        self.diferencia_norte_value_label.grid(row=5, column=1, padx=1, pady=1, sticky='ew')

        self.diferencia_este_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 8))
        self.diferencia_este_value_label.grid(row=5, column=2, padx=1, pady=1, sticky='ew')

        self.angulo_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 8))
        self.angulo_value_label.grid(row=2, column=3, padx=1, pady=1, sticky='ew')

        self.cuadrante_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 8))
        self.cuadrante_label.grid(row=2, column=4, padx=1, pady=1, sticky='ew')

        self.azimut_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 8))
        self.azimut_label.grid(row=2, column=5, padx=1, pady=1, sticky="ew")

        # Botón con fuente más grande
        calcular_button = tk.Button(self.contenedor_superior, text="Calcular Azimut", command=self.calcular_diferencias, font=("Arial", 8))
        calcular_button.grid(row=7, column=0, columnspan=len(self.column_labels), pady=1, sticky='ew')

    def _create_left_frame(self):
        tk.Label(self.left_frame, text="Cartera de campo", bg="lightgrey", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(2, 5), sticky='ew')

        self.left_frame.grid_columnconfigure(0, weight=0)
        for col in range(1, 6):
            self.left_frame.grid_columnconfigure(col, weight=0)

        labels = ["Delta", "Punto", "Angulo OBS", "Distancia", "Observación"]
        self.left_entries = []

        # Etiquetas para la primera fila de "Delta", "Punto", "Angulo OBS", "Distancia", "Observación"
        for idx, label in enumerate(labels):
            tk.Label(self.left_frame, text=label, bg="lightgrey", font=("Arial", 8)).grid(row=1, column=idx, padx=3, pady=3, sticky='ew')
            
            # Solo crea las entradas de texto para "Delta", "Punto", y "Angulo OBS" en la primera fila
            if idx < 3:
                entry = tk.Entry(self.left_frame, font=("Arial", 8), width= 10)
                entry.grid(row=2, column=idx, padx=1, pady=1, sticky='ew')
                self.left_entries.append(entry)

        # Segunda fila de entradas de "Punto", "Angulo OBS", "Distancia", "Observación" sin etiquetas adicionales
        for idx in range(1, len(labels)):
            entry = tk.Entry(self.left_frame, font=("Arial", 8), width=10)
            entry.grid(row=3, column=idx, padx=1, pady=1, sticky='ew')
            self.left_entries.append(entry)

        button_frame = tk.Frame(self.left_frame, bg="lightgrey")
        button_frame.grid(row=4, column=0, columnspan=len(labels), pady=5, sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)

        add_second_row_button = tk.Button(button_frame, text="Agregar Solo Segunda Fila", command=self.agregar_solo_segunda_fila, font=("Arial", 8))
        add_second_row_button.pack(side="left", padx=3, pady=3, expand=True)

        add_button = tk.Button(button_frame, text="Agregar Fila", command=self.agregar_fila, font=("Arial", 8))
        add_button.pack(side="left", padx=3, pady=3, expand=True)

        remove_button = tk.Button(button_frame, text="Eliminar Fila", command=self.eliminar_fila, font=("Arial", 8))
        remove_button.pack(side="left", padx=3, pady=3, expand=True)

    def _create_right_frame(self):
        labels = ["Delta", "Punto", "Ángulo OBS", "Distancia", "Observación"]

        self.tree = ttk.Treeview(self.right_frame, columns=labels, show='headings')
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("#1", text="Delta")
        self.tree.heading("#2", text="Punto")
        self.tree.heading("#3", text="Ángulo OBS")
        self.tree.heading("#4", text="Distancia")
        self.tree.heading("#5", text="Observación")

        self.tree.column("#1", width=100, anchor="center")
        self.tree.column("#2", width=100, anchor="center")
        self.tree.column("#3", width=200, anchor="center")
        self.tree.column("#4", width=100, anchor="center")
        self.tree.column("#5", width=100, anchor="center")

    def calcular_diferencias(self):
        try:
            punto1 = float(self.top_entries[0].get())
            punto2 = float(self.top_entries[1].get())
            angulo1 = float(self.top_entries[2].get())
            angulo2 = float(self.top_entries[3].get())
            distancia = float(self.top_entries[4].get())

            diferencia_norte = punto2 - punto1
            diferencia_este = distancia * (angulo2 - angulo1) / 360
            azimut = calcular_azimut(angulo1, angulo2)

            self.diferencia_norte_value_label.config(text="{:.2f}".format(diferencia_norte))
            self.diferencia_este_value_label.config(text="{:.2f}".format(diferencia_este))
            self.angulo_value_label.config(text="{:.2f}".format(angulo1))
            self.cuadrante_label.config(text=determinar_cuadrante(azimut))
            self.azimut_label.config(text="{:.2f}".format(azimut))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos")

    def agregar_fila(self):
        try:
            delta = self.left_entries[0].get()
            punto = self.left_entries[1].get()
            angulo_obs = self.convertir_gms(self.left_entries[2].get())
            distancia = self.left_entries[3].get()
            observacion = self.left_entries[4].get()

            self.tree.insert("", "end", values=(delta, punto, angulo_obs, distancia, observacion))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos")

    def agregar_solo_segunda_fila(self):
        try:
            punto = self.left_entries[1].get()
            angulo_obs = self.convertir_gms(self.left_entries[2].get())
            distancia = self.left_entries[3].get()
            observacion = self.left_entries[4].get()

            self.tree.insert("", "end", values=("", punto, angulo_obs, distancia, observacion))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos")

    def eliminar_fila(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            messagebox.showerror("Error", "No se ha seleccionado ninguna fila para eliminar")

    def convertir_gms(self, angulo):
        try:
            partes = angulo.split(".")
            if len(partes) != 3:
                raise ValueError("Formato de ángulo incorrecto. Debe ser en formato 'grados.minutos.segundos'.")

            grados = int(partes[0])
            minutos = int(partes[1])
            segundos = int(partes[2])

            if not (0 <= minutos < 60 and 0 <= segundos < 60):
                raise ValueError("Los minutos y segundos deben estar en el rango de 0 a 59.")

            return f"{grados}° {minutos}′ {segundos}″"
        except (ValueError, IndexError):
            raise ValueError("Error al convertir el ángulo. Asegúrese de ingresar el ángulo en formato correcto.")

