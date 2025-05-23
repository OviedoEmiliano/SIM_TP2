from scipy.stats import chi2
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

    # Calculo de Frecuencias Esperadas
    frecEsperadas = []

    if distribucion == "Uniforme":
        a = parametrosDistribucion.get("a", 0.0)
        b = parametrosDistribucion.get("b", 1.0)

        frecEsperadas = [
            ((limitesIntervalos[i + 1] - limitesIntervalos[i]) / (b - a))
            for i in range(len(limitesIntervalos) - 1)
        ]

    elif distribucion == "Normal":
        mu = parametrosDistribucion.get("mu", 0.0)
        sigma = parametrosDistribucion.get("sigma", 1.0)
        frecEsperadas = [
            norm.cdf(limitesIntervalos[i + 1], mu, sigma)
            - norm.cdf(limitesIntervalos[i], mu, sigma)
            for i in range(len(limitesIntervalos) - 1)
        ]
    elif distribucion == "Exponencial":
        lambda_p = parametrosDistribucion.get("lambda", 1.0)

        frecEsperadas = [
            expon.cdf(limitesIntervalos[i + 1], scale=1 / lambda_p)
            - expon.cdf(limitesIntervalos[i], scale=1 / lambda_p)
            for i in range(len(limitesIntervalos) - 1)
        ]
    else:
        print("Error: no se ha especificado la distribución")

    frecEsperadas = np.array(frecEsperadas) * cantNrosGenerados
    frecEsperadas *= sum(frecObservadas) / sum(frecEsperadas)

    # Calculate individual Chi-squared values for the original frequencies
    valores_chi_individuales_original = []
    for i in range(len(frecObservadas)):
        if frecEsperadas[i] != 0:
            res = ((frecObservadas[i] - frecEsperadas[i]) ** 2) / frecEsperadas[i]
            valores_chi_individuales_original.append(res)
        else:
            valores_chi_individuales_original.append(0) # Handle division by zero

    # Agrupamiento
    frec_esperadas_agrupadas = []
    frec_observadas_agrupadas = []
    acum_esp = 0
    acum_obs = 0

    for i in range(len(frecEsperadas)):
        acum_esp += frecEsperadas[i]
        acum_obs += frecObservadas[i]
        if acum_esp >= 5:
            frec_esperadas_agrupadas.append(acum_esp)
            frec_observadas_agrupadas.append(acum_obs)
            acum_esp = 0
            acum_obs = 0

    if acum_esp > 0:
        if len(frec_esperadas_agrupadas) > 0:
            frec_esperadas_agrupadas[-1] += acum_esp
            frec_observadas_agrupadas[-1] += acum_obs
        else:
            frec_esperadas_agrupadas.append(acum_esp)
            frec_observadas_agrupadas.append(acum_obs)

    chi_calculado = 0
    valores_chi_individuales_agrupados = [] # Renamed for clarity
    for i in range(len(frec_esperadas_agrupadas)):
        if frec_esperadas_agrupadas[i] != 0:
            res = ((frec_observadas_agrupadas[i] - frec_esperadas_agrupadas[i]) ** 2) / (
                frec_esperadas_agrupadas[i]
            )
            chi_calculado += res
            valores_chi_individuales_agrupados.append(res)
        else:
            valores_chi_individuales_agrupados.append(0) # Handle division by zero


    chi2_tabla = chi2.ppf(1 - alpha, len(frec_esperadas_agrupadas) - 1)

    return (
        frecObservadas,
        frecEsperadas,
        frec_observadas_agrupadas,
        frec_esperadas_agrupadas,
        valores_chi_individuales_original, # New return value
        valores_chi_individuales_agrupados,
        chi_calculado,
        chi2_tabla,
    )


