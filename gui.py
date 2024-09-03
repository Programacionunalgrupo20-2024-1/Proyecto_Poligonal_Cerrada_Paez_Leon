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
        self.contenedor_superior.grid(row=0, column=0, sticky='ew', padx=5, pady=(5, 0))  # Ajuste de padding

        self.column_labels = ["Punto", "Norte", "Este", "Ángulo", "Cuadrante", "Azimut"]
        self._create_superior_container()

        self.left_frame = tk.Frame(self.main_frame, bg="lightgrey", bd=2, relief="solid")
        self.left_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=(0, 5))  # Ajuste de padding

        self.right_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="solid")
        self.right_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=(0, 5))  # Ajuste de padding



        self._create_left_frame()
        self._create_right_frame()

    def _create_superior_container(self):
        # Configura las columnas con peso para ajustar el tamaño
        for i in range(len(self.column_labels)):
            self.contenedor_superior.grid_columnconfigure(i, weight=1)  # Asegura que las columnas se expandan igualmente

        # Configura las filas con peso bajo para ajustar el tamaño
        for i in range(8):  # Ajusta el número de filas que tengas
            self.contenedor_superior.grid_rowconfigure(i, weight=1)

        # Define el tamaño mínimo del Frame (ajusta el valor según sea necesario)
        self.contenedor_superior.config(width=50)  # Ajusta este valor según el tamaño deseado

        # Título con fuente más grande
        titulo_label = tk.Label(self.contenedor_superior, text="Azimut General", bg="lightgrey", font=("Arial", 10, "bold"))
        titulo_label.grid(row=0, column=0, columnspan=len(self.column_labels), padx=3, pady=0, sticky='ew')

        # Etiquetas con fuente más grande
        for idx, label in enumerate(self.column_labels):
            label_widget = tk.Label(self.contenedor_superior, text=label, bg="lightgrey", font=("Arial", 8))
            label_widget.grid(row=1, column=idx, padx=1, pady=1, sticky='ew')

        self.top_entries = [None] * (2 * len(self.column_labels))  # Inicializa con None, suficiente para ambas filas
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
        labels = ["Delta", "Punto", "Angulo OBS", "Distancia", "Observación"]
        column_widths = {
            "Delta": 50,
            "Punto": 50,
            "Angulo OBS": 80,
            "Distancia": 70,
            "Observación": 75
        }
        
        self.tree = ttk.Treeview(self.right_frame, columns=labels, show='headings')
        self.tree.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        self.right_frame.config(width=300, height=150)

        for label in labels:
            self.tree.heading(label, text=label)
            # Asigna el ancho específico para cada columna
            self.tree.column(label, width=column_widths.get(label, 70), anchor=tk.CENTER)

        # Configurar las filas y columnas del right_frame para que el Treeview y el nuevo frame se ajusten
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=0)  # Nueva fila para el frame rectangular

        # Crear el nuevo frame rectangular debajo del Treeview
        self.rectangular_frame = tk.Frame(self.right_frame, bg="lightgrey", bd=2, relief="solid")
        self.rectangular_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.rectangular_frame.config(width=200, height=150) 

        # Configurar las columnas y filas del nuevo frame rectangular
        self.rectangular_frame.grid_columnconfigure(0, weight=1)
        self.rectangular_frame.grid_rowconfigure(0, weight=1)

        # Titulo del frame
        titulo_juste_angular_label = tk.Label(self.rectangular_frame, text="Ajuste angular", bg="lightgrey", font=("Arial", 8, "bold"))
        titulo_juste_angular_label.grid(row=0, column=0, padx=1, pady=1, sticky='w')

        # Etiquetas una debajo de otra
        sumataria_observada_label = tk.Label(self.rectangular_frame, text="Sumatoria Obs", bg="lightgrey")
        sumataria_observada_label.grid(row=1, column=0, padx=1, pady=1, sticky='w')

        sumataria_teorica_label = tk.Label(self.rectangular_frame, text="Sumatoria Teorica", bg="lightgrey")
        sumataria_teorica_label.grid(row=2, column=0, padx=1, pady=1, sticky='w')

        error_pertimido_label = tk.Label(self.rectangular_frame, text="Error Permitido", bg="lightgrey")
        error_pertimido_label.grid(row=3, column=0, padx=1, pady=1, sticky='w')

        error_angular_label = tk.Label(self.rectangular_frame, text="Error Angular", bg="lightgrey")
        error_angular_label.grid(row=4, column=0, padx=1, pady=1, sticky='w')

        ajuste_angular_label = tk.Label(self.rectangular_frame, text="Ajuste Angular", bg="lightgrey")
        ajuste_angular_label.grid(row=5, column=0, padx=1, pady=1, sticky='w')

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
        # Obtener datos de la primera fila de entradas en el left_frame
        datos_fila_1 = [entry.get() for entry in self.left_entries[:3]]  # Ajusta el rango para tomar solo las primeras tres columnas
        datos_fila_1.extend(["", ""])  # Completa con columnas vacías para las últimas dos columnas (Distancia y Observación)

        # Obtener datos de la segunda fila de entradas en el left_frame
        datos_fila_2 = [""] * len(self.tree["columns"])  # Crear una lista con el número de columnas del Treeview
        datos_fila_2[1] = self.left_entries[3].get()  # "Punto" de la fila 1
        datos_fila_2[2] = self.left_entries[4].get()  # "Ángulo OBS" de la fila 1
        datos_fila_2[3] = self.left_entries[5].get()  # "Distancia" de la fila 2
        datos_fila_2[4] = self.left_entries[6].get()  # "Observación" de la fila 2

        # Agregar primera fila de datos al Treeview
        if any(datos_fila_1[:3]):  # Verifica que al menos una de las primeras tres entradas tenga valor
            self.tree.insert("", "end", values=datos_fila_1)

        # Agregar segunda fila de datos al Treeview
        if any(datos_fila_2[1:]):  # Verifica que al menos uno de los campos relevantes tenga valor
            self.tree.insert("", "end", values=datos_fila_2)

        # Limpiar las entradas después de agregar las filas
        for entry in self.left_entries:
            entry.delete(0, tk.END)


    def agregar_solo_segunda_fila(self):
        # Obtener datos de la segunda fila de entradas en el left_frame
        datos_fila_2 = [""] * len(self.left_entries)  # Inicializa con valores vacíos
        datos_fila_2[1] = self.left_entries[3].get()  # Punto
        datos_fila_2[2] = self.left_entries[4].get()  # Ángulo OBS
        datos_fila_2[3] = self.left_entries[5].get()  # Distancia
        datos_fila_2[4] = self.left_entries[6].get()  # Observación

        # Agregar segunda fila de datos al Treeview
        if any(datos_fila_2[1:]):  # Verifica que al menos uno de los campos relevantes tenga valor
            self.tree.insert("", "end", values=datos_fila_2)

        # Limpiar las entradas después de agregar la fila
        for entry in self.left_entries:
            entry.delete(0, tk.END)



    def eliminar_fila(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna fila para eliminar.")
