import numpy as np
from modelo.generador_distribuciones import GeneradorDistribucionesModelo
from tkinter import messagebox
from vista.interfaz import InterfazGenerador

class ControladorGenerador:
    def __init__(self, vista):
        #Inicializa el controlador con la vista y el modelo.
        self.vista = vista
        self.modelo = GeneradorDistribucionesModelo()

    def validar_cantidad(self, cantidad_str):
        # Valida que la cantidad ingresada sea un número entero entre 1 y 1,000,000.
        
        try:
            cantidad = int(cantidad_str)
            if not (1 <= cantidad <= 1_000_000):
                return None, "Por favor, ingresa una cantidad entre 1 y 1,000,000."
            return cantidad, None
        except ValueError:
            return None, "Por favor, ingresa un número entero válido para la cantidad."

    def generar_y_mostrar_histograma(self):
        """
        Obtiene y valida entradas desde la vista, genera los números aleatorios,
        muestra resultados, histograma y tabla de frecuencias.
        """
        cantidad_str = self.vista.obtener_cantidad()
        cantidad, error = self.validar_cantidad(cantidad_str)
        if error:
            self.vista.mostrar_resultado(error)
            return

        distribucion = self.vista.obtener_distribucion()
        parametros, error_params = self.vista.obtener_parametros()
        if error_params:
            self.vista.mostrar_resultado(error_params)
            return

        try:
            numeros_aleatorios = self.modelo.generar_aleatorios(cantidad, distribucion, parametros)
        except Exception as e:
            messagebox.showerror("Error al generar números", str(e))
            return

        # Mostrar los resultados y preparar navegación por páginas
        self.vista.numeros_generados = numeros_aleatorios
        self.vista.pagina_actual = 0
        self.vista.mostrar_pagina_resultados()

        # Mostrar histograma y tabla de frecuencias
        num_intervalos = self.vista.obtener_num_intervalos()
        self.vista.mostrar_histograma(numeros_aleatorios, distribucion, num_intervalos)

        tabla = self.calcular_tabla_frecuencias(numeros_aleatorios, num_intervalos)
        self.mostrar_tabla_frecuencias(tabla)

    def calcular_tabla_frecuencias(self, numeros, num_intervalos):
        """
        Calcula la tabla de frecuencias (intervalos, frecuencia absoluta,
        frecuencia relativa y frecuencia acumulada) a partir de los datos generados.
        """
        conteo, limites = np.histogram(numeros, bins=num_intervalos)
        tabla = []
        total_datos = len(numeros)
        acumulado = 0

        for i in range(len(conteo)):
            intervalo = f"[{limites[i]:.4f}, {limites[i+1]:.4f})"
            frecuencia_absoluta = conteo[i]
            frecuencia_relativa = conteo[i] / total_datos if total_datos > 0 else 0
            acumulado += frecuencia_absoluta
            tabla.append((intervalo, frecuencia_absoluta, frecuencia_relativa, acumulado))
        return tabla

    def mostrar_tabla_frecuencias(self, tabla):
        # Envía la tabla de frecuencias calculada a la vista para que la muestre en una nueva ventana.
        self.vista.crear_ventana_tabla_frecuencias(tabla)


def configurar_app():
    # Configura la aplicación creando la vista y el controlador, y vinculándolos entre sí.
    vista = InterfazGenerador(None)
    controlador = ControladorGenerador(vista)
    vista.controlador = controlador
    return vista

def main():
    # Punto de entrada de la aplicación: inicia la interfaz gráfica.
    vista = configurar_app()
    vista.iniciar()
    vista.mainloop()

if __name__ == "__main__":
    main()