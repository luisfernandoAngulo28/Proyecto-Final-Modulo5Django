from django.core.exceptions import ValidationError

def validar_par(value):
    if value % 2 != 0:
        raise ValidationError("El valor debe ser par")


def validar_texto_sin_numeros(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Este campo no debe contener numeros")

def validar_subject(value):
    if value == "prueba":
        raise ValidationError("El subject no debe ser prueba")
