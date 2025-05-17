import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math

ventana_histograma_activa = None
ventana_tabla_frecuencias_activa = None
ventana_prueba_bondad_activa = None


class InterfazGenerador(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        print(f"Controlador en InterfazGenerador.__init__: {controlador}")
        self.controlador = controlador
        self.title("Generador de Números Aleatorios")
        self.numeros_generados = []
        self.pagina_actual = 0
        self.tamano_pagina = 200
        self.distribucion_var = tk.StringVar(value="Uniforme")
        self.intervalos_var = tk.StringVar(value="10")

    def iniciar(self):
        self._crear_pantalla_principal()
        self._configurar_grid()
        self._mostrar_parametros(2)

    """


    
        FUNCIONES PARA VER LA VENTANA PRINCIPAL

    
        
    """

    # Seccion donde se carga la cantidad de numeros a generar.
    def _seccion_cantidad_numeros(self):
        self.cantidad_label = tk.Label(self, text="Cantidad de números a generar:")
        self.cantidad_entry = tk.Entry(self)

    # Seccion donde se puede seleccionar la distribucion.
    def _seccion_seleccion_distribucion(self):
        self.distribucion_frame = tk.LabelFrame(self, text="Tipo de Distribución")
        self.rb_exponencial = tk.Radiobutton(
            self.distribucion_frame,
            text="Exponencial (lambda)",
            variable=self.distribucion_var,
            value="Exponencial",
            command=lambda: self._mostrar_parametros(1),
        )
        self.rb_normal = tk.Radiobutton(
            self.distribucion_frame,
            text="Normal (mu, sigma)",
            variable=self.distribucion_var,
            value="Normal",
            command=lambda: self._mostrar_parametros(2),
        )
        self.rb_uniforme = tk.Radiobutton(
            self.distribucion_frame,
            text="Uniforme (a, b)",
            variable=self.distribucion_var,
            value="Uniforme",
            command=lambda: self._mostrar_parametros(2),
        )

    # Seccion donde se cargan los parametros de acuerdo a la distribucion.
    def _seccion_parametros(self):
        self.parametros_frame = tk.LabelFrame(self, text="Parámetros")
        self.parametro1_label = tk.Label(self.parametros_frame, text="Parámetro 1:")
        self.parametro1_entry = tk.Entry(self.parametros_frame)
        self.parametro2_label = tk.Label(self.parametros_frame, text="Parámetro 2:")
        self.parametro2_entry = tk.Entry(self.parametros_frame)

    # Seccion donde se selecciona la prueba de bondad que se ejecutara.
    def _seccion_pruebas_bondad(self):
        self.prueba_var = tk.StringVar(value="chi2")
        self.prueba_de_bondad = tk.LabelFrame(self, text="Prueba de Bondad")
        self.prueba_chi_cuadrado = tk.Radiobutton(
            self.prueba_de_bondad,
            text="Chi Cuadrado",
            variable=self.prueba_var,
            value="chi2",
        )
        self.prueba_ks = tk.Radiobutton(
            self.prueba_de_bondad,
            text="Kolmogorov-Smirnov",
            variable=self.prueba_var,
            value="ks",
        )

        self.alpha_label = tk.Label(self.prueba_de_bondad, text="Alfa:")
        self.alpha_entry = tk.Entry(self.prueba_de_bondad)

    # Seccion donde se seleccionan los intervalos y generan los graficos.
    def _seccion_generar_mostrar_graficos(self):
        self.intervalos_label = tk.Label(self, text="Número de intervalos:")
        self.intervalos_combo = ttk.Combobox(
            self,
            textvariable=self.intervalos_var,
            values=["10", "15", "20", "25"],
            state="readonly",
        )

        self.generar_mostrar_boton = tk.Button(
            self,
            text="Generar Números y Mostrar Graficos",
            command=self.controlador.generar_y_mostrar_graficos,
        )

    # Seccion donde se muestran los nros generados y paginados.
    def _seccion_mostrar_nros_generados_paginados(self):
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

    # Funcion para crear las secciones de la ventana principal.
    def _crear_pantalla_principal(self):
        self._seccion_cantidad_numeros()
        self._seccion_seleccion_distribucion()
        self._seccion_parametros()
        self._seccion_pruebas_bondad()
        self._seccion_generar_mostrar_graficos()
        self._seccion_mostrar_nros_generados_paginados()

    """
    


        FUNCIONES PARA ORGANIZAR LA VENTANA PRINCIPAL (GRID)



    """

    def _grid_cantidad_numeros(self):
        self.cantidad_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cantidad_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def _grid_seleccion_distribucion(self):
        self.distribucion_frame.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.rb_exponencial.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.rb_normal.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.rb_uniforme.grid(row=2, column=0, padx=5, pady=2, sticky="w")

    def _grid_parametros(self):
        self.parametros_frame.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.parametro1_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.parametro1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.parametro2_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.parametro2_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    def _grid_pruebas_bondad(self):
        self.prueba_de_bondad.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )

        self.prueba_chi_cuadrado.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.prueba_ks.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.alpha_label.grid(row=2, column=0, padx=(0, 2), pady=5, sticky="e")
        self.alpha_entry.grid(row=2, column=1, padx=(2, 0), pady=5, sticky="w")

    def _grid_generar_mostrar_graficos(self):
        self.intervalos_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.intervalos_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.generar_mostrar_boton.grid(
            row=7, column=0, columnspan=2, padx=5, pady=10, sticky="ew"
        )

    def _grid_mostrar_nros_generados_paginados(self):
        self.scrollbar.grid(row=5, column=2, padx=0, pady=5, sticky="ns")
        self.resultado_text.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )
        self.boton_anterior.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        self.boton_siguiente.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

    # Funcion para configurar el grid de la ventana principal y ordenar los elementos.
    def _configurar_grid(self):
        self._grid_cantidad_numeros()
        self._grid_seleccion_distribucion()
        self._grid_parametros()
        self._grid_pruebas_bondad()
        self._grid_generar_mostrar_graficos()
        self._grid_mostrar_nros_generados_paginados()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)

    """

    

    FUNCIONES QUE SON UTILIZADAS DENTRO DE LAS SECCIONES

    

    """

    # Funcion para mostrar los campos de los parametros de la distribucion seleccionada
    def _mostrar_parametros(self, num_params):
        distribucion = self.distribucion_var.get()
        if num_params == 1:
            self.parametro1_label.config(text="Lambda:")
            self.parametro1_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.parametro1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
            self.parametro2_label.grid_forget()
            self.parametro2_entry.grid_forget()
        elif num_params == 2:
            if distribucion == "Normal":
                self.parametro1_label.config(text="Mu:")
                self.parametro2_label.config(text="Sigma:")
            elif distribucion == "Uniforme":
                self.parametro1_label.config(text="a:")
                self.parametro2_label.config(text="b:")
            else:
                self.parametro1_label.config(text="Parámetro 1:")
                self.parametro2_label.config(text="Parámetro 2:")

            self.parametro1_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
            self.parametro1_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
            self.parametro2_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
            self.parametro2_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        # Funcion para calcular la Anterior Pagina

    # Funcion para calcular la Pagina Anterior
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

    """
    


    FUNCIONES UTILIZADAS PARA OBTENER LOS VALORES INGRESADOS EN CADA SECCION

    

    """

    # Funcion para obtener la cantidad de numeros a generar
    def obtener_cantidad(self):
        return self.cantidad_entry.get()

    # Funcion para obtener la distribucion seleccionada
    def obtener_distribucion(self):
        return self.distribucion_var.get()

    # Funcion para obtener los parametros de la distribucion seleccionada, exponencial: labda, normal: mu y sigma, uniforme: a y b.
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

    # Funcion para obtener el numero de intervalos seleccionados para el histograma
    def obtener_num_intervalos(self):
        return int(self.intervalos_var.get())

    # Funcion para obtener el alpha ingresado
    def obtener_alpha(self):
        return float(self.alpha_entry.get()) if self.alpha_entry.get() else 0.05

    # Funcion para obtener la prueba de bondad seleccionada
    def obtener_prueba_bondad_seleccionada(self):
        return self.prueba_var.get()

    """
    


    FUNCIONES USADAS EN EL CONTROLADOR

    

    """

    # Funcion para mostrar los numeros generados en el cuadro de texto
    def mostrar_resultado(self, texto):
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, texto)
        self.resultado_text.see(tk.END)

    # Funcion para mostrar la pagina con todos los numeros generados llamando a la funcion mostrar_resultados
    def mostrar_pagina_resultados(self):
        if not self.numeros_generados:
            return

        inicio = self.pagina_actual * self.tamano_pagina
        fin = inicio + self.tamano_pagina
        pagina = self.numeros_generados[inicio:fin]

        # Seteamos la cantidad de columnas
        columnas = 10
        texto = f"Números página {self.pagina_actual + 1}:\n\n"
        for i, num in enumerate(pagina):
            texto += f"{num:<10}"  # 10 caracteres de ancho, alineado a la izquierda
            if (i + 1) % columnas == 0:
                texto += "\n"

        self.mostrar_resultado(texto)

    # Funcion para mostrar el histograma en una ventana nueva
    def crear_ventana_histograma(self, numeros, distribucion, num_intervalos):
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

    # Funcion para mostrar el resultado de la prueba de bondad de CHI CUADRADO.
    def crear_ventana_prueba_bondad_chi2(self, resultado_prueba):
        global ventana_prueba_bondad_activa

        if ventana_prueba_bondad_activa:
            ventana_prueba_bondad_activa.destroy()

        nueva_ventana = tk.Toplevel(self)
        nueva_ventana.title("Prueba de Bondad")

        resultado_text = tk.Text(nueva_ventana, wrap=tk.WORD)
        resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(nueva_ventana, command=resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        resultado_text.config(yscrollcommand=scrollbar.set)

        # Deshabilitar la edición del Text widget
        resultado_text.config(state=tk.DISABLED)

        # Extraer datos del diccionario
        frec_obs = resultado_prueba.get("frec_observadas", [])
        frec_esp = resultado_prueba.get("frec_esperadas", [])
        frec_obs_agrup = resultado_prueba.get("frec_observadas_agrupadas", [])
        frec_esp_agrup = resultado_prueba.get("frec_esperadas_agrupadas", [])
        valores_chi = resultado_prueba.get("valores_chi_individuales", [])
        chi_calculado = resultado_prueba.get("chi_calculado", 0)
        chi_tabla = resultado_prueba.get("chi_tabla", 0)
        alpha = resultado_prueba.get("alpha", 0)
        distribucion = resultado_prueba.get("distribucion", "desconocida")

        # Crear el texto de la tabla
        resultado = "=== Prueba de Bondad Chi² ===\n\n"
        resultado += f"Distribución hipotética: {distribucion}\n"
        resultado += f"Estadístico Chi² Calculado: {chi_calculado:.4f}\n"
        if chi_tabla is not None:
            resultado += f"Estadístico Chi² de Tabla: {chi_tabla:.4f}\n"
        resultado += f"Nivel de significancia (α): {alpha:.4f}\n\n"

        resultado += "Resultado de la Prueba:\n"
        if chi_tabla is not None:
            if chi_calculado <= chi_tabla:
                resultado += f"📊 Como {chi_calculado:.4f} <= {chi_tabla:.4f}, NO hay suficiente evidencia para rechazar la H₀: 'Los numeros generados siguen una distribucion: {distribucion}'. \n\n"
            else:
                resultado += f"📊 Como {chi_calculado:.4f} > {chi_tabla:.4f}, se RECHAZA la H₀: 'Los numeros generados siguen una distribucion: {distribucion}'.\n\n"

        # Encabezados
        resultado += (
            f"{'Intervalo':>9} | {'Frec Obs':>8} | {'Frec Esp':>8} | "
            f"{'Int Agrup':>9} | {'Obs Agrup':>9} | {'Esp Agrup':>9} | {'Chi² Ind':>9}\n"
        )
        resultado += "-" * 88 + "\n"

        intervalo_agrup = 1
        for i in range(len(frec_obs)):
            # Etiqueta intervalo acumulado sólo si está dentro del rango de acumulados
            if i < len(frec_obs_agrup):

                etiqueta_intervalo_acum = f"{intervalo_agrup}"
                obs_agrup = frec_obs_agrup[i]
                esp_agrup = frec_esp_agrup[i]
                chi_ind = valores_chi[i]
            else:
                etiqueta_intervalo_agrup = 0
                obs_agrup = 0
                esp_agrup = 0
                chi_ind = 0

            resultado += (
                f"{i + 1:9} | {frec_obs[i]:8} | {frec_esp[i]:8.4f} | "
                f"{etiqueta_intervalo_acum:>9} | {obs_agrup:>9} | {esp_agrup:>9.4f} | {chi_ind:>9.4f}\n"
            )
            intervalo_agrup += 1
        resultado += (
            f"{'':9}  {'':8}  {'':8}  "
            f"{'':9}  {'':9}  {'Total':>14} | {chi_calculado:>9.4f}\n"
        )

        # Insertar texto y habilitar scroll
        resultado_text.config(state=tk.NORMAL)
        resultado_text.insert(tk.END, resultado)
        resultado_text.config(state=tk.DISABLED)

        # Guardar la ventana para poder cerrarla después
        ventana_prueba_bondad_activa = nueva_ventana

    # Funcion para mostrar el resultado de la prueba de bondad de Kolmogorov-Smirnov
    def crear_ventana_prueba_bondad_ks(self, resultado_prueba):
        global ventana_prueba_bondad_activa

        if ventana_prueba_bondad_activa:
            ventana_prueba_bondad_activa.destroy()

        nueva_ventana = tk.Toplevel(self)
        nueva_ventana.title("Prueba de Bondad KS")

        resultado_text = tk.Text(nueva_ventana, wrap=tk.WORD)
        resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(nueva_ventana, command=resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        resultado_text.config(yscrollcommand=scrollbar.set)

        # Deshabilitar la edición del Text widget
        resultado_text.config(state=tk.DISABLED)

        # Extraer datos del diccionario
        frec_obs = resultado_prueba.get("frecObservadas", [])
        frec_esp = resultado_prueba.get("frecEsperadas", [])
        prob_frec_obs = resultado_prueba.get("probFrecObs", [])
        prob_frec_obs_acum = resultado_prueba.get("probFrecObsAcum", [])
        prob_frec_esp = resultado_prueba.get("probFrecEsp", [])
        prob_frec_esp_acum = resultado_prueba.get("probFrecEspAcum", [])
        dif_acum = resultado_prueba.get("diferenciasAcum", [])
        ks_calculado = resultado_prueba.get("ksCalculado", 0)
        ks_tabla = resultado_prueba.get("ksTabla", 0)
        alpha = resultado_prueba.get("alpha", 0)
        distribucion = resultado_prueba.get("distribucion", "desconocida")

        # Crear texto principal
        resultado = "=== Prueba de Bondad Kolmogorov-Smirnov (KS) ===\n\n"
        resultado += f"Distribución hipotética: {distribucion}\n"
        resultado += f"Estadístico KS Calculado: {ks_calculado:.4f}\n"
        resultado += f"Estadístico KS de Tabla: {ks_tabla:.4f}\n"
        resultado += f"Nivel de significancia (α): {alpha:.4f}\n\n"

        resultado += "Resultado de la Prueba:\n"
        if ks_calculado <= ks_tabla:
            resultado += f"📊 Como {ks_calculado:.4f} <= {ks_tabla:.4f}, NO hay suficiente evidencia para rechazar la H₀: 'Los números generados siguen una distribución: {distribucion}'.\n\n"
        else:
            resultado += f"📊 Como {ks_calculado:.4f} > {ks_tabla:.4f}, se RECHAZA la H₀: 'Los números generados siguen una distribución: {distribucion}'.\n\n"

        # Encabezados
        resultado += (
            f"{'Intervalo':>9} | {'Frec Obs':>8} | {'Frec Esp':>8} | "
            f"{'P(Obs)':>8} | {'P(Esp)':>8} | {'P(Obs) Ac':>10} | {'P(Esp) Ac':>10} | {'|Dif|':>7}\n"
        )
        resultado += "-" * 90 + "\n"

        for i in range(len(frec_obs)):
            resultado += (
                f"{i + 1:9} | {frec_obs[i]:8} | {frec_esp[i]:8.4f} | "
                f"{prob_frec_obs[i]:8.4f} | {prob_frec_esp[i]:8.4f} | "
                f"{prob_frec_obs_acum[i]:10.4f} | {prob_frec_esp_acum[i]:10.4f} | {dif_acum[i]:7.4f}\n"
            )

        resultado += (
            f"{'':>70} {'Max KS':>8} | {ks_calculado:>7.4f}\n"
        )

        # Insertar texto y habilitar scroll
        resultado_text.config(state=tk.NORMAL)
        resultado_text.insert(tk.END, resultado)
        resultado_text.config(state=tk.DISABLED)

        # Guardar referencia
        ventana_prueba_bondad_activa = nueva_ventana