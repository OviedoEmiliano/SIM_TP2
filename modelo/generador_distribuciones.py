import random
import numpy as np

class GeneradorDistribucionesModelo:
    def generar_aleatorios(self, cantidad, distribucion, parametros):


        # PARA GENERAR NUMEROS ALEATORIOS CON DISTRIBUCION EXPONENCIAL
        if distribucion == "Exponencial":
            lambda_param = parametros.get("lambda", 1.0)
            # Generar numero y redondear a 4 decimales
            numeros_aleatorios = [round(random.expovariate(lambda_param), 4) for _ in range(cantidad)]

        # PARA GENERAR NUMEROS ALEATORIOS CON DISTRIBUCION NORMAL
        elif distribucion == "Normal":
            mu_param = parametros.get("mu", 0.0)
            sigma_param = parametros.get("sigma", 1.0)
            # Generar numero y redondear a 4 decimales
            numeros_aleatorios = [round(num, 4) for num in np.random.normal(mu_param, sigma_param, cantidad).tolist()]

        # PARA GENERAR NUMEROS ALEATORIOS CON DISTRIBUCION UNIFORME
        elif distribucion == "Uniforme":
            a_param = parametros.get("a", 0.0)
            b_param = parametros.get("b", 1.0)
            # Generar numero y redondear a 4 decimales
            numeros_aleatorios = [round(random.uniform(a_param, b_param), 4) for _ in range(cantidad)]

        else:
            return []




        return numeros_aleatorios
    