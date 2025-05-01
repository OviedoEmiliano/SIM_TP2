import random
import numpy as np

class GeneradorDistribucionesModelo:
    def generar_aleatorios(self, cantidad, distribucion, parametros):
        numeros_aleatorios = []
        if distribucion == "Exponencial":
            lambda_param = parametros.get("lambda", 1.0)
            numeros_aleatorios = [random.expovariate(lambda_param) for _ in range(cantidad)]
        elif distribucion == "Normal":
            mu_param = parametros.get("mu", 0.0)
            sigma_param = parametros.get("sigma", 1.0)
            numeros_aleatorios = np.random.normal(mu_param, sigma_param, cantidad).tolist()
        elif distribucion == "Uniforme":
            a_param = parametros.get("a", 0.0)
            b_param = parametros.get("b", 1.0)
            numeros_aleatorios = [random.uniform(a_param, b_param) for _ in range(cantidad)]
        return numeros_aleatorios