from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.user_service import UserService
from src.core.services.role_service import RoleService
from src.core.services.employee_service import EmployeeService
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error
from src.web.handlers import get_int_param, get_str_param, get_bool_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel
from src.web.forms.user_forms.create_user_form import CreateUserForm
from src.web.forms.user_forms.update_user_form import UpdateUserForm
#from src.web.forms.user_forms.search_user_form import SearchUserForm
from web.forms.search_form import SearchForm

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.get('/search')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('home'))
def search():
    """Busca usuarios según criterios específicos con paginación."""
    params = request.args
    
    # TODO: Luego reemplazar esta seccion
    key = params.get('tipo_filtro', None)
    value = params.get('busqueda', '') if params.get('busqueda', '') and params.get('busqueda', '') != '' else None
    
    email = value if key == 'email' else None
    activo = not bool(value) if key == 'activo' else None 
    role_id = int(value) if key == 'role_id' and value and value.isdigit() else None 
    
    page = int(value) if key == 'page' and value and value.isdigit() else 1 
    per_page = int(value) if key == 'per_page' and value and value.isdigit() else 25 
    
    order_by = value if key == 'orden_filtro' else 'created_at'
    ascending = params.get('orden','Ascendente') == 'Ascendente'

    ''' Y cambiarlo por esto:
    email = get_str_param(params, 'email', optional= True)
    activo = get_bool_param(params, 'activo', optional= True) 
    role_id = get_int_param(params, 'role_id', optional= True) 
    page = get_int_param(params, 'page', 1, optional= True) 
    per_page = get_int_param(params, 'per_page', 25, optional= True) 
    order_by = get_str_param(params, 'order_by', 'created_at', optional= True)
    ascending = get_bool_param(params, 'ascending', True, optional= True)
    '''

    users, total, pages = UserService.search_users(
        email=email,
        activo=activo,
        role_id=role_id,
        page=page,
        per_page=per_page,
        order_by=order_by,
        ascending=ascending
    )

    users_list = [user.to_dict() for user in users] if users else [{
        'id': '0',
        'email': '',
        'alias': '',
        'activo': False,
        'role': '',
        'created_at': '',
        'updated_at': ''
    }]
    
    
    form = SearchForm()

    busqueda = ['email', 'activo', 'role_id']
    orden = ['created_at', 'email']
    form.tipo_filtro.choices = [(campo, campo.replace('_',' ').capitalize()) for campo in busqueda]
    form.orden_filtro.choices = [(campo, campo.replace('_', ' ').capitalize()) for campo in orden]
    
    for param, valor in params.to_dict().items():
        if param in form._fields:
            form._fields[param].data = valor

    return render_template('search_box.html', entidad='users', anterior=url_for('home'), form=form, lista_diccionarios=users_list, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado de ususarios')

@bp.get('/<int:id>')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda id: url_for('users.search'))
def detail(id):
    """Muestra los detalles de un usuario por su ID.""" 
    
    user = UserService.get_user_by_id(id, include_blocked=True)
    return render_template('detail.html', titulo='Detalle de usuario', anterior = url_for('users.search'), diccionario=user.to_dict(), entidad='users')

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('users.search'))
def new():
    """Muestra el formulario para crear un nuevo usuario y crea el usuario con los datos proporcionados en el formulario."""
    employee_choices = [(e.id, e.email) for e in EmployeeService.get_employees_without_user()]
    if not employee_choices:
        raise ValueError("No hay empleados sin usuario disponibles.")
    
    role_choices = [(r.id, r.name) for r in RoleService.get_all_roles()]
    if not role_choices:
        raise ValueError("No hay roles disponibles.")

    form = CreateUserForm()
    form.employee_id.choices = employee_choices
    form.role_id.choices = role_choices

    if form.validate_on_submit():
        return create_user()
           
    return render_template('form.html', form=form)

def create_user():
    """Crea un nuevo usuario con los datos proporcionados en el formulario.""" 
    params = request.form

    user = UserService.create_user(
        employee_id=get_int_param(params, "employee_id", optional=False),
        alias=get_str_param(params, "alias", optional=False),
        password=get_str_param(params, "password", optional=False),
        activo=get_bool_param(params, "activo", False, optional=True),
        role_id=get_int_param(params, "role_id", optional=False)
    )
    flash("Usuario creado exitosamente", "success")
    return redirect(url_for('users.detail', id=user.id))

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda id: url_for('users.search'))
def update(id):
    """Muestra el formulario para editar un usuario existente y actualiza la información.""" 
    user = UserService.get_user_by_id(id, include_blocked=True)

    role_choices = [(r.id, r.name) for r in RoleService.get_all_roles()]
    if not role_choices:
        raise ValueError("No hay roles disponibles.")

    form = UpdateUserForm()
    form.populate_obj(user)
    form.role_id.choices = role_choices

    if form.validate_on_submit():
        return update_user(id)

    return render_template('form.html', form=form)

def update_user(id):
    """Actualiza la información de un usuario existente.""" 
    params = request.form

    UserService.update_user(
        user_id=id,
        alias=get_str_param(params, "alias", optional=True),
        password=get_str_param(params, "password", optional=True),
        activo=get_bool_param(params, "activo", False, optional=True),
        role_id=get_int_param(params, "role_id", optional=True)
    )
    flash("Usuario actualizado exitosamente", "success")
    return redirect(url_for('users.detail', id=id))

@bp.post('/delete/<int:id>')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda id: url_for('users.search'))
def delete(id):
    """Elimina un usuario existente.""" 
    UserService.delete_user(id)
    flash("Usuario eliminado exitosamente", "success")
    return redirect(url_for('users.search'))


@bp.post('/block/<int:user_id>')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.BLOCK.value}")
@handle_error(lambda user_id: url_for('users.search'))
def block(user_id):
    """Bloquea un usuario existente.""" 
    UserService.block_user(user_id)
    flash("Usuario bloqueado exitosamente", "success")
    return redirect(url_for('users.search'))
