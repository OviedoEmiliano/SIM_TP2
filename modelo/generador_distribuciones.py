import random
import math

class GeneradorDistribucionesModelo:
    def generar_aleatorios(self, cantidad, distribucion, parametros):
        """
        Genera una lista de números aleatorios según la distribución especificada.

        Args:
            cantidad (int): Número de valores a generar.
            distribucion (str): Tipo de distribución ("Exponencial", "Normal", "Uniforme").
            parametros (dict): Diccionario de parámetros necesarios según la distribución.

        Returns:
            list: Lista de números aleatorios generados y redondeados a 4 decimales.
        """

        if distribucion == "Exponencial":
            # Distribución Exponencial: X = -1/λ * ln(1 - U)
            lambda_param = parametros.get("lambda", 1.0)
            return [round(-1 / lambda_param * math.log(1 - random.random()), 4) for _ in range(cantidad)]

        elif distribucion == "Normal":
            # Distribución Normal usando el método de Box-Muller
            mu = parametros.get("mu", 0.0)
            sigma = parametros.get("sigma", 1.0)

            # Si la cantidad es impar, generamos un número extra y luego recortamos
            pares = cantidad if cantidad % 2 == 0 else cantidad + 1
            resultados = []

            for _ in range(pares // 2):
                u1 = random.random()
                u2 = random.random()
                r = math.sqrt(-2 * math.log(u1))
                z1 = r * math.cos(2 * math.pi * u2)
                z2 = r * math.sin(2 * math.pi * u2)
                resultados.extend([
                    round(mu + sigma * z1, 4),
                    round(mu + sigma * z2, 4)
                ])

            return resultados[:cantidad]  # Recorta si se generó uno extra

        elif distribucion == "Uniforme":
            # Distribución Uniforme en el intervalo [a, b]
            a = parametros.get("a", 0.0)
            b = parametros.get("b", 1.0)
            return [round(random.uniform(a, b), 4) for _ in range(cantidad)]

        else:
            # Distribución no reconocida
            return []
        
