from flask_wtf import FlaskForm
from wtforms import ValidationError
from src.core.enums.client_enum import Condicion

def OtroCertificadoRequired(form, field):
    if form.cert_discapacidad.data == str(Condicion.OTRO.name) and field.data == "":
        raise ValidationError("Falta especificación del certificado que dispone")