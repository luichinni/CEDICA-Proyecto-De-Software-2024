from core.enums.client_enum import AsignacionFamiliar, Condicion, Dias, Discapacidad, Pension, TipoDocs
from core.services.employee_service import EmployeeService
from core.services.equestrian_service import EquestrianService
from flask import Blueprint, request, render_template, redirect, url_for, flash
from web.forms.client_forms.client_file_search import ClientFileSearchForm
from web.forms.client_forms.client_search import ClientSearchForm
from src.core.services.client_service import ClientService, ClientDocuments
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error
from src.web.handlers import get_int_param, get_str_param, get_bool_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel
from src.web.forms.client_forms.create_client_form import ClientFirstForm, ClientSecondForm, ClientThirdForm, ClientFourthForm, ClientFifthForm, ClientSixthForm, ClientSeventhForm, PropuestaDeTrabajo, UploadFile, UploadLink
from flask import session
from src.web.forms.client_forms.procesadores import *


clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/listado',methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('home'))
def search():
    """Lista todos los clientes con paginación."""
    
    params = request.args
    params_dict = params.to_dict()
    
    form = ClientSearchForm()
    
    for param, valor in params_dict.items():
        if param in form._fields:
            form._fields[param].data = valor
    
    filtro = None
    
    if params.get('tipo_filtro', None) and params.get('busqueda', '') != '':
        filtro = {
            params['tipo_filtro']: params.get('busqueda')
        }
    
    
    order_by = params.get('orden_filtro',None)
    
    ascending = (params.get('orden','Ascendente') == 'Ascendente')
    
    page = int(params.get('page','1'))

    per_page = int(params.get('per_page','5'))

    clients, total, pages = ClientService.get_clients(filtro,page,per_page,order_by,ascending, like=True)
    
    listado = []

    if clients:
        for cliente in clients:
            listado.append({
                'id': cliente.id,
                'Nombre': cliente.nombre,
                'Apellido': cliente.apellido,
                'DNI': cliente.dni,
                'Atendido por': cliente.atendido_por
            })
    else:
        listado = [{
        'id': '0',
        'Nombre': '',
        'Apellido': '',
        'DNI': '',
        'Atendido por': ''
    }]
    
    return render_template('search_box.html', entidad='clients', anterior=url_for('home'), form=form, lista_diccionarios=listado, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado JyA')


@clients_bp.route('/create', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('clients.search'))
def new():
    forms = {
        'Datos personales': ClientFirstForm(),
        'Detalles': ClientSecondForm(),
        'Situacion previsional': ClientThirdForm(),
        'Institución Escolar': ClientFourthForm(),
        'Atencion': ClientFifthForm(),
        'Tutores legales': ClientSixthForm(),
        'Propuesta de trabajo': ClientSeventhForm()
    }
    
    validadores = {
        'Datos personales': procesar_primero,
        'Detalles': procesar_segundo,
        'Situacion previsional': procesar_tercero_y_quinto,
        'Institución Escolar': procesar_cuarto,
        'Atencion': procesar_tercero_y_quinto,
        'Tutores legales': procesar_sexto,
        'Propuesta de trabajo': procesar_septimo
    }

    activa = int(request.args.get('activa',0))
    ruta_post = url_for('clients.new')
    entidad = 'clients'
    titulo = 'Cargar J&A'
    url_volver = url_for('clients.search')

    empleados = [(emp.id, emp.dni + ': ' + emp.nombre + ' ' + emp.apellido) for emp in EmployeeService.get_all_employees()]
    forms['Propuesta de trabajo'].propuesta_trabajo.profesor_id.choices = empleados
    forms['Propuesta de trabajo'].propuesta_trabajo.conductor_id.choices = empleados
    forms['Propuesta de trabajo'].propuesta_trabajo.auxiliar_pista_id.choices = empleados
    forms['Propuesta de trabajo'].propuesta_trabajo.caballo_id.choices = [(eq.id, str(eq.id)+ ': ' + eq.nombre) for eq in EquestrianService.get_all_equestrian()[0]]

    if request.method == 'POST':
        datos = dict()
        for form in forms:
            forms[form].validate_on_submit()
            datos = {**datos,**validadores[form](forms[form])}
        
        ClientService.create_client(**datos)
        
        flash('JyA registrado con éxito!','success')
        
        return redirect(url_for('clients.search'))

    return render_template('client/multi_form.html', activa=activa,forms=forms, ruta_post=ruta_post, entidad=entidad,titulo=titulo,url_volver=url_volver)


@clients_bp.get('/<int:id>')
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda: url_for('clients.search'))
def detail(id: int):
    return redirect(url_for('client_files.search',id=id,activo='informacion'))

