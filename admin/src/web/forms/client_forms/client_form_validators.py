from datetime import date
from wtforms import ValidationError
from src.core.enums.client_enum import Condicion

def OtroCertificadoRequired(form, field):
    if form.cert_discapacidad.data == str(Condicion.OTRO.value) and field.data == "":
        raise ValidationError("Falta especificación del certificado que dispone")
    
def validate_not_in_future(form, field):
    if field.data > date.today():
        raise ValidationError('La fecha no puede ser mayor a la fecha actual.')