def calcular_prueba_bondad_ks(
    array_nros_generados, distribucion, parametros_distribucion, alpha, intervalos
):

    n = len(array_nros_generados)
    frecObservadas, limitesIntervalos = np.histogram(
        array_nros_generados, bins=intervalos
    )

    frecEsperadas = []

    if distribucion == "Uniforme":
        a = parametros_distribucion.get("a", 0.0)
        b = parametros_distribucion.get("b", 1.0)
        frecEsperadas = [
            ((limitesIntervalos[i + 1] - limitesIntervalos[i]) / (b - a))
            for i in range(len(limitesIntervalos) - 1)
        ]
    elif distribucion == "Normal":
        mu = parametros_distribucion.get("mu", 0.0)
        sigma = parametros_distribucion.get("sigma", 1.0)
        frecEsperadas = [
            norm.cdf(limitesIntervalos[i + 1], mu, sigma)
            - norm.cdf(limitesIntervalos[i], mu, sigma)
            for i in range(len(limitesIntervalos) - 1)
        ]
    elif distribucion == "Exponencial":
        lambda_p = parametros_distribucion.get("lambda", 1.0)
        frecEsperadas = [
            expon.cdf(limitesIntervalos[i + 1], scale=1 / lambda_p)
            - expon.cdf(limitesIntervalos[i], scale=1 / lambda_p)
            for i in range(len(limitesIntervalos) - 1)
        ]
    else:
        print("Error: no se ha especificado la distribución")

    frecEsperadas = np.array(frecEsperadas) * len(array_nros_generados)
    frecEsperadas *= sum(frecObservadas) / sum(frecEsperadas)

    prob_frec_obs = []
    prob_frec_esp = []
    prob_obs_acum = 0
    prob_esp_acum = 0
    prob_frec_obs_acum = []
    prob_frec_esp_acum = []
    for i in range(len(frecEsperadas)):
        prob_obs = frecObservadas[i] / len(array_nros_generados)
        prob_frec_obs.append(prob_obs)
        prob_obs_acum += prob_obs
        prob_frec_obs_acum.append(prob_obs_acum)

        prob_esp = frecEsperadas[i] / len(array_nros_generados)
        prob_frec_esp.append(prob_esp)
        prob_esp_acum += prob_esp
        prob_frec_esp_acum.append(prob_esp_acum)

    dif_probs_acum = []
    for i in range(len(prob_frec_esp)):
        res = abs(prob_frec_obs_acum[i] - prob_frec_esp_acum[i])
        dif_probs_acum.append(res)

    ks_calculado = max(dif_probs_acum)
    ks_tabla = ksone.ppf(1 - alpha / 2, n)

    # === Agrupamiento por Frecuencia Esperada < 5 ===
    frec_obs_agrup = []
    frec_esp_agrup = []
    prob_obs_agrup = []
    prob_esp_agrup = []
    prob_obs_acum_agrup = []
    prob_esp_acum_agrup = []
    dif_acum_agrup = []

    acum_obs = 0
    acum_esp = 0
    acum_prob_obs = 0
    acum_prob_esp = 0

    for i in range(len(frecEsperadas)):
        acum_obs += frecObservadas[i]
        acum_esp += frecEsperadas[i]
        acum_prob_obs += prob_frec_obs[i]
        acum_prob_esp += prob_frec_esp[i]

        if acum_esp >= 5:
            frec_obs_agrup.append(acum_obs)
            frec_esp_agrup.append(acum_esp)
            prob_obs_agrup.append(acum_prob_obs)
            prob_esp_agrup.append(acum_prob_esp)
            prob_obs_acum_agrup.append(sum(prob_obs_agrup))
            prob_esp_acum_agrup.append(sum(prob_esp_agrup))
            dif_acum_agrup.append(abs(sum(prob_obs_agrup) - sum(prob_esp_agrup)))

            acum_obs = 0
            acum_esp = 0
            acum_prob_obs = 0
            acum_prob_esp = 0

    if acum_esp > 0:
        if len(frec_esp_agrup) > 0:
            frec_obs_agrup[-1] += acum_obs
            frec_esp_agrup[-1] += acum_esp
            prob_obs_agrup[-1] += acum_prob_obs
            prob_esp_agrup[-1] += acum_prob_esp
            prob_obs_acum_agrup[-1] = sum(prob_obs_agrup)
            prob_esp_acum_agrup[-1] = sum(prob_esp_agrup)
            dif_acum_agrup[-1] = abs(prob_obs_acum_agrup[-1] - prob_esp_acum_agrup[-1])
        else:
            frec_obs_agrup.append(acum_obs)
            frec_esp_agrup.append(acum_esp)
            prob_obs_agrup.append(acum_prob_obs)
            prob_esp_agrup.append(acum_prob_esp)
            prob_obs_acum_agrup.append(acum_prob_obs)
            prob_esp_acum_agrup.append(acum_prob_esp)
            dif_acum_agrup.append(abs(acum_prob_obs - acum_prob_esp))

    return (
        frecObservadas,
        frecEsperadas,
        prob_frec_obs,
        prob_frec_obs_acum,
        prob_frec_esp,
        prob_frec_esp_acum,
        dif_probs_acum,
        ks_calculado,
        ks_tabla,
        frec_obs_agrup,
        frec_esp_agrup,
        prob_obs_agrup,
        prob_esp_agrup,
        prob_obs_acum_agrup,
        prob_esp_acum_agrup,
        dif_acum_agrup,
    )