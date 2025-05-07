import numpy as np
from modelo.generador_distribuciones import GeneradorDistribucionesModelo
from tkinter import messagebox
from vista.interfaz import InterfazGenerador

class ControladorGenerador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = GeneradorDistribucionesModelo()


    # Funcion para calcular el histograma, generarlo y devolverlo
    def generar_y_mostrar_histograma(self):
        try:
            cantidad_str = self.vista.obtener_cantidad()
            cantidad = int(cantidad_str)

            # Numero entre 1 y 1.000.000
            if not (1 <= cantidad <= 1000000):
                self.vista.mostrar_resultado("Por favor, ingresa una cantidad entre 1 y 1,000,000.")
                return

            distribucion = self.vista.obtener_distribucion()
            parametros, error_params = self.vista.obtener_parametros()
            if error_params:
                self.vista.mostrar_resultado(error_params)
                return

            numeros_aleatorios = self.modelo.generar_aleatorios(cantidad, distribucion, parametros)
            self.vista.numeros_generados = numeros_aleatorios
            self.vista.pagina_actual = 0
            self.vista.mostrar_pagina_resultados()

            num_intervalos = self.vista.obtener_num_intervalos()
            self.vista.mostrar_histograma(numeros_aleatorios, distribucion, num_intervalos)

            tabla = self.calcular_tabla_frecuencias(numeros_aleatorios, num_intervalos)
            self.vista.crear_ventana_tabla_frecuencias(tabla)

        except ValueError:
            self.vista.mostrar_resultado("Por favor, ingresa un número entero válido para la cantidad.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    # Funcion para calcular la tabla, generarla y devolverla
    def calcular_tabla_frecuencias(self, numeros, num_intervalos):
        conteo, limites = np.histogram(numeros, bins=num_intervalos)
        tabla = []
        total_datos = len(numeros)
        acumulado = 0
        for i in range(len(conteo)):
            intervalo = f"[{limites[i]:.4f} - {limites[i+1]:.4f})"
            frecuencia_absoluta = conteo[i]
            frecuencia_relativa = conteo[i] / total_datos if total_datos > 0 else 0
            acumulado += conteo[i]
            tabla.append((intervalo, frecuencia_absoluta, frecuencia_relativa, acumulado))
        return tabla

    # Funcion para mostrar la tabla de frecuencias
    def mostrar_tabla_frecuencias(self, tabla):
        self.vista.crear_ventana_tabla_frecuencias(tabla)

def main():
    vista = InterfazGenerador(None)  # No se pasan widgets aún
    controlador = ControladorGenerador(vista)
    vista.controlador = controlador  # Establecer el controlador
    vista.iniciar()  # Ahora sí, crear los widgets
    vista.mainloop()

if __name__ == "__main__":
    main()