@clients_bp.route('/update/<int:id>', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda: url_for('clients.search'))
def update(id):
    forms = {
        'Datos personales': ClientFirstForm,
        'Detalles': ClientSecondForm,
        'Situacion previsional': ClientThirdForm,
        'Institución Escolar': ClientFourthForm,
        'Atencion': ClientFifthForm,
        'Tutores legales': ClientSixthForm,
        'Propuesta de trabajo': ClientSeventhForm
    }
    
    cliente_data = ClientService.get_client_by_id(id).to_dict()
    cliente_data['dias'] = [Dias[dia].value for dia in cliente_data['dias']]
        
    for form in forms:
        if request.method == 'GET':
            if form == 'Propuesta de trabajo':
                forms[form] = forms[form](data={'propuesta_trabajo':cliente_data})
            else:
                forms[form] = forms[form](data=cliente_data)
        else:
            forms[form] = forms[form]()
        
    
    validadores = {
        'Datos personales': procesar_primero,
        'Detalles': procesar_segundo,
        'Situacion previsional': procesar_tercero_y_quinto,
        'Institución Escolar': procesar_cuarto,
        'Atencion': procesar_tercero_y_quinto,
        'Tutores legales': procesar_sexto,
        'Propuesta de trabajo': procesar_septimo
    }

    activa = int(request.args.get('activa',0))
    ruta_post = url_for('clients.update', id=id)
    entidad = 'clients'
    titulo = 'Cargar J&A'
    url_volver = url_for('clients.search')

    empleados = [(emp.id, emp.dni + ': ' + emp.nombre + ' ' + emp.apellido) for emp in EmployeeService.get_all_employees()]
    forms['Propuesta de trabajo'].propuesta_trabajo.profesor_id.choices = empleados
    forms['Propuesta de trabajo'].propuesta_trabajo.conductor_id.choices = empleados
    forms['Propuesta de trabajo'].propuesta_trabajo.auxiliar_pista_id.choices = empleados
    forms['Propuesta de trabajo'].propuesta_trabajo.caballo_id.choices = [(eq.id, str(eq.id)+ ': ' + eq.nombre) for eq in EquestrianService.get_all_equestrian()[0]]

    if request.method == 'POST':
        
        datos = dict()
        for form in forms:
            forms[form].validate_on_submit()
            datos = {**datos,**validadores[form](forms[form])}
        
        ClientService.update_client(id,**datos)
        
        flash('Datos de JyA actualizados con éxito!', 'success')
        
        return redirect(url_for('clients.search'))

    return render_template('client/multi_form.html', activa=activa,forms=forms, ruta_post=ruta_post, entidad=entidad,titulo=titulo,url_volver=url_volver)

@clients_bp.post('/delete/<int:id>')
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda: url_for('clients.search'))
def delete(id):
    ClientService.delete_client(id)
    
    flash('JyA dado de baja con éxito!','success')
    
    return redirect(url_for('clients.search'))


clients_files_bp = Blueprint('client_files', __name__,url_prefix='/client_files')

@clients_files_bp.route('/upload/<int:id>/<string:es_link>', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('client_files.search'))
def new(id,es_link):
    es_link = (es_link.lower() == 'true')
    form = UploadFile() if not es_link else UploadLink()
    if form.validate_on_submit():
        flash('Documento cargado con éxito!','success')
        ClientService.add_document(id,form.titulo.data,form.archivo.data,form.tipo.data,es_link)
        return redirect(url_for('client_files.search',id=id, activo='documents'))
    
    return render_template('form.html',
                           url_volver=url_for('client_files.search',
                                            id=id,
                                            activo='documents'
                                        ),
                           ruta_post=url_for('client_files.new',
                                             id=id,
                                             es_link=es_link
                                        ),
                           form=form)

