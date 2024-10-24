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
from src.web.forms.user_forms.search_user_form import SearchUserForm

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.get('/search')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('user.list_users'))
def search():
    """Busca usuarios según criterios específicos con paginación."""
    params = request.args
    
    email = get_str_param(params, 'email', optional= True)
    activo = get_bool_param(params, 'activo', optional= True) 
    role_id = get_int_param(params, 'role_id', optional= True) 
    page = get_int_param(params, 'page', 1, optional= True) 
    per_page = get_int_param(params, 'per_page', 25, optional= True) 
    order_by = get_str_param(params, 'order_by', 'created_at', optional= True)
    ascending = get_bool_param(params, 'ascending', True, optional= True)

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
    
    form = SearchUserForm()
    
    for param, valor in params.to_dict().items():
        if param in form._fields:
            form._fields[param].data = valor

    return render_template('search_box.html', entidad='users', anterior=url_for('home'), form=form, lista_diccionarios=users_list, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado de ususarios')

@bp.get('/<int:user_id>')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def detail(user_id):
    """Muestra los detalles de un usuario por su ID.""" 
    
    user = UserService.get_user_by_id(user_id)
    return render_template('detail.html', titulo='Detalle de usuario', anterior = url_for('user.list_users'), diccionario=user.to_dict(), entidad='users')

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('user.list_users'))
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
    return redirect(url_for('user.user_detail', user_id=user.id))

@bp.route('/<int:user_id>/update', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def edit(user_id):
    """Muestra el formulario para editar un usuario existente y actualiza la información.""" 
    user = UserService.get_user_by_id(user_id)

    role_choices = [(r.id, r.name) for r in RoleService.get_all_roles()]
    if not role_choices:
        raise ValueError("No hay roles disponibles.")

    form = UpdateUserForm()
    form.populate_obj(user)
    form.role_id.choices = role_choices

    if form.validate_on_submit():
        return update_user(user_id)

    return render_template('form.html', form=form)

def update_user(user_id):
    """Actualiza la información de un usuario existente.""" 
    params = request.form

    UserService.update_user(
        user_id=user_id,
        alias=get_str_param(params, "alias", optional=True),
        password=get_str_param(params, "password", optional=True),
        activo=get_bool_param(params, "activo", False, optional=True),
        role_id=get_int_param(params, "role_id", optional=True)
    )
    flash("Usuario actualizado exitosamente", "success")
    return redirect(url_for('user.user_detail', user_id=user_id))

@bp.post('/<int:user_id>/delete')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def delete(user_id):
    """Elimina un usuario existente.""" 
    UserService.delete_user(user_id)
    flash("Usuario eliminado exitosamente", "success")
    return redirect(url_for('user.list_users'))


@bp.post('/<int:user_id>/block')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.BLOCK.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def block(user_id):
    """Bloquea un usuario existente.""" 
    UserService.block_user(user_id)
    flash("Usuario bloqueado exitosamente", "success")
    return redirect(url_for('user.list_users'))
