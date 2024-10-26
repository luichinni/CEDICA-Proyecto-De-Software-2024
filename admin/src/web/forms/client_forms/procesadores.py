from core.services.employee_service import EmployeeService
from core.services.equestrian_service import EquestrianService

def procesar_domicilio(campo):
    """Genera el diccionario con la direccion segun el campo de WTForms

    Args:
        campo (Any): Campo que contiene los elementos calle, numero, departamento, localidad y provincia

    Returns:
        dict: Diccionario formateado de la dirección o domicilio
    """
    return {
        'calle': campo.calle.data,
        'numero': campo.numero.data,
        'departamento': campo.departamento.data,
        'localidad': campo.localidad.data,
        'provincia': campo.provincia.data
    }


def procesar_primero(form):
    """Procesa el primer formulario de cliente, genera el diccionario con la informacion formateada

    Args:
        form (FlaskForm): Objeto que hereda de FlaskForm, debe entrar cargado y validado

    Returns:
        dict: diccionario con los campos del formulario formateados
    """
    datos = dict()
    for f1 in form:
        if f1.name == 'csrf_token':
            continue
        
        if f1.name == 'contacto_emergencia':
            datos[f1.name] = {
                'nombre': f1.form.nombre.data,
                'telefono': f1.form.telefono.data
            }
            
        elif f1.name == 'domicilio':
            datos[f1.name] = procesar_domicilio(f1.form)
        
        elif f1.name == 'lugar_nacimiento':
            datos[f1.name] = {
                'localidad_nacimiento':f1.form.localidad_nacimiento.data,
                'provincia_nacimiento':f1.form.provincia_nacimiento.data
            }
            
        else:
            datos[f1.name] = f1.data
                    
    return datos


def procesar_segundo(form):
    """Procesa el segundo formulario de cliente, genera el diccionario con la informacion formateada

    Args:
        form (FlaskForm): Objeto que hereda de FlaskForm, debe entrar cargado y validado

    Returns:
        dict: diccionario con los campos del formulario formateados
    """
    datos = dict()
    for f24 in form:
        if f24.name == 'csrf_token':
            continue
        
        if f24.name == 'otro_cert' and f24.data is not None and f24.data:
            datos['cert_discapacidad'] = f24.data
            
        else:
            datos[f24.name] = f24.data # guardo segundo paso
    
    return datos


def procesar_tercero_y_quinto(form):
    """Procesa el tercer y quinto formulario de cliente, genera el diccionario con la informacion formateada

    Args:
        form (FlaskForm): Objeto que hereda de FlaskForm, debe entrar cargado y validado

    Returns:
        dict: diccionario con los campos del formulario formateados
    """
    datos = dict()
    for f3 in form:
        if f3.name == 'csrf_token':
            continue
        
        datos[f3.name] = f3.data # tercera parte
    
    return datos


def procesar_cuarto(form):
    """Procesa el cuarto formulario de cliente, genera el diccionario con la informacion formateada

    Args:
        form (FlaskForm): Objeto que hereda de FlaskForm, debe entrar cargado y validado

    Returns:
        dict: diccionario con los campos del formulario formateados
    """
    datos = dict()
    datos['institucion_escolar'] = {
        'nombre': form.institucion_escolar.nombre.data,
        'direccion': procesar_domicilio(form.institucion_escolar.direccion),
        'telefono': form.institucion_escolar.telefono.data,
        'grado': form.institucion_escolar.grado.data,
        'observaciones': form.institucion_escolar.observaciones.data
    }
    
    return datos


def procesar_sexto(form):
    """Procesa el sexto formulario de cliente, genera el diccionario con la informacion formateada

    Args:
        form (FlaskForm): Objeto que hereda de FlaskForm, debe entrar cargado y validado

    Returns:
        dict: diccionario con los campos del formulario formateados
    """
    responsables = {}
    for f5 in form:
        if f5.name == 'csrf_token':
            continue
        
        for index, tutor_form in enumerate(form[f5.name].entries):
            responsables[index] = {
                'parentesco': tutor_form.parentesco.data,
                'nombre': tutor_form.nombre.data,
                'apellido': tutor_form.apellido.data,
                'dni': tutor_form.dni.data,
                'domicilio': procesar_domicilio(tutor_form.domicilio),
                'telefono': tutor_form.telefono.data,
                'email': tutor_form.email.data,
                'escolaridad': tutor_form.escolaridad.data,
                'ocupacion': tutor_form.ocupacion.data
            }
            
    return {"tutores_responsables":responsables}


def procesar_septimo(form):
    """Procesa el septimo formulario de cliente, genera el diccionario con la informacion formateada

    Args:
        form (FlaskForm): Objeto que hereda de FlaskForm, debe entrar cargado y validado

    Returns:
        dict: diccionario con los campos del formulario formateados
    """
    datos = dict()
    for f6 in form.propuesta_trabajo.form:
        nombre = f6.name.split('-')[1]
        
        if nombre == 'csrf_token':
            continue
        
        if nombre in ['profesor_id','conductor_id','auxiliar_pista_id']:
            EmployeeService.get_employee_by_id(int(f6.data))
            datos[nombre] = f6.data
            
        elif (nombre == 'caballo_id'):
            EquestrianService.get_equestrian_by_id(int(f6.data))
            datos[nombre] = f6.data
            
        else:
            datos[nombre] = f6.data
    
    return datos