@clients_files_bp.route('/update/<int:id>/<int:id_entidad>/<string:es_link>', methods=['POST','GET'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('clients.search'))
def update(id:int, id_entidad: int,es_link:str):
    es_link = es_link=='True'
    
    archivo = ClientService.get_document_by_id(id).to_dict()
    if not es_link:
        archivo['titulo'] = ''.join(archivo['titulo'].split('_')[2:])
        
    archivo['tipo'] = archivo['tipo'].value
    
    archivo['archivo'] = archivo['ubicacion']
    
    form = None
    
    if request.method=='GET' and es_link and archivo['es_link']:
        form = UploadLink(data=archivo)
    
    elif request.method=='GET' and not es_link and not archivo['es_link']:
        form = UploadFile(data=archivo)
        del form.archivo
        
    elif request.method=='GET':
        raise ValueError('El documento no es válido')
    
    elif request.method == 'POST':
        if es_link:
            form = UploadLink()
        else:
            form = UploadFile()
            del form.archivo
        
        ClientService.update_document(id,form.titulo.data,form.tipo.data,form.archivo.data if es_link else '',es_link)
        
        flash('Documento actualizado con éxito!','success')
        
        return redirect(url_for('client_files.search',id=id_entidad, activo='documents'))
    
    return render_template('form.html',
                           url_volver=url_for('client_files.search',id=id_entidad, activo='documents'),
                           ruta_post=url_for('client_files.update',
                                             id=id,
                                             id_entidad=id_entidad,
                                             es_link=es_link
                                        ),
                           form=form)

@clients_files_bp.post('/delete/<int:id>')
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda: url_for('clients.search'))
def delete(id):
    ClientService.delete_document(id)
    
    flash('Documento dado de baja con éxito!')
    
    return redirect(request.referrer)


@clients_files_bp.get('/detail/<int:id>')
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda: url_for('clients.search'))
def detail(id):
    archivo = ClientService.get_document(id)
    
    if not archivo:
        raise ValueError('No existe el archivo')
    
    return redirect(archivo)

