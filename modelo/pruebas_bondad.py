from scipy.stats import chisquare
from scipy.stats import kstest
from scipy.stats import norm
from scipy.stats import expon
import numpy as np


# Calcular la prueba de bondad
def calcular_prueba_bondad_chi2(
    arrayNrosGenerados, distribucion, parametrosDistribucion, alpha, intervalos
):
    cantNrosGenerados = len(arrayNrosGenerados)
    frecObservadas, limitesIntervalos = np.histogram(
        arrayNrosGenerados, bins=intervalos
    )

    frecEsperadas = []

    if distribucion == "Uniforme":
        a = parametrosDistribucion.get("a", 0.0)
        b = parametrosDistribucion.get("b",1.0)
        
        
        frecEsperadas = [
            ((limitesIntervalos[i + 1] - limitesIntervalos[i]) / (b - a))
            for i in range(len(limitesIntervalos) - 1)
        ]

    elif distribucion == "Normal":
        mu = parametrosDistribucion.get("mu",0.0)
        sigma = parametrosDistribucion.get("sigma",1.0);
        frecEsperadas = [
            norm.cdf(limitesIntervalos[i+1], mu, sigma) - norm.cdf(limitesIntervalos[i], mu, sigma)
            for i in range(len(limitesIntervalos) - 1)
        ]
    elif distribucion == "Exponencial":
        lambda_p = parametrosDistribucion.get("lambda", 1.0)
        
        frecEsperadas = [
            expon.cdf(limitesIntervalos[i+1], scale=1/lambda_p) - expon.cdf(limitesIntervalos[i], scale=1/lambda_p)
            for i in range(len(limitesIntervalos) - 1)
        ]
    else:
        print("Error: no se ha especificado la distribución")




    print("\n\n Frecuecnias esperadas: ",frecEsperadas,"\n\n Frecuecnias observadas: ", frecObservadas)
    frecEsperadas = np.array(frecEsperadas)*cantNrosGenerados
    frecEsperadas *= (sum(frecObservadas) / sum(frecEsperadas))


    print("\n\n ACA HICIMOS LOS CALCULOS DE LA FREC ESP\n\n")
    print("\n\n Frecuecnias esperadas: ",frecEsperadas,"\n\n Frecuecnias observadas: ", frecObservadas)
    chi2stat, p_value = chisquare(frecObservadas,frecEsperadas)
    return frecObservadas, frecEsperadas, chi2stat, p_value

# Calcular la prueba de bondad
def calcular_prueba_bondad_ks(
    arrayNrosGenerados,
    distribucion,
    parametrosDistribucion,
):

    if distribucion == "Uniforme":
        pass
    elif distribucion == "Normal":
        pass
    elif distribucion == "Exponencial":
        pass
    else:
        print("Error: no se ha especificado la distribución")

