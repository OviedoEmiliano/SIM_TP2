import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math

ventana_histograma_activa = None
ventana_tabla_frecuencias_activa = None

class InterfazGenerador(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        print(f"Controlador en InterfazGenerador.__init__: {controlador}")
        self.controlador = controlador
        self.title("Generador de Números Aleatorios con Histograma")

        self.numeros_generados = []
        self.pagina_actual = 0
        self.tamano_pagina = 200

        self.distribucion_var = tk.StringVar(value="Uniforme")
        self.intervalos_var = tk.StringVar(value="10")



    def iniciar(self):
        self._crear_widgets()
        self._configurar_grid()
        self._mostrar_parametros(2)

    def _crear_widgets(self):
        self.cantidad_label = tk.Label(self, text="Cantidad de números a generar:")
        self.cantidad_entry = tk.Entry(self)

        self.distribucion_frame = tk.LabelFrame(self, text="Tipo de Distribución")
        self.rb_exponencial = tk.Radiobutton(
            self.distribucion_frame,
            text="Exponencial (lambda):",
            variable=self.distribucion_var,
            value="Exponencial",
            command=lambda: self._mostrar_parametros(1),
        )
        self.rb_normal = tk.Radiobutton(
            self.distribucion_frame,
            text="Normal (mu, sigma):",
            variable=self.distribucion_var,
            value="Normal",
            command=lambda: self._mostrar_parametros(2),
        )
        self.rb_uniforme = tk.Radiobutton(
            self.distribucion_frame,
            text="Uniforme (a, b):",
            variable=self.distribucion_var,
            value="Uniforme",
            command=lambda: self._mostrar_parametros(2),
        )

        self.parametros_frame = tk.LabelFrame(self, text="Parámetros")
        self.parametro1_label = tk.Label(self.parametros_frame, text="Parámetro 1:")
        self.parametro1_entry = tk.Entry(self.parametros_frame)
        self.parametro2_label = tk.Label(self.parametros_frame, text="Parámetro 2:")
        self.parametro2_entry = tk.Entry(self.parametros_frame)

        self.intervalos_label = tk.Label(
            self, text="Número de intervalos del histograma:"
        )
        self.intervalos_combo = ttk.Combobox(
            self,
            textvariable=self.intervalos_var,
            values=["10", "15", "20", "25"],
            state="readonly",
        )

        self.generar_histograma_boton = tk.Button(
            self,
            text="Generar y Mostrar Histograma",
            command=self.controlador.generar_y_mostrar_histograma,
        )

        self.scrollbar = tk.Scrollbar(self)
        self.resultado_text = tk.Text(
            self, height=5, width=50, yscrollcommand=self.scrollbar.set
        )
        self.boton_anterior = tk.Button(
            self, text="Anterior", command=self._anterior_pagina
        )
        self.boton_siguiente = tk.Button(
            self, text="Siguiente", command=self._siguiente_pagina
        )
        self.scrollbar.config(command=self.resultado_text.yview)

    def _configurar_grid(self):
        self.cantidad_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cantidad_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.distribucion_frame.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.rb_exponencial.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.rb_normal.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.rb_uniforme.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.parametros_frame.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.parametro1_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.parametro1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.parametro2_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.parametro2_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        self.intervalos_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.intervalos_combo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.generar_histograma_boton.grid(
            row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew"
        )

        self.scrollbar.grid(row=5, column=2, padx=0, pady=5, sticky="ns")
        self.resultado_text.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )
        self.boton_anterior.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        self.boton_siguiente.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)

    def _mostrar_parametros(self, num_params):
        if num_params == 1:
            self.parametro1_label.config(text="Lambda:")
            self.parametro1_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.parametro1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
            self.parametro2_label.grid_forget()
            self.parametro2_entry.grid_forget()
        elif num_params == 2:
            self.parametro1_label.config(text="Parámetro 1:")
            self.parametro1_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.parametro1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
            self.parametro2_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
            self.parametro2_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    def mostrar_resultado(self, texto):
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, texto)
        self.resultado_text.see(tk.END)

    def mostrar_histograma(self, numeros, distribucion, num_intervalos):
        global ventana_histograma_activa

        if ventana_histograma_activa:
            ventana_histograma_activa.destroy()

        histograma_ventana = tk.Toplevel(self)
        histograma_ventana.title(
            f"Histograma ({distribucion}, {num_intervalos} intervalos)"
        )
        ventana_histograma_activa = histograma_ventana

        fig, ax = plt.subplots()
        n, bins, patches = ax.hist(numeros, bins=num_intervalos, edgecolor="black")

        # Creamos las etiquetas personalizadas
        labels = [f"{bins[0]:.4f}"] + [f"{b:.4f}" for b in bins[1:]]

        # Establecemos las ubicaciones de las etiquetas en los límites de los intervalos
        ax.set_xticks(bins)
        ax.set_xticklabels(labels, rotation=45, ha="right")

        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Distribución {distribucion} ({num_intervalos} intervalos)")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=histograma_ventana)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def obtener_cantidad(self):
        return self.cantidad_entry.get()

    def obtener_distribucion(self):
        return self.distribucion_var.get()

    def obtener_parametros(self):
        params = {}
        if self.distribucion_var.get() == "Exponencial":
            try:
                params["lambda"] = (
                    float(self.parametro1_entry.get())
                    if self.parametro1_entry.get()
                    else 1.0
                )
            except ValueError:
                return None, "Por favor, ingresa un número válido para lambda."
        elif self.distribucion_var.get() == "Normal":
            try:
                params["mu"] = (
                    float(self.parametro1_entry.get())
                    if self.parametro1_entry.get()
                    else 0.0
                )
                params["sigma"] = (
                    float(self.parametro2_entry.get())
                    if self.parametro2_entry.get()
                    else 1.0
                )
            except ValueError:
                return None, "Por favor, ingresa números válidos para mu y sigma."
        elif self.distribucion_var.get() == "Uniforme":
            try:
                params["a"] = (
                    float(self.parametro1_entry.get())
                    if self.parametro1_entry.get()
                    else 0.0
                )
                params["b"] = (
                    float(self.parametro2_entry.get())
                    if self.parametro2_entry.get()
                    else 1.0
                )
            except ValueError:
                return None, "Por favor, ingresa números válidos para a y b."
        return params, None

    def obtener_num_intervalos(self):
        return int(self.intervalos_var.get())
    




    # Funcion para mostrar la pagina de resultados
    def mostrar_pagina_resultados(self):
        if not self.numeros_generados:
            return

        inicio = self.pagina_actual * self.tamano_pagina
        fin = inicio + self.tamano_pagina
        pagina = self.numeros_generados[inicio:fin]

        columnas = 10
        texto = f"Números página {self.pagina_actual + 1}:\n\n"
        for i, num in enumerate(pagina):
            texto += f"{num:<10}"  # 10 caracteres de ancho, alineado a la izquierda
            if (i + 1) % columnas == 0:
                texto += "\n"

        self.mostrar_resultado(texto)



    # Funcion para calcular la Anterior Pagina
    def _anterior_pagina(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_pagina_resultados()


    
    # Funcion para calcular la Siguiente Pagina
    def _siguiente_pagina(self):
        total_paginas = math.ceil(len(self.numeros_generados) / self.tamano_pagina)
        if self.pagina_actual < total_paginas - 1:
            self.pagina_actual += 1
            self.mostrar_pagina_resultados()

    # Funcion para mostrar la Tabla de frecuencias en el cuadro de texto
    def crear_ventana_tabla_frecuencias(self, tabla):
        global ventana_tabla_frecuencias_activa  # Usa la variable global

        if ventana_tabla_frecuencias_activa:
            ventana_tabla_frecuencias_activa.destroy()  # Cierra la ventana anterior


        nueva_ventana = tk.Toplevel(self)
        nueva_ventana.title("Tabla de Frecuencias")

        # Crear un widget Text para mostrar la tabla
        resultado_text = tk.Text(nueva_ventana, wrap=tk.WORD)
        resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Añadir una barra de desplazamiento vertical si es necesario
        scrollbar = tk.Scrollbar(nueva_ventana, command=resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        resultado_text.config(yscrollcommand=scrollbar.set)

        # Insertar la tabla de frecuencias en el Text widget
        resultado_text.insert(tk.END, "\nTabla de Frecuencias:\n")
        resultado_text.insert(tk.END, f"{'Intervalo':<25} {'Frec. Abs.':<10} {'Frec. Rel.':<10} {'Frec. Acum.':<10}\n")
        resultado_text.insert(tk.END, "-" * 65 + "\n")  # Ajusta el ancho de la línea
        for intervalo, frecuencia_absoluta, frecuencia_relativa, acumulado in tabla:
            resultado_text.insert(tk.END, f"{intervalo:<25} {frecuencia_absoluta:<10} {frecuencia_relativa:<10.4f} {acumulado:<10}\n")  # Formatea la frecuencia relativa

        # Deshabilitar la edición del Text widget
        resultado_text.config(state=tk.DISABLED)