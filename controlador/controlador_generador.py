import numpy as np
from modelo.generador_distribuciones import GeneradorDistribucionesModelo
from tkinter import messagebox
from vista.interfaz import InterfazGenerador
from modelo.pruebas_bondad import calcular_prueba_bondad_chi2
from modelo.pruebas_bondad import calcular_prueba_bondad_ks


class ControladorGenerador:
    def __init__(self, vista):
        # Inicializa el controlador con la vista y el modelo.
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

    def generar_y_mostrar_graficos(self):
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
            numeros_aleatorios = self.modelo.generar_aleatorios(
                cantidad, distribucion, parametros
            )
        except Exception as e:
            messagebox.showerror("Error al generar números", str(e))
            return

        # Mostrar los resultados y preparar navegación por páginas
        self.vista.numeros_generados = numeros_aleatorios
        self.vista.pagina_actual = 0
        self.vista.mostrar_pagina_resultados()

        # Mostrar Graficos
        num_intervalos = self.vista.obtener_num_intervalos()
        self.vista.crear_ventana_histograma(
            numeros_aleatorios, distribucion, num_intervalos
        )

        prueba_bondad_seleccionada = self.vista.obtener_prueba_bondad_seleccionada()
        alpha = self.vista.obtener_alpha()

        if prueba_bondad_seleccionada == "chi2":
            prueba_bondad = self.calcular_prueba_bondad_chi2(
                numeros_aleatorios,
                distribucion,
                parametros,
                alpha,
                num_intervalos,
            )
            self.vista.crear_ventana_prueba_bondad_chi2(prueba_bondad)
        elif prueba_bondad_seleccionada == "ks":
            prueba_bondad = self.calcular_prueba_bondad_ks(
                numeros_aleatorios,
                distribucion,
                parametros,
                alpha,
                num_intervalos
            )
            self.vista.crear_ventana_prueba_bondad_ks(prueba_bondad)

    def calcular_prueba_bondad_chi2(
        self, nros_generados, distribucion, parametros, alpha, cant_intervalos
    ):
        (
            frec_observadas,
            frec_esperadas,
            frec_observadas_agrupadas,
            frec_esperadas_agrupadas,
            valores_chi_individuales,
            chi_calculado,
            chi2_tabla,
        ) = calcular_prueba_bondad_chi2(
            nros_generados, distribucion, parametros, alpha, cant_intervalos
        )
        resultado_prueba = {
            "frec_observadas": frec_observadas,
            "frec_esperadas": frec_esperadas,
            "chi_calculado": chi_calculado,
            "frec_observadas_agrupadas": frec_observadas_agrupadas,
            "frec_esperadas_agrupadas": frec_esperadas_agrupadas,
            "valores_chi_individuales": valores_chi_individuales,
            "chi_tabla": chi2_tabla,
            "distribucion": distribucion,
            "alpha": alpha,
        }
        return resultado_prueba

    def calcular_prueba_bondad_ks(
        self, nros_generados, distribucion, parametros, alpha, intervalos
    ):
        (
            frecObservadas,
            frecEsperadas,
            prob_frec_obs,
            prob_frec_obs_acum,
            prob_frec_esp,
            prob_frec_esp_acum,
            dif_probs_acum,
            ks_calculado,
            ks_tabla,
        ) = calcular_prueba_bondad_ks(nros_generados, distribucion, parametros, alpha, intervalos)
        resultado_prueba = {
            "frecObservadas": frecObservadas,
            "frecEsperadas": frecEsperadas,
            "probFrecObs": prob_frec_obs,
            "probFrecObsAcum": prob_frec_obs_acum,
            "probFrecEsp": prob_frec_esp,
            "probFrecEspAcum": prob_frec_esp_acum,
            "diferenciasAcum": dif_probs_acum,
            "ksCalculado": ks_calculado,
            "ksTabla": ks_tabla,
            "distribucion": distribucion,
            "alpha": alpha,
        }
        return resultado_prueba


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
