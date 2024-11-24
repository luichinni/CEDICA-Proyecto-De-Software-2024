from flask import render_template, Blueprint, redirect, request, url_for, flash

from core.models.employee.employee import TipoDoc
from src.core.services.employee_service import EmployeeService
from src.core.services.user_service import UserService
from web.forms.client_forms.client_search import ClientSearchForm
from web.forms.client_forms.create_client_form import UploadFile, UploadLink
from web.forms.employee_forms.CreateEmployeeForm import CreateEmployeeForm
from web.forms.employee_forms.EditEmployeeForm import EditEmployeeForm
from web.forms.employee_forms.SearchEmployeeForm import SearchEmployeeForm
from web.handlers.auth import check_permissions
from web.handlers import handle_error, get_int_param, get_str_param, get_bool_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel
from src.web.forms.client_forms.client_file_search import FileSearchForm

bp = Blueprint('employees', __name__, url_prefix='/employee')

def collect_employee_data_from_form(form):
    """Retorna los datos del form en formato de diccionario"""
    return {
            'nombre': form.nombre.data,
            'apellido': form.apellido.data,
            'dni': form.dni.data,
            'domicilio': form.domicilio.data,
            'localidad': form.localidad.data,
            'telefono': form.telefono.data,
            'profesion': form.profesion.data.upper(),
            'puesto_laboral': form.puesto_laboral.data.upper(),
            'fecha_inicio': form.fecha_inicio.data,
            'fecha_cese': form.fecha_cese.data,
            'contacto_emergencia_nombre': form.contacto_emergencia_nombre.data,
            'contacto_emergencia_telefono': form.contacto_emergencia_telefono.data,
            'obra_social': form.obra_social.data,
            'nro_afiliado': form.nro_afiliado.data,
            'condicion': form.condicion.data.replace(' ','_').upper(),
            'activo': bool(form.activo.data),
        }

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.NEW.value}")
def new():
    """Crear un empleado"""
    form = CreateEmployeeForm()
    if form.validate_on_submit():
        new_employee_data = collect_employee_data_from_form(form)
        new_employee_data['email'] = form.email.data
        EmployeeService.add_employee(**new_employee_data)
        flash("Se registro el empleado exitosamente", "success")
        return redirect(url_for('employees.search'))
    context = {
        'form': form,
        'titulo': 'Crear un empleado',
        'url_post': url_for('employees.new'),
        'url_volver': url_for('employees.search')
    }
    return render_template('form.html', **context)

@bp.route('/', methods=['GET'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.INDEX.value}")
def index():
    """Listar los empleados"""
    params = request.args
    page = get_int_param(params, 'page', 1, True)
    per_page = get_int_param(params, 'per_page', 5, True)

    employees, total, pages = EmployeeService.get_employees(page=page, per_page=per_page)

    lista_diccionarios = [employee.to_dict() for employee in employees]
    return render_template('list.html', lista_diccionarios=lista_diccionarios, entidad="employees")

@bp.route('/search', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.INDEX.value}")
def search():
    params = request.args

    filtros = {'email': get_str_param(params, 'email', optional=True),
               'nombre': get_str_param(params, 'nombre', optional=True),
               'apellido': get_str_param(params, 'apellido', optional=True),
               'dni': get_str_param(params, 'dni', optional=True),
               'puesto_laboral': get_str_param(params, 'puesto_laboral', optional=True)}
    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 5, optional=True)
    order_by = get_str_param(params, 'order_by', 'created_at', optional=True)
    ascending = get_bool_param(params, 'ascending', True, optional= True)

    employees, total, pages = EmployeeService.get_employees(
        filtro=filtros,
        page=page,
        per_page=per_page,
        order_by=order_by,
        ascending=ascending)

    lista_diccionarios = [employee.to_dict() for employee in employees]

    form = SearchEmployeeForm(**params.to_dict())

    return render_template('search_box.html',
                                              form=form,
                                              entidad='employees',
                                              anterior=url_for('home'),
                                              lista_diccionarios=lista_diccionarios,
                                              total=total,
                                              current_page=page,
                                              per_page =per_page,
                                              pages=pages,
                                              titulo='Listado de empleados')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda id: url_for('employees.search'))
def update(id):
    """Editar un empleado existente"""
    employee = EmployeeService.get_employee_by_id(id)
    if not employee:
        flash("El empleado seleccionado no existe", "danger")
        return redirect(url_for('employees.search'))
    form = EditEmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee_data = collect_employee_data_from_form(form)
        EmployeeService.update_employee(employee, **employee_data)
        flash(f"Empleado {employee.nombre} {employee.apellido} actualizado con éxito", "success")
        return redirect(url_for('employees.search'))
    context = {
        'form': form,
        'titulo': 'Editar un empleado',
        'url_post': url_for('employees.update', id=id),
        'url_volver': url_for('employees.search')
    }
    return render_template('form.html', **context)

