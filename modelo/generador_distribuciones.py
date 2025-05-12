import random
import numpy as np
import math

class GeneradorDistribucionesModelo:
    def generar_aleatorios(self, cantidad, distribucion, parametros):


        # PARA GENERAR NUMEROS ALEATORIOS CON DISTRIBUCION EXPONENCIAL utilizando la formula con el Lambda
        if distribucion == "Exponencial":
            lambda_param = parametros.get("lambda", 1.0)
            # Generar numero y redondear a 4 decimales
            numeros_aleatorios = [round(random.expovariate(lambda_param), 4) for _ in range(cantidad)]

        # PARA GENERAR NUMEROS ALEATORIOS CON DISTRIBUCION NORMAL utilizando la formula de Box-Muller
        elif distribucion == "Normal":
            mu_param = parametros.get("mu", 0.0)
            sigma_param = parametros.get("sigma", 1.0)
            # Generar numero y redondear a 4 decimales

            # Si la cantidad es impar, se genera un numero extra, por lo contrario estariamos generando un numero menos.
            pares = cantidad if cantidad % 2 == 0 else cantidad + 1
            numeros_aleatorios = [];
            for _ in range(pares//2):
                rand1 = random.random()
                rand2 = random.random()
                n1 = math.sqrt(-2 * math.log(rand1)) * math.cos(2 * math.pi * rand2)
                n2 = math.sqrt(-2 * math.log(rand1)) * math.sin(2 * math.pi * rand2)
                
                N1 = round(mu_param + sigma_param * n1, 4);
                N2 = round(mu_param + sigma_param * n2, 4);

                numeros_aleatorios.extend([N1, N2])

        # PARA GENERAR NUMEROS ALEATORIOS CON DISTRIBUCION UNIFORME utilizando Random
        elif distribucion == "Uniforme":
            a_param = parametros.get("a", 0.0)
            b_param = parametros.get("b", 1.0)
            # Generar numero y redondear a 4 decimales
            numeros_aleatorios = [round(random.uniform(a_param, b_param), 4) for _ in range(cantidad)]

        else:
            return []




        return numeros_aleatorios
    