@clients_files_bp.route('/listado/<int:id>',methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda: url_for('clients.search'))
def search(id):
    """Lista todos los archivos con paginación."""
    params = request.args
    params_dict = params.to_dict()
    
    form = ClientFileSearchForm()
    
    for param, valor in params_dict.items():
        if param in form._fields:
            form._fields[param].data = valor
    
    filtro = None
    extension = params.get('tipo_filtro', None)
    
    if extension and extension.upper() not in ['PDF', 'DOC', 'XLS', 'JPEG','LINK']:
        extension = None
    
    if params.get('tipo_filtro', None) and params.get('busqueda', '') != '':
        # 'PDF', 'DOC', 'XLS', 'JPEG','Link'
        if params.get('tipo_filtro').upper() in ['PDF', 'DOC', 'XLS', 'JPEG']:
            filtro = {
                'titulo': params.get('busqueda')
            }
        elif params.get('tipo_filtro') == 'Link':
            filtro = {
                'titulo': params.get('busqueda')
            }
        else:
            filtro = {
                params['tipo_filtro'].lower(): params.get('busqueda')
            }
    
    activo = params.get('activo', 'informacion')
    
    order_by = params.get('orden_filtro',None)
    
    if not order_by or order_by == 'fecha_de_carga':
        order_by = 'created_at'
    
    ascending = (params.get('orden','Ascendente') == 'Ascendente')
    
    page = int(params.get('page','1'))

    per_page = int(params.get('per_page','5'))
    
    archivos, total, pages = ClientService.get_documents(id,filtro,extension,page,per_page,order_by,ascending, like=True)
    
    listado = []

    if archivos:
        for archivo in archivos:
            dict_archivo = archivo.to_dict()
            dict_archivo['ubicacion'] = 'Servidor Local' if dict_archivo['ubicacion'].startswith('client_files/') else 'Servidor Externo'
            dict_archivo['Fecha de carga'] = dict_archivo['created_at']
            del dict_archivo['created_at']
            listado.append(dict_archivo)
    else:
        # por si no hay que listar y que no se rompa
        listado = [{
        'id': '0',
        'Titulo':'',
        'es_link': True,
        'ubicacion': ''
    }]
    
    datos_cliente = ClientService.get_client_by_id(id).to_dict()

    profesor = EmployeeService.get_employee_by_id(int(datos_cliente['profesor_id']))
    conductor = EmployeeService.get_employee_by_id(int(datos_cliente['conductor_id']))
    auxiliar = EmployeeService.get_employee_by_id(int(datos_cliente['auxiliar_pista_id']))
    caballo = EquestrianService.get_equestrian_by_id(int(datos_cliente['caballo_id']))
    
    datos_front = {
        'id':datos_cliente['id'],
        'DNI': datos_cliente['dni'],
        'Nombre': datos_cliente['nombre'],
        'Apellido': datos_cliente['apellido'],
        'Fecha de nacimiento': datos_cliente['fecha_nacimiento'],
        'Lugar de nacimiento': datos_cliente['lugar_nacimiento']['localidad_nacimiento'] + ' provincia de ' + datos_cliente['lugar_nacimiento']['provincia_nacimiento'],
        'Domicilio': datos_cliente['domicilio']['calle'] 
            + ' n' 
            + datos_cliente['domicilio']['numero'] 
            + ('dpto ' + datos_cliente['domicilio']['departamento'] if datos_cliente['domicilio']['departamento'] else '') 
            + ', '
            + datos_cliente['domicilio']['localidad']
            + ' provincia de '
            + datos_cliente['domicilio']['provincia'],
        'Teléfono de contacto': datos_cliente['telefono'],
        'Nombre del contacto de emergencia': datos_cliente['contacto_emergencia']['nombre'],
        'Teléfono del contacto de emergencia': datos_cliente['contacto_emergencia']['telefono'],
        'Becado': 'Sí' if datos_cliente['becado'] else 'No',
        'Observaciones de beca': datos_cliente['obs_beca'],
        'Certificado de discapacidad': datos_cliente['cert_discapacidad'] if not datos_cliente['cert_discapacidad'].isnumeric() else Condicion(int(datos_cliente['cert_discapacidad'])).name.replace('_',' ').capitalize(),
        'Discapacidad': Discapacidad(datos_cliente['discapacidad']).name.replace('_',' ').capitalize(),
        'Asignación': AsignacionFamiliar(datos_cliente['asignacion']).name.replace('_',' ').capitalize(),
        'Pensión': Pension(datos_cliente['pension']).name.replace('_',' ').capitalize(),
        'Obra social': datos_cliente['obra_social'],
        'Nro de afiliado': datos_cliente['nro_afiliado'],
        'Posee curatela': 'Sí' if datos_cliente['curatela'] else 'No',
        'Observaciones': datos_cliente['observaciones'],
        'Profesionales que lo atienden': datos_cliente['atendido_por'],
        'Tutores responsables':'',
        'Propuesta de trabajo institucional': datos_cliente['propuesta_trabajo'],
        'Condición': 'Regular' if datos_cliente['condicion'] else 'Baja',
        'Sede': datos_cliente['sede'],
        'Dias': ' | '.join(datos_cliente['dias']),
        'Profesor asignado': profesor.nombre + ' ' + profesor.apellido + ' - ' + profesor.dni,
        'Conductor asignado': conductor.nombre + ' ' + conductor.apellido + ' - ' + conductor.dni,
        'Ecuestre asignado': caballo.nombre,
        'Auxiliar de pista asignado': auxiliar.nombre + ' ' + auxiliar.apellido + ' - ' + auxiliar.dni
    }
    
    if datos_cliente.get('institucion_escolar',None):
        datos_front = {
            **datos_front,
            'Institución escolar actual': datos_cliente['institucion_escolar']['nombre'],
            'Dirección de la institución escolar': datos_cliente['institucion_escolar']['direccion']['calle'] 
                + ' n' 
                + datos_cliente['institucion_escolar']['direccion']['numero']
                + ', '
                + datos_cliente['institucion_escolar']['direccion']['localidad']
                + ' provincia de '
                + datos_cliente['institucion_escolar']['direccion']['provincia'],
            'Teléfono de la institución escolar': datos_cliente['institucion_escolar']['telefono'],
            'Grado actual al que concurre': datos_cliente['institucion_escolar']['grado'],
            'Observaciones de la institución escolar': datos_cliente['institucion_escolar']['observaciones']
        }

    return render_template('different_detail.html', 
                           diccionario=datos_front,
                           activo=activo,
                           entidad='clients',
                           entidad_archivo='client_files',
                           anterior=url_for('clients.detail',id=id),
                           form=form, 
                           lista_diccionarios=listado,
                           total=total,
                           current_page=page,
                           per_page=per_page,
                           pages=pages,
                           titulo='Detalle'
                        )