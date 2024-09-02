# calculations.py
from math import atan, degrees, fabs

def decimal_a_dms(grados_decimales):
    grados = int(grados_decimales)
    minutos = int((grados_decimales - grados) * 60)
    segundos = (grados_decimales - grados - minutos / 60) * 3600
    return grados, minutos, segundos

def determinar_cuadrante(x, y):
    if x > 0 and y > 0:
        return "I"
    elif x > 0 and y < 0:
        return "II"
    elif x < 0 and y < 0:
        return "III"
    elif x < 0 and y > 0:
        return "IV"
    elif x == 0 and y != 0:
        return "Eje Y"
    elif y == 0 and x != 0:
        return "Eje X"
    else:
        return "Origen"

def calcular_azimut(cuadrante, angulo):
    if cuadrante == "I":
        return angulo
    elif cuadrante == "II":
        return 180 - angulo
    elif cuadrante == "III":
        return 180 + angulo
    elif cuadrante == "IV":
        return 360 - angulo
    else:
        return 0
