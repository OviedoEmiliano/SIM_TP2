from modelo.generador_distribuciones import GeneradorDistribucionesModelo
from tkinter import messagebox
from vista.interfaz import InterfazGenerador

class ControladorGenerador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = GeneradorDistribucionesModelo()

    def generar_y_mostrar_histograma(self):
        try:
            cantidad_str = self.vista.obtener_cantidad()
            cantidad = int(cantidad_str)
            if not (1 <= cantidad <= 1000000):
                self.vista.mostrar_resultado("Por favor, ingresa una cantidad entre 1 y 1,000,000.")
                return

            distribucion = self.vista.obtener_distribucion()
            parametros, error_params = self.vista.obtener_parametros()
            if error_params:
                self.vista.mostrar_resultado(error_params)
                return

            numeros_aleatorios = self.modelo.generar_aleatorios(cantidad, distribucion, parametros)
            self.vista.mostrar_resultado(f"Números generados ({distribucion}):\n{numeros_aleatorios[:cantidad]}")

            num_intervalos = self.vista.obtener_num_intervalos()
            self.vista.mostrar_histograma(numeros_aleatorios, distribucion, num_intervalos)

        except ValueError:
            self.vista.mostrar_resultado("Por favor, ingresa un número entero válido para la cantidad.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

def main():
    vista = InterfazGenerador(None)  # No se pasan widgets aún
    controlador = ControladorGenerador(vista)
    vista.controlador = controlador  # Establecer el controlador
    vista.iniciar()  # Ahora sí, crear los widgets
    vista.mainloop()

if __name__ == "__main__":
    main()