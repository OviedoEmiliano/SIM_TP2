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
        a, b = parametrosDistribucion

        frecEsperadas = [
            ((limitesIntervalos[i + 1] - limitesIntervalos[i]) / (b - a))
            for i in range(len(limitesIntervalos) - 1)
        ]

    elif distribucion == "Normal":
        mu, sigma = parametrosDistribucion;
        frecEsperadas = [
            norm.cdf(limitesIntervalos[i+1], mu, sigma) - norm.cdf(limitesIntervalos[i], mu, sigma)
            for i in range(len(limitesIntervalos) - 1)
        ]
    elif distribucion == "Exponencial":
        lambda_p = parametrosDistribucion[0];
        
        frecEsperadas = [
            expon.cdf(limitesIntervalos[i+1], scale=1/lambda_p) - expon.cdf(limitesIntervalos[i], scale=1/lambda_p)
            for i in range(len(limitesIntervalos) - 1)
        ]
    else:
        print("Error: no se ha especificado la distribución")

    frecEsperadas = np.array(frecEsperadas)*cantNrosGenerados

    chi2stat, p_value = chisquare(frecObservadas,frecEsperadas)
    return chi2stat,p_value

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