@bp.route('/delete/<int:id>', methods=['POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda id: url_for('employees.search'))
def delete(id):
    """Eliminar un empleado de manera logica"""
    employee_to_delete = EmployeeService.get_employee_by_id(id)
    if not employee_to_delete:
        flash("El empleado seleccionado no existe", "danger")
    else:
        users = employee_to_delete.user
        [UserService.delete_user(user.id) for user in users if not user.deleted]
        EmployeeService.delete_employee(id)
        flash("Se elimino el empleado exitosamente", "success")
    return redirect(url_for('employees.search'))

@bp.route('<int:id>', methods=['GET'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda id: url_for('employees.search'))
def detail(id):
    #employee = EmployeeService.get_employee_by_id(id)
    #if not employee:
    #    flash(f'Empleado con ID {id} no encontrado', 'warning')
    #    return redirect(url_for('employees.search'))

    #titulo = f'Detalle del empleado {employee.nombre} {employee.apellido}'
    #anterior = url_for('employees.search')
    #diccionario = employee.to_dict()
    #entidad = 'employees'

    #return render_template('detail.html', titulo=titulo, anterior=anterior, diccionario= diccionario, entidad=entidad )
    return redirect(
        url_for('employee_files.search',
                id=id,
                activo='informacion'
                )
    )


employee_files_bp = Blueprint('employee_files', __name__,url_prefix='/employee_files')


@employee_files_bp.route('/upload/<int:id>/<string:es_link>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda id, es_link: url_for('employee_files.search', id=id, activo='documents'))
def new(id, es_link):
    es_link = (es_link.lower() == 'true')
    form = UploadFile() if not es_link else UploadLink()
    form.tipo.choices = [(tipo.value,tipo.name.replace('_',' ').capitalize()) for tipo in TipoDoc]
    if form.validate_on_submit():
        flash('Documento cargado con éxito!', 'success')
        EmployeeService.add_document(id, form.titulo.data, form.archivo.data, form.tipo.data, es_link)
        return redirect(url_for('employee_files.search', id=id, activo='documents'))

    return render_template(
        'form.html',
        url_volver=url_for(
            'employee_files.search',
            id=id,
            activo='documents'
        ),
        ruta_post=url_for(
            'employee_files.new',
            id=id,
            es_link=es_link
        ),
        form=form
    )


@employee_files_bp.route('/update/<int:id>/<int:id_entidad>/<string:es_link>', methods=['POST', 'GET'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda id, id_entidad, es_link: url_for('employees.search'))
def update(id: int, id_entidad: int, es_link: str):
    es_link = es_link == 'True'

    archivo = EmployeeService.get_document_by_id(id).to_dict()
    if not es_link:
        archivo['titulo'] = ''.join(archivo['titulo'].split('_')[2:])

    archivo['tipo'] = archivo['tipo'].value

    archivo['archivo'] = archivo['ubicacion']

    form = None

    if request.method == 'GET' and es_link and archivo['es_link']:
        form = UploadLink(data=archivo)

    elif request.method == 'GET' and not es_link and not archivo['es_link']:
        form = UploadFile(data=archivo)
        del form.archivo

    elif request.method == 'GET':
        raise ValueError('El documento no es válido')

    elif request.method == 'POST':
        if es_link:
            form = UploadLink()
        else:
            form = UploadFile()
            del form.archivo

        EmployeeService.update_document(id, form.titulo.data, form.tipo.data, form.archivo.data if es_link else '',
                                      es_link)

        flash('Documento actualizado con éxito!', 'success')

        return redirect(url_for('employee_files.search', id=id_entidad, activo='documents'))

    return render_template(
        'form.html',
        url_volver=url_for(
            'employee_files.search',
            id=id_entidad,
            activo='documents'
        ),
        ruta_post=url_for(
            'employee_files.update',
            id=id,
            id_entidad=id_entidad,
            es_link=es_link
        ),
        form=form
    )


@employee_files_bp.post('/delete/<int:id>')
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda id: url_for('employees.search'))
def delete(id):
    EmployeeService.delete_document(id)

    flash('Documento dado de baja con éxito!')

    return redirect(request.referrer)


@employee_files_bp.get('/detail/<int:id>')
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda id: url_for('employees.search'))
def detail(id):
    archivo = EmployeeService.get_document(id)

    if not archivo:
        raise ValueError('No existe el archivo')

    return redirect(archivo)


@employee_files_bp.route('/listado/<int:id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda id: url_for('employees.search'))
def search(id):
    """Lista todos los archivos con paginación."""
    params = request.args

    activo = get_str_param(params, 'activo', default="informacion")

    filtros = {
        'titulo': get_str_param(params, 'titulo', optional=True),
        'tipo': get_str_param(params, 'tipo', 'TODOS', optional=True),
    }

    extension = get_str_param(params, 'extension', default="TODOS", optional=True)

    if extension == "TODOS":
        extension = None

    if filtros['tipo'] == "TODOS":
        del filtros['tipo']

    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 5, optional=True)
    order_by = get_str_param(params, 'order_by', 'created_at', optional=True)
    ascending = params.get('ascending', '1') == '1'
    deleted = False

    EmployeeFileSearchForm = FileSearchForm(TipoDoc)
    form = EmployeeFileSearchForm(**params.to_dict())

    if False:  # deberia chequear que sea admin?
        deleted = get_bool_param(params, 'deleted', False, optional=True)  # revisar

    else:
        del form.deleted

    docs, total, pages = EmployeeService.get_documents(
        employee_id=id,
        filtro=filtros,
        extension=extension,
        page=page,
        per_page=per_page,
        order_by=order_by,
        ascending=ascending,
        include_deleted=deleted,
        like=True
    )

    lista_diccionarios = []

    for doc in docs:
        lista_diccionarios.append({
            'id': doc.id,
            'Titulo': doc.titulo,
            'Tipo': doc.tipo.name.capitalize(),
            'Ubicación': 'Servidor externo' if doc.es_link else 'Servidor local',
            'Fecha de carga': doc.created_at,
            'es_link': doc.es_link
        })


    datos_empleado = EmployeeService.get_employee_by_id(id).to_dict()

    return render_template(
        'different_detail.html',
        diccionario=datos_empleado,
        activo=activo,
        entidad='employees',
        entidad_archivo='employee_files',
        anterior=url_for('employees.search', id=id),
        form=form,
        lista_diccionarios=lista_diccionarios,
        total=total,
        current_page=page,
        per_page=per_page,
        pages=pages,
        titulo=f'Información del Empleado: {datos_empleado['nombre']} {datos_empleado['apellido']}'
    )