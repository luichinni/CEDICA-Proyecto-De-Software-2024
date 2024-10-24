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
from src.web.forms.client_forms.create_client_form import ClientFirstForm, ClientSecondForm, ClientThirdForm, ClientFourthForm, ClientFifthForm, ClientSixthForm, ClientSeventhForm, UploadFile, UploadLink
from flask import session


clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/listado',methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.INDEX.value}")
#@handle_error(lambda: url_for('home'))
def search_clients():
    """Lista todos los clientes con paginación."""
    """params = request.args.keys()
    
    page = params['page'] if params['page'] is not None else 1
    per_page = params['per_page'] if params['per_page'] is not None else 25
    
    filtro = None
    
    users, total, pages = ClientService.get_clients(filtro=filtro,page=page, per_page=per_page)
    
    return render_template('user/list.html', users=users, total=total, pages=pages, current_page=page, per_page=per_page)"""
    
    params = request.args
    params_dict = params.to_dict()
    
    form = ClientSearchForm()
    
    print(params)
    
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
    
    page = int(getattr(params,'page','1'))

    per_page = int(getattr(params,'per_page','25'))

    print(filtro, order_by,ascending, page, per_page)

    clients, total, pages = ClientService.get_clients(filtro,page,per_page,order_by,ascending, like=True)
    
    listado = []

    if clients:
        print('entra')
        for cliente in clients:
            listado.append({
                'id': cliente.id,
                'Nombre': cliente.nombre,
                'Apellido': cliente.apellido,
                'DNI': cliente.dni,
                'Atendido por': cliente.atendido_por
            })
    else:
        # por si no hay que listar y que no se rompa
        listado = [{
        'id': '0',
        'Nombre': '',
        'Apellido': '',
        'DNI': '',
        'Atendido por': ''
    }]
    
    print(listado)
    
    #anterior=request.referrer
    return render_template('search_box.html', entidad='clients', anterior=url_for('home'), form=form, lista_diccionarios=listado, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado JyA')


@clients_bp.route('/create', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}")
#@handle_error(lambda: url_for('clients.new_clients'))
def new_clients():
    forms = {
        'Datos personales': ClientFirstForm(),
        'Detalles': ClientSecondForm(),
        'Situacion previsional': ClientThirdForm(),
        'Institución Escolar': ClientFourthForm(),
        'Atencion': ClientFifthForm(),
        'Tutores legales': ClientSixthForm(),
        'Propuesta de trabajo': ClientSeventhForm()
    }

    activa = int(request.args.get('activa',0))
    ruta_post = url_for('clients.new_clients')
    entidad = 'clients'
    titulo = 'Cargar J&A'
    url_volver = url_for('clients.search_clients')

    return render_template('client/multi_form.html', activa=activa,forms=forms, ruta_post=ruta_post, entidad=entidad,titulo=titulo,url_volver=url_volver)

    """ paso = session.get('paso',default=0)
    paso = paso if (paso < 7) else 0
    forms = [ClientFirstForm(),ClientSecondForm(), ClientThirdForm(), ClientFourthForm(), ClientFifthForm(), ClientSixthForm(), ClientSeventhForm()]

    if (paso == 6) or (paso == 5):
        empleados = [(emp.id, emp.dni + ': ' + emp.nombre + ' ' + emp.apellido) for emp in EmployeeService.get_all_employees()]
        forms[paso if paso == 6 else 6].propuesta_trabajo.profesor_id.choices = empleados
        forms[paso if paso == 6 else 6].propuesta_trabajo.conductor_id.choices = empleados
        forms[paso if paso == 6 else 6].propuesta_trabajo.auxiliar_pista_id.choices = empleados
        forms[paso if paso == 6 else 6].propuesta_trabajo.caballo_id.choices = [(eq.id, str(eq.id)+ ': ' + eq.nombre) for eq in EquestrianService.get_all_equestrian()[0]]
    
    if request.method == 'POST' and forms[paso].validate_on_submit():
        datos = dict()
        if paso == 0:
            for f1 in forms[paso]:
                if f1.name == 'csrf_token':
                    continue
                
                if f1.name == 'contacto_emergencia':
                    datos[f1.name] = {
                        'nombre': f1.form.nombre.data,
                        'telefono': f1.form.telefono.data
                    }
                    
                elif f1.name == 'domicilio':
                    datos[f1.name] = f1.form.calle.data +' N'+f1.form.numero.data
                    if f1.form.departamento.data:
                        datos[f1.name] += ' dpto ' + f1.form.departamento.data
                    
                    datos[f1.name] += ' ' + f1.form.localidad.data
                    datos[f1.name] += ', ' + f1.form.provincia.data
                
                elif f1.name == 'lugar_nacimiento':
                    datos[f1.name] = f1.form.localidad_nacimiento.data + ' provincia de ' + f1.form.provincia_nacimiento.data
                    
                else:
                    datos[f1.name] = f1.data
        
        elif paso == 1:
            for f24 in forms[paso]:
                if f24.name == 'csrf_token':
                    continue
                
                if f24.name == 'otro_cert' and f24.data is not None and f24.data:
                    datos['cert_discapacidad'] = f24.data
                else:
                    datos[f24.name] = f24.data # guardo segundo paso
        
        elif paso == 2 or paso == 4:
            for f3 in forms[paso]:
                if f3.name == 'csrf_token':
                    continue
                
                datos[f3.name] = f3.data # tercera parte
                
        elif paso == 3:
            datos['institucion_escolar'] = {
                'nombre': forms[paso].institucion_escolar.nombre.data,
                'direccion': {
                    'calle': forms[paso].institucion_escolar.direccion.calle.data,
                    'numero': forms[paso].institucion_escolar.direccion.numero.data,
                    'departamento': forms[paso].institucion_escolar.direccion.departamento.data,
                    'localidad': forms[paso].institucion_escolar.direccion.localidad.data,
                    'provincia': forms[paso].institucion_escolar.direccion.provincia.data,
                },
                'telefono': forms[paso].institucion_escolar.telefono.data,
                'grado': forms[paso].institucion_escolar.grado.data,
                'observaciones': forms[paso].institucion_escolar.observaciones.data
            }
        
        elif paso == 5:
            responsables = dict()
            for f5 in forms[paso]:
                if f5.name == 'csrf_token':
                    continue
                
                for index, tutor_form in enumerate(forms[paso][f5.name].entries):
                    responsables[index] = {
                        'parentesco': tutor_form.parentesco.data,
                        'nombre': tutor_form.nombre.data,
                        'apellido': tutor_form.apellido.data,
                        'dni': tutor_form.dni.data,
                        'domicilio': {
                            'calle': tutor_form.domicilio.calle.data,
                            'numero': tutor_form.domicilio.numero.data,
                            'dpto': tutor_form.domicilio.departamento.data,
                            'localidad': tutor_form.domicilio.localidad.data,
                            'provincia': tutor_form.domicilio.provincia.data
                        },
                        'telefono': tutor_form.telefono.data,
                        'email': tutor_form.email.data,
                        'escolaridad': tutor_form.escolaridad.data,
                        'ocupacion': tutor_form.ocupacion.data
                    }
            
            datos['tutores_responsables'] = responsables
            
        elif paso == 6:
            datos = dict()
            for f6 in forms[paso].propuesta_trabajo.form:
                nombre = f6.name.split('-')[1]
                
                if nombre == 'csrf_token':
                    continue
                
                if nombre in ['profesor_id','conductor_id','auxiliar_pista_id']:
                    EmployeeService.get_employee_by_id(int(f6.data))
                    datos[nombre] = f6.data
                else:
                    datos[nombre] = f6.data

        ClientService.validate_data(**datos) # lanzar error si falla algo

        session['cliente'] = datos if (paso == 0) else {**session['cliente'], **datos} # guardo datos acumulados
        
        paso += 1
        session['paso'] = paso
        
        print(session['cliente'])
    
    if request.method == 'GET' and session.get('cliente',{}):
        flash('Parece que estabas cargando un Jinete o Amazonas!', 'warning')
    
    if paso <= 6:
        form = forms[paso]
        
        return render_template('/client/paginated_form.html', form=form, ruta_post=url_for('.new_clients'), activa=paso,tabs=["Datos Personales", "Detalles", "Situacion previsional", "Institucion Escolar", "Atención", "Tutores Legales", "Propuesta de Trabajo"])
    else:
        ClientService.create_client(**session['cliente'])
        del session['cliente']
        del session['paso']
        return redirect(url_for('clients.search_clients')) """


@clients_bp.route('/create/cancelar', methods=['GET','POST'])
#@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}")
#@handle_error(lambda: url_for('auth.index'))
def cancelar_form():
    if session.get('cliente',0):
        del session['cliente']
    if session.get('paso',0):
        del session['paso']
    return redirect(url_for('clients.search_clients'))


@clients_bp.get('/<int:id>')
def detail_clients(id: int):
    return redirect(url_for('client_file.search_client_file',id=id))

@clients_bp.get('/update')
def update_clients():
    pass

@clients_bp.post('/delete/<int:id>')
def delete_clients(id):
    ClientService.delete_client(id)
    flash('JyA dado de baja con éxito','success')
    return redirect(url_for('clients.search_clients'))


clients_files_bp = Blueprint('client_file', __name__,url_prefix='/client_file')

@clients_files_bp.route('/upload/<int:id>/<string:es_link>', methods=['GET','POST'])
def new_client_file(id,es_link):
    es_link = (es_link.lower() == 'true')
    form = UploadFile() if not es_link else UploadLink()
    if form.validate_on_submit():
        flash('Cargado exitosamente','success')
        ClientService.add_document(id,form.titulo.data,form.archivo.data,form.tipo.data,es_link)
        return redirect(url_for('client_file.search_client_file',id=id, active='documents'))
    
    return render_template('form.html',
                           anterior=url_for('client_file.search_client_file',
                                            id=id,
                                            activo='documents'
                                        ),
                           ruta_post=url_for('client_file.new_client_file',
                                             id=id,
                                             es_link=es_link
                                        ),
                           form=form)

@clients_files_bp.get('/update/<int:id>/<string:es_link>')
def update_client_file(id:int,es_link:str):
    return redirect(request.referrer)

@clients_files_bp.post('/delete/<int:id>')
def delete_client_file(id):
    ClientService.delete_document(id)
    return redirect(request.referrer)


@clients_files_bp.get('/detail/<int:id>')
def detail_client_file(id):
    archivo = ClientService.get_document(id)
    
    if not archivo:
        raise ValueError('No existe el archivo')
    
    return redirect(archivo)

@clients_files_bp.route('/search/<int:id>',methods=['GET','POST'])
def search_client_file(id):
    """Lista todos los archivos con paginación."""
    
    params = request.args
    params_dict = params.to_dict()
    
    form = ClientFileSearchForm()
    
    for param, valor in params_dict.items():
        if param in form._fields:
            form._fields[param].data = valor
    
    filtro = None
    
    if params.get('tipo_filtro', None) and params.get('busqueda', '') != '':
        filtro = {
            params['tipo_filtro']: params.get('busqueda')
        }
    
    activo = params.get('activo', 'informacion')
    
    order_by = params.get('orden_filtro',None)
    
    ascending = (params.get('orden','Ascendente') == 'Ascendente')
    
    page = int(getattr(params,'page','1'))

    per_page = int(getattr(params,'per_page','25'))

    print(filtro, order_by,ascending, page, per_page)

    archivos, total, pages = ClientService.get_documents(id,filtro,page,per_page,order_by,ascending, like=True)

    
    listado = []

    if archivos:
        print('entra')
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

    #anterior=request.referrer
    return render_template('different_detail.html', 
                           diccionario=datos_cliente,
                           activo=activo,
                           entidad='clients',
                           entidad_archivos='client_file',
                           anterior=url_for('clients.detail_clients',id=id),
                           form=form, 
                           lista_diccionarios=listado,
                           total=total,
                           current_page=page,
                           per_page=per_page,
                           pages=pages,titulo='Detalle'
                        )
