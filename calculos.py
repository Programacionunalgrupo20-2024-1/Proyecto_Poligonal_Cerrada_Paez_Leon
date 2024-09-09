# calculations.py
from math import atan, degrees, fabs



class ConversionError(Exception):
    def __init__(self, gms_string, message="Formato de GMS no válido"):
        super().__init__(message)
        self.gms_string = gms_string
        self.message = message

    def __str__(self):
        return f"{self.message}: '{self.gms_string}"


def convertir_a_gms(angulo_puntos):
    try:
        # Divide el ángulo en grados, minutos y segundos usando el punto como delimitador
        partes = angulo_puntos.split('.')
        if len(partes) != 3:
            raise ValueError("Formato inválido")
        grados, minutos, segundos = map(float, partes)
        return f"{int(grados)}° {int(minutos)}′ {segundos:.2f}″"
    except ValueError as e:
        # Lanza una excepción con un mensaje detallado
        raise ConversionError(angulo_puntos) from e        


def decimal_a_dms(grados_decimales):
    grados = int(grados_decimales)
    minutos = int((grados_decimales - grados) * 60)
    segundos = (grados_decimales - grados - minutos / 60) * 3600
    return f"{grados}° {minutos}′ {segundos:.2f}″"

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

def convertir_gms_a_decimal(gms_string):
    # Divide el string GMS en partes para convertir a formato decimal
    try:
        grados, minutos, segundos = map(float, gms_string.replace("°", "").replace("′", "").replace("″", "").split())
        return grados + (minutos / 60) + (segundos / 3600)
    except ValueError as e:
        raise ValueError(f"Formato de GMS no válido: {gms_string}") from e