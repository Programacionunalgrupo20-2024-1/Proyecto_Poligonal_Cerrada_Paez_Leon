import tkinter as tk
from tkinter import ttk, messagebox
from math import fabs, atan, degrees, sqrt
from calculos import decimal_a_dms, determinar_cuadrante, calcular_azimut, convertir_gms_a_decimal, convertir_a_gms, ConversionError


class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.insert(0, self.placeholder)
        self.config(fg='grey')  # Inicialmente, el texto de marcador de posición es gris
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)

    def remove_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg='black')  # Cambia el color del texto a negro cuando se enfoca

    def add_placeholder(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg='grey')  # Cambia el color del texto a gris cuando no se enfoca

class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz con Frame a la Izquierda")
        self.root.state('zoomed')

        # Creación del Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Frames alojados en Notebook
        self.main_frame = ttk.Frame(self.notebook)
        self.poligonal_frame = ttk.Frame(self.notebook)
        
        # Se añaden frames como pestañas al notebook
        self.notebook.add(self.main_frame, text='Calculos')
        self.notebook.add(self.poligonal_frame, text='Tabla de cáculos')

        # Contenido del Main Frame
        self.contenedor_superior = tk.Frame(self.main_frame, bg="lightgrey", bd=2, relief="solid")
        self.contenedor_superior.grid(row=0, column=0, sticky='ew', padx=5, pady=(5, 0))  # Ajuste de padding

        self.column_labels = ["Punto", "Norte", "Este", "Ángulo", "Cuadrante", "Azimut"]
        self._create_superior_container()

        self.valores_col3 = []
        self.valores_col3_decimales = []

        self.left_frame = tk.Frame(self.main_frame, bg="lightgrey", bd=2, relief="solid")
        self.left_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=(0, 5))  # Ajuste de padding

        self.right_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="solid")
        self.right_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=(0, 5))  # Ajuste de padding

        # Contenido de Poligonal Frame
        self.top_frame = tk.Frame(self.poligonal_frame, bg="lightgrey", bd=2, relief="solid")
        self.top_frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)

        self._create_left_frame()
        self._create_right_frame()
        self.crear_top_frame()

        self.configurar_teclado()

    def _create_superior_container(self):

        # Coordenadas guardadas
        self.norte_uno = []
        self.norte_dos = []
        self.este_uno = []
        self.este_dos = []

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

        # Entrada de puntos texto
        entrada_1 = tk.Entry(self.contenedor_superior, font=("Arial", 8), width= 8)
        entrada_1.grid(row=2, column=0, padx=1, pady=1, sticky='ew')

        entrada_2 = tk.Entry(self.contenedor_superior, font=("Arial", 8), width= 8)
        entrada_2.grid(row=3, column=0, padx=1, pady=1, sticky='ew')

        # Entrada de coordenadas norte
        norte_1 = tk.Entry(self.contenedor_superior, font=("Arial", 8), width= 8)
        norte_1.grid(row=2, column=1, padx=1, pady=1, sticky='ew')
        self.norte_uno.append(norte_1)

        norte_2 = tk.Entry(self.contenedor_superior, font=("Arial", 8), width= 8)
        norte_2.grid(row=3, column=1, padx=1, pady=1, sticky='ew')
        self.norte_dos.append(norte_2)

        # Entrada de coordenadas este
        este_1 = tk.Entry(self.contenedor_superior, font=("Arial", 8), width= 10)
        este_1.grid(row=2, column=2, padx=1, pady=1, sticky='ew')
        self.este_uno.append(este_1)

        este_2 = tk.Entry(self.contenedor_superior, font=("Arial", 8), width= 10)
        este_2.grid(row=3, column=2, padx=1, pady=1, sticky='ew')
        self.este_dos.append(este_2)


        # Etiquetas de diferencias con fuente más grande
        self.diferencia_label = tk.Label(self.contenedor_superior, text="DIFERENCIA", bg="lightgrey", font=("Arial", 8, "bold"))
        self.diferencia_label.grid(row=5,  column=0, padx=1, pady=1, sticky='w')

        self.diferencia_norte_label = tk.Label(self.contenedor_superior, text="Norte", bg="lightgrey", font=("Arial", 7))
        self.diferencia_norte_label.grid(row=4, column=1, padx=1, pady=1, sticky='ew')

        self.diferencia_este_label = tk.Label(self.contenedor_superior, text="Este", bg="lightgrey", font=("Arial", 7))
        self.diferencia_este_label.grid(row=4, column=2, padx=1, pady=1, sticky='ew')

        self.diferencia_norte_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 7))
        self.diferencia_norte_value_label.grid(row=5, column=1, padx=1, pady=1, sticky='ew')

        self.diferencia_este_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 7))
        self.diferencia_este_value_label.grid(row=5, column=2, padx=1, pady=1, sticky='ew')

        self.angulo_value_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 7))
        self.angulo_value_label.grid(row=2, column=3, padx=1, pady=1, sticky='ew')

        self.cuadrante_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 7))
        self.cuadrante_label.grid(row=2, column=4, padx=1, pady=1, sticky='ew')

        self.azimut_label = tk.Label(self.contenedor_superior, text="", bg="lightgrey", font=("Arial", 7))
        self.azimut_label.grid(row=2, column=5, padx=1, pady=1, sticky="ew")

        # Botón con fuente más grande
        calcular_button = tk.Button(self.contenedor_superior, text="Calcular Azimut", command=self.calcular_diferencias, font=("Arial", 8))
        calcular_button.grid(row=7, column=0, columnspan=len(self.column_labels), pady=1, sticky='ew')
        
    def calcular_diferencias(self):
            
            norte_1 = float(self.norte_uno[0].get())
            norte_2 = float(self.norte_dos[0].get())
            este_1 = float(self.este_uno[0].get())
            este_2 = float(self.este_dos[0].get())

            # Calcula las diferencias y otros valores
            diferencia_norte = norte_2 - norte_1
            diferencia_este = este_2 - este_1

            self.diferencia_norte_value_label.config(text=f"{diferencia_norte}")
            self.diferencia_este_value_label.config(text=f"{diferencia_este}")

            cuadrante = determinar_cuadrante(diferencia_este, diferencia_norte)
            self.cuadrante_label.config(text=f"{cuadrante}")

            calculo = atan(fabs(diferencia_este)/fabs(diferencia_norte))
            angulo = degrees(calculo)
            angulo_convertido = decimal_a_dms(angulo)
            self.angulo_value_label.config(text=f"{angulo_convertido}")

            calculo_azimut = calcular_azimut(cuadrante,angulo)
            azimut_convertido = decimal_a_dms(calculo_azimut)
            self.azimut_label.config(text=f"{azimut_convertido}")

    def _create_left_frame(self):
        tk.Label(self.left_frame, text="Cartera de campo", bg="lightgrey", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(2, 5), sticky='ew')

        self.left_frame.grid_columnconfigure(5, weight=0)
        for col in range(1, 6):
            self.left_frame.grid_columnconfigure(col, weight=0)

        labels = ["Delta", "Punto", "Angulo OBS", "Distancia", "Observación"]
        self.left_entries = []

        # Etiquetas para la primera fila de "Delta", "Punto", "Angulo OBS", "Distancia", "Observación"
        for idx, label in enumerate(labels):
            hola=tk.Label(self.left_frame, text=label, bg="lightgrey", font=("Arial", 8)).grid(row=1, column=idx, padx=3, pady=3, sticky='ew')
            

            # Solo crea las entradas de texto para "Delta", "Punto", y "Angulo OBS" en la primera fila
            if idx < 3:
                entry = tk.Entry(self.left_frame, font=("Arial", 8), width= 11)
                entry.grid(row=2, column=idx, padx=1, pady=1, sticky='ew')
                self.left_entries.append(entry)

        # Segunda fila de entradas de "Punto", "Angulo OBS", "Distancia", "Observación" sin etiquetas adicionales
        for idx in range(1, len(labels)):
            entry = tk.Entry(self.left_frame, font=("Arial", 8), width=11)
            entry.grid(row=3, column=idx, padx=1,pady=1, sticky='ew')
            self.left_entries.append(entry)

        button_frame = tk.Frame(self.left_frame, bg="lightgrey")
        button_frame.grid(row=4, column=0, columnspan=len(labels), pady=5, sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)

        self.add_button = tk.Button(button_frame, text="Agregar Delta", command=self.agregar_fila, font=("Arial", 8))
        self.add_button.pack(side="left", padx=3, pady=3, expand=True)

        self.add_second_row_button = tk.Button(button_frame, text="Agregar Detalle", command=self.agregar_solo_segunda_fila, font=("Arial", 8))
        self.add_second_row_button.pack(side="left", padx=3, pady=3, expand=True)

        remove_button = tk.Button(button_frame, text="Eliminar Fila", command=self.eliminar_fila, font=("Arial", 8))
        remove_button.pack(side="left", padx=3, pady=3, expand=True)

    def agregar_fila(self):
        
        # Obtener datos de la primera fila de entradas en el left_frame
        datos_fila_1 = [entry.get() for entry in self.left_entries[:3]]  # Ajusta el rango para tomar solo las primeras tres columnas
        
        # Convertir el Ángulo OBS de la primera fila
        angulo_obs_1 = self.left_entries[2].get()  # Índice correcto para el Ángulo OBS
        
        try:
            datos_fila_1[2] = convertir_a_gms(angulo_obs_1) # Aplicar la conversión
        except ConversionError as e:
            messagebox.showerror("Error al convertir Ángulo OBS 1")
            return

        # Completa con columnas vacías para las últimas dos columnas (Distancia y Observación)
        datos_fila_1.extend(["", ""])
        
        # Obtener datos de la segunda fila de entradas en el left_frame
        datos_fila_2 = [""] * len(self.tree["columns"])  # Crear una lista con el número de columnas del Treeview
        datos_fila_2[1] = self.left_entries[3].get()  # "Punto" de la fila 2

        # Convertir el Ángulo OBS de la segunda fila
        angulo_obs_2 = self.left_entries[4].get()
        try:
            datos_fila_2[2] = convertir_a_gms(angulo_obs_2) # Aplicar la conversión
        except ConversionError as e:
            messagebox.showerror("Error al convertir Ángulo OBS 2")
            

        datos_fila_2[3] = self.left_entries[5].get()  # "Distancia" de la fila 2
        datos_fila_2[4] = self.left_entries[6].get()  # "Observación" de la fila 2
        
        # Agregar primera fila de datos al Treeview
        if any(datos_fila_1[:3]):  # Verifica que al menos una de las primeras tres entradas tenga valor
            self.tree.insert("", "end", values=datos_fila_1, tags=("delta",))

        # Agregar primera fila de datos al Treeview de segunda pestaña
        if any(datos_fila_1[:3]):  # Verifica que al menos una de las primeras tres entradas tenga valor
            self.tree_tabla.insert("", "end", values=datos_fila_1, tags=("delta",))


        # Obtener datos de la segunda fila de entradas en el left_frame para el segundo treeview
        datos_fila_2_reordenada = [""] * len(self.tree_tabla["columns"])  # Crear una lista con el número de columnas del Treeview segunda pestaña
        datos_fila_2_reordenada[1] = self.left_entries[3].get()  # "Punto" de la fila 2

        # Convertir el Ángulo OBS de la segunda fila
        angulo_obs_2_tree = self.left_entries[4].get()
        try:
            datos_fila_2_reordenada[2] = convertir_a_gms(angulo_obs_2_tree) # Aplicar la conversión
        except ConversionError as e:
            messagebox.showerror("Error al convertir Ángulo OBS 2")

        datos_fila_2_reordenada[6] = self.left_entries[5].get()  # "Distancia" de la fila 2
        datos_fila_2_reordenada[15] = self.left_entries[6].get()  # "Observación" de la fila 2
        

        # Agregar segunda fila de datos al Treeview de segunda pestaña
        if any(datos_fila_2[1:]):  # Verifica que al menos uno de los campos relevantes tenga valor
            id_fila_2 = self.tree_tabla.insert("", "end", values=datos_fila_2_reordenada, tags=("delta",))

        # Agregar segunda fila de datos al Treeview
        if any(datos_fila_2[1:]):  # Verifica que al menos uno de los campos relevantes tenga valor
            id_fila_2 = self.tree.insert("", "end", values=datos_fila_2, tags=("delta",))
        
            # Guardar valores segunda fila tercera columna
            valores_segunda_fila = self.tree.item(id_fila_2, 'values')  # Obtener valores de la fila
            valor_col3 = valores_segunda_fila[2]  # Tercera columna (índice 2)
            decimales = convertir_gms_a_decimal(valor_col3)
            self.valores_col3_decimales.append(decimales)  # Guardar en la lista


        # Limpiar las entradas después de agregar las filas 
        for entrada in self.left_entries:
            entrada.delete(0, tk.END)

    def agregar_solo_segunda_fila(self):
        # Obtener datos de la segunda fila de entradas en el left_frame
        datos_fila_2 = [""] * len(self.tree["columns"])  # Inicializa con valores vacíos
        datos_fila_2[1] = self.left_entries[3].get()  # "Punto"
        
        # Convertir el Ángulo OBS de la segunda fila
        angulo_obs_2 = self.left_entries[4].get()
        print(f"Ángulo OBS 2 (antes de conversión): {angulo_obs_2}")  # Mensaje de depuración
        datos_fila_2[2] = convertir_a_gms(angulo_obs_2)  # Convertir el Ángulo OBS de la segunda fila
        print(f"Ángulo OBS 2 (después de conversión): {datos_fila_2[2]}")  # Mensaje de depuración

        datos_fila_2[3] = self.left_entries[5].get()  # "Distancia"
        datos_fila_2[4] = self.left_entries[6].get()  # "Observación"

        # Agregar segunda fila de datos al Treeview
        if any(datos_fila_2[1:]):  # Verifica que al menos uno de los campos relevantes tenga valor
            self.tree.insert("", "end", values=datos_fila_2, tags=("detalle",))

        # Obtener datos de la segunda fila de entradas en el left_frame para el segundo treeview
        datos_fila_2_reordenada = [""] * len(self.tree_tabla["columns"])  # Crear una lista con el número de columnas del Treeview segunda pestaña
        datos_fila_2_reordenada[1] = self.left_entries[3].get()  # "Punto" de la fila 2

        # Convertir el Ángulo OBS de la segunda fila
        angulo_obs_2_tree = self.left_entries[4].get()
        try:
            datos_fila_2_reordenada[2] = convertir_a_gms(angulo_obs_2_tree) # Aplicar la conversión
        except ConversionError as e:
            messagebox.showerror("Error al convertir Ángulo OBS 2")

        datos_fila_2_reordenada[6] = self.left_entries[5].get()  # "Distancia" de la fila 2
        datos_fila_2_reordenada[15] = self.left_entries[6].get()  # "Observación" de la fila 2
        

        # Agregar segunda fila de datos al Treeview de segunda pestaña
        if any(datos_fila_2[1:]):  # Verifica que al menos uno de los campos relevantes tenga valor
            id_fila_2 = self.tree_tabla.insert("", "end", values=datos_fila_2_reordenada, tags=("detalle",))
        

        # Limpiar las entradas después de agregar la fila
        for entry in self.left_entries:
            entry.delete(0, tk.END)

    def crear_top_frame(self):

        Tabla_labels_2 = ["Delta", "Punto", "Angulo\nOBS", "Ajuste\nAngular", "Angulo\nCorregido", "Azimut", "Distancia", "N-S", "E-W", "Ajuste\nN-S", "Ajuste\nE-W ", "N-S\nCorregido", "E-W\nCorregido", "Coordenadas\nN-S", "Coordenadas\nE-W", "Observaciones"]
        
        column_widths_2 = {
            "Delta" : 60,
            "Punto" : 60,
            "Angulo\nOBS" : 70,
            "Ajuste\nAngular": 70,
            "Angulo\nCorregido": 70,
            "Azimut" : 70,
            "Distancia" : 50,
            "N-S" : 60,
            "E-W" : 60,
            "Ajuste\nN-S" : 60,
            "Ajuste\nE-W " : 60,
            "N-S\nCorregido" : 60,
            "E-W\nCorregido" : 60,
            "Coordenadas\nN-S" : 60,
            "Coordenadas\nE-W" : 60,
            "Observaciones" : 80
        }

        self.tree_tabla = ttk.Treeview(self.top_frame, columns=Tabla_labels_2, show='headings', height=10)
        self.tree_tabla.grid(row=0, column=1, padx=0, pady=0, sticky='nsew')
        self.top_frame.config(width=500, height=100)

        # Crear un estilo y configurar la fuente
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 7, 'bold'))
        style.map('Treeview.Heading', background=[('selected', 'lightblue')])
        style.configure('Treeview', font=('Arial',7))

        # Configuración de estilo para colores de filas
        self.style = ttk.Style()
        self.style.configure("delta.Treeview", background="lightgreen")
        self.style.configure("detalle.Treeview", background="lightcoral")
        
        self.tree_tabla.tag_configure("delta", background="lightgreen")
        self.tree_tabla.tag_configure("detalle", background="lightcoral")

        for label in column_widths_2:
            self.tree_tabla.heading(label, text=label, anchor='center')
            # Asigna el ancho específico para cada columna
            self.tree_tabla.column(label, width=column_widths_2.get(label, 70), anchor=tk.CENTER)

        # Configurar las filas y columnas del right_frame para que el Treeview y el nuevo frame se ajusten
        self.tree_tabla.grid_columnconfigure(0, weight=1)
        self.tree_tabla.grid_rowconfigure(0, weight=1)




    def _create_right_frame(self):
        self.lados_poligono = []
        self.valor_de_a = []
        labels = ["Delta", "Punto", "Angulo OBS", "Distancia", "Observación"]
        column_widths = {
            "Delta": 50,
            "Punto": 50,
            "Angulo OBS": 80,
            "Distancia": 70,
            "Observación": 75
        }
        
        self.tree = ttk.Treeview(self.right_frame, columns=labels, show='headings', height=5)
        self.tree.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')
        self.right_frame.config(width=300, height=100)

        # Configuración de estilo para colores de filas
        self.style = ttk.Style()
        self.style.configure("delta.Treeview", background="lightgreen")
        self.style.configure("detalle.Treeview", background="lightcoral")
        
        self.tree.tag_configure("delta", background="lightgreen")
        self.tree.tag_configure("detalle", background="lightcoral")


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
        self.rectangular_frame.grid_columnconfigure(0, weight=0)
        self.rectangular_frame.grid_rowconfigure(0, weight=0)


        # Etiquetas una debajo de otra
        sumataria_observada_label = tk.Label(self.rectangular_frame, text="Sumatoria Obs", bg="lightgrey", font=("Arial", 7))
        sumataria_observada_label.grid(row=1, column=0, padx=1, pady=1, sticky='w')

        sumataria_teorica_label = tk.Label(self.rectangular_frame, text="Sumatoria Teorica", bg="lightgrey", font=("Arial", 7))
        sumataria_teorica_label.grid(row=2, column=0, padx=1, pady=1, sticky='w')

        error_pertimido_label = tk.Label(self.rectangular_frame, text="Error Permitido", bg="lightgrey", font=("Arial", 7))
        error_pertimido_label.grid(row=3, column=0, padx=1, pady=1, sticky='w')

        error_angular_label = tk.Label(self.rectangular_frame, text="Error Angular", bg="lightgrey", font=("Arial", 7))
        error_angular_label.grid(row=4, column=0, padx=1, pady=1, sticky='w')

        ajuste_angular_label = tk.Label(self.rectangular_frame, text="Ajuste Angular", bg="lightgrey", font=("Arial", 7))
        ajuste_angular_label.grid(row=5, column=0, padx=1, pady=1, sticky='w')

        Ajuste_angular_button = tk.Button(self.rectangular_frame, text="Ajuste Angular", command=self.calcular_ajuste_angular, font=("Arial", 8, "bold"))
        Ajuste_angular_button.grid(row=0, column=0, padx=1, pady=1, sticky='ew')

        # Entrada de texto lados de poligono y valor de a con placeholder
        lados_entry = PlaceholderEntry(self.rectangular_frame, placeholder="# lados", font=("Arial", 7), width=11)
        lados_entry.grid(row=0, column=1, padx=3, pady=1, sticky='w')
        self.lados_poligono.append(lados_entry)

        valor_a = PlaceholderEntry(self.rectangular_frame, placeholder="valor a", font=("Arial", 7), width=11)
        valor_a.grid(row=0, column=2, padx=1, pady=1, sticky='w')
        self.valor_de_a.append(valor_a)

        # Etiquetas calculos -> Sumatoria observada, Sumatoria teorica, Error permitdo, error angular y ajuste angular
        self.calculo_sumatoria_observada_label = tk.Label(self.rectangular_frame, text="", bg="lightgrey", font=("Arial", 7))
        self.calculo_sumatoria_observada_label.grid(row=1, column=1, padx=1, pady=1, sticky='w')

        self.calculo_sumatoria_teorica_label = tk.Label(self.rectangular_frame, text="", bg="lightgrey", font=("Arial", 7))
        self.calculo_sumatoria_teorica_label.grid(row=2, column= 1, padx=1, pady=1, sticky='w')

        self.calculo_error_permitido_label = tk.Label(self.rectangular_frame, text="", bg="lightgrey", font=("Arial", 7))
        self.calculo_error_permitido_label.grid(row=3, column=1, padx=1, pady=1, sticky='w')

        self.calculo_error_angular_label = tk.Label(self.rectangular_frame,  text="", bg="lightgrey", font=("Arial", 7))
        self.calculo_error_angular_label.grid(row=4, column=1, padx=1, pady=1, sticky='w')

        self.calculo_ajuste_angular_label = tk.Label(self.rectangular_frame,  text="", bg="lightgrey", font=("Arial", 7))
        self.calculo_ajuste_angular_label.grid(row=5, column=1, padx=1, pady=1, sticky='w')

    def calcular_ajuste_angular(self):
        try:
            # Obtener valor de a
            a = self.valor_de_a[0].get()
            a_gms = convertir_a_gms(a) 
            a_decimal = convertir_gms_a_decimal(a_gms)        

            # Obtener número de lados del poligono
            lados = int(self.lados_poligono[0].get())

            # Sumatoria obs
            sumatoria_obs = sum(self.valores_col3_decimales)
            sumatoria_obs_convertida = decimal_a_dms(sumatoria_obs)
            self.calculo_sumatoria_observada_label.config(text=f"{sumatoria_obs_convertida}")

            # Sumatoria Teorica
            sumatoria_teorica = 180*(lados+2)
            sumatoria_teorica_convertida = decimal_a_dms(sumatoria_teorica)
            self.calculo_sumatoria_teorica_label.config(text=f"{sumatoria_teorica_convertida}")
            
            # Error permitido
            error_permitido = a_decimal*sqrt(lados)
            error_permitido_convertido = decimal_a_dms(error_permitido)
            self.calculo_error_permitido_label.config(text=f"{error_permitido_convertido}")

            # Error angular
            error_angular = sumatoria_teorica-sumatoria_obs
            error_angular_convertido = decimal_a_dms(error_angular)
            self.calculo_error_angular_label.config(text=f"{error_angular_convertido}")

            # Ajuste Angular
            ajuste_angular = error_angular/(lados+1)*1
            ajuste_angular_convertido = decimal_a_dms(ajuste_angular)
            self.calculo_ajuste_angular_label.config(text=f"{ajuste_angular_convertido}")

        
        except ValueError:
            messagebox.showerror("Formato invalido")  
    
    def configurar_teclado(self):
        
        # Bindear la tecla "Supr" para eliminar filas
        self.root.bind('<Delete>', self.eliminar_fila)

    def eliminar_fila(self, event=None):
        # Obtener todas las filas seleccionadas
        selected_items = self.tree.selection()
        
        if selected_items:
            # Recorrer y eliminar cada fila seleccionada
            for item in selected_items:
                self.tree.delete(item)
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna fila para eliminar.")

        if selected_items:
            # Recorrer y eliminar cada fila seleccionada
            for item in selected_items:
                self.tree_tabla.delete(item)
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna fila para eliminar.")

        

