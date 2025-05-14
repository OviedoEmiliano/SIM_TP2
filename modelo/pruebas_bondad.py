from scipy.stats import chisquare
from scipy.stats import chi2
from scipy.stats import kstest
from scipy.stats import ksone
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


    # Este calculo lo hacemos para llevar de probabilidades a frecuencias absolutas
    frecEsperadas = np.array(frecEsperadas)*cantNrosGenerados
    # Y este otro calculo lo hacemos para reducir la discrepancia entre las frec observadas y las frec esperadas
    frecEsperadas *= (sum(frecObservadas) / sum(frecEsperadas))


    # Calcular chi tabla
    chi2_tabla = chi2.ppf(1 - alpha,  len(limitesIntervalos) - 1)

    chi2stat, p_value = chisquare(frecObservadas,frecEsperadas)
    return frecObservadas, frecEsperadas, chi2stat, chi2_tabla, p_value

# Calcular la prueba de bondad
def calcular_prueba_bondad_ks(
    array_nros_generados,
    distribucion,
    parametros_distribucion,
    alpha
):

    n = len(array_nros_generados)

    if distribucion == "Uniforme":
        a = parametros_distribucion.get("a", 0.0)
        b = parametros_distribucion.get("b",1.0)
        ks_stat, p_value = kstest(array_nros_generados,"uniform", args=(a,b-a))
    elif distribucion == "Normal":
        mu = parametros_distribucion.get("mu", 0.0)
        sigma = parametros_distribucion.get("sigma",1.0)
        ks_stat, p_value = kstest(array_nros_generados,"norm", args=(mu,sigma))
    elif distribucion == "Exponencial":
        lambda_p = parametros_distribucion.get("lambda", 0.0)
        ks_stat, p_value = kstest(array_nros_generados,"expon", args=(0,(1/lambda_p)))
    else:
        print("Error: no se ha especificado la distribución")

    ks_tabla = ksone.ppf(1 - alpha/2, n)
    return ks_stat, p_value, ks_tabla
