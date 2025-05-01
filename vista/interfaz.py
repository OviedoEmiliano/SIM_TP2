import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class InterfazGenerador(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        print(f"Controlador en InterfazGenerador.__init__: {controlador}")
        self.controlador = controlador
        self.title("Generador de Números Aleatorios con Histograma")

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
        self.rb_exponencial = tk.Radiobutton(self.distribucion_frame, text="Exponencial (lambda):", variable=self.distribucion_var, value="Exponencial", command=lambda: self._mostrar_parametros(1))
        self.rb_normal = tk.Radiobutton(self.distribucion_frame, text="Normal (mu, sigma):", variable=self.distribucion_var, value="Normal", command=lambda: self._mostrar_parametros(2))
        self.rb_uniforme = tk.Radiobutton(self.distribucion_frame, text="Uniforme (a, b):", variable=self.distribucion_var, value="Uniforme", command=lambda: self._mostrar_parametros(2))

        self.parametros_frame = tk.LabelFrame(self, text="Parámetros")
        self.parametro1_label = tk.Label(self.parametros_frame, text="Parámetro 1:")
        self.parametro1_entry = tk.Entry(self.parametros_frame)
        self.parametro2_label = tk.Label(self.parametros_frame, text="Parámetro 2:")
        self.parametro2_entry = tk.Entry(self.parametros_frame)

        self.intervalos_label = tk.Label(self, text="Número de intervalos del histograma:")
        self.intervalos_combo = ttk.Combobox(self, textvariable=self.intervalos_var, values=["10", "15", "20", "25"], state="readonly")

        self.generar_histograma_boton = tk.Button(self, text="Generar y Mostrar Histograma", command=self.controlador.generar_y_mostrar_histograma)

        self.scrollbar = tk.Scrollbar(self)
        self.resultado_text = tk.Text(self, height=5, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.resultado_text.yview)

    def _configurar_grid(self):
        self.cantidad_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cantidad_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.distribucion_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.rb_exponencial.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.rb_normal.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.rb_uniforme.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.parametros_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.parametro1_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.parametro1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.parametro2_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.parametro2_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        self.intervalos_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.intervalos_combo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.generar_histograma_boton.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        self.scrollbar.grid(row=5, column=2, padx=0, pady=5, sticky="ns")
        self.resultado_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

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
        histograma_ventana = tk.Toplevel(self)
        histograma_ventana.title(f"Histograma ({distribucion}, {num_intervalos} intervalos)")

        fig, ax = plt.subplots()
        ax.hist(numeros, bins=num_intervalos)
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        ax.set_title(f"Distribución {distribucion} ({num_intervalos} intervalos)")

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
                params["lambda"] = float(self.parametro1_entry.get()) if self.parametro1_entry.get() else 1.0
            except ValueError:
                return None, "Por favor, ingresa un número válido para lambda."
        elif self.distribucion_var.get() == "Normal":
            try:
                params["mu"] = float(self.parametro1_entry.get()) if self.parametro1_entry.get() else 0.0
                params["sigma"] = float(self.parametro2_entry.get()) if self.parametro2_entry.get() else 1.0
            except ValueError:
                return None, "Por favor, ingresa números válidos para mu y sigma."
        elif self.distribucion_var.get() == "Uniforme":
            try:
                params["a"] = float(self.parametro1_entry.get()) if self.parametro1_entry.get() else 0.0
                params["b"] = float(self.parametro2_entry.get()) if self.parametro2_entry.get() else 1.0
            except ValueError:
                return None, "Por favor, ingresa números válidos para a y b."
        return params, None

    def obtener_num_intervalos(self):
        return int(self.intervalos_var.get())