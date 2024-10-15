from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.user_service import UserService
from src.core.services.role_service import RoleService
from src.core.services import employee_service
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error
from src.web.handlers import get_int_param, get_str_param, get_bool_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.get('/')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.INDEX.value}")
def list_users():
    """Lista todos los usuarios con paginación."""
    params = request.args
    page = get_int_param(params, 'page', 1, optional= True)
    per_page = get_int_param(params, 'per_page', 25, optional= True)
    
    users, total, pages = UserService.get_all_users(page=page, per_page=per_page)
    
    return render_template('user/list.html', users=users, total=total, pages=pages, current_page=page, per_page=per_page)

@bp.get('/search')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('user.list_users'))
def search_users():
    """Busca usuarios según criterios específicos con paginación."""
    params = request.args
    
    email = get_str_param(params, 'email', optional= True)
    activo = get_bool_param(params, 'activo', optional= True) 
    role_id = get_int_param(params, 'role_id', optional= True) 
    page = get_int_param(params, 'page', 1, optional= True) 
    per_page = get_int_param(params, 'per_page', 25, optional= True) 
    order_by = get_int_param(params, 'order_by', 'created_at', optional= True)
    ascending = get_int_param(params, 'ascending', True, optional= True)

    users, total, pages = UserService.search_users(
        email=email,
        activo=activo,
        role_id=role_id,
        page=page,
        per_page=per_page,
        order_by=order_by,
        ascending=ascending
    )

    return render_template('user/list.html', users=users, total=total, pages=pages, current_page=page, per_page=per_page)

@bp.get('/<int:user_id>')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def user_detail(user_id):
    """Muestra los detalles de un usuario por su ID.""" 
    
    user = UserService.get_user_by_id(user_id)
    return render_template('user/detail.html', user=user)

def get_user_data(params, optional=False):
    """Obtiene la información de un usuario existente.""" 

    role_id = get_int_param(params, "role_id", optional=optional)
    
    employee_email = get_str_param(params, "employee_email", optional=optional)
    employee_id = employee_service.get_employee_by_email(employee_email).id if employee_email else None
    
    alias = get_str_param(params, "alias", optional=optional)
    password=get_str_param(params, "password", optional=optional)
    activo=get_bool_param(params, "activo", optional=optional)
    return ( employee_id, alias, password, activo, role_id )

@bp.get('/new')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('user.list_users'))
def new_user():
    """Muestra el formulario para crear un nuevo usuario.""" 
    roles = RoleService.get_all_roles()
    return render_template('user/create.html', roles=roles)

@bp.post('/create')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('user.new_user'))
def create_user():
    """Crea un nuevo usuario con los datos proporcionados en el formulario.""" 
    params = request.form
    employee_id, alias, password, activo, role_id = get_user_data(params, optional=False)

    user = UserService.create_user(
        employee_id=employee_id,
        alias=alias,
        password=password,
        activo=activo,
        role_id=role_id
    )
    flash("Usuario creado exitosamente", "success")
    return redirect(url_for('user.user_detail', user_id=user.id))

@bp.get('/<int:user_id>/edit')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def edit_user(user_id):
    """Muestra el formulario para editar un usuario existente.""" 
    user = UserService.get_user_by_id(user_id)
    roles = RoleService.get_all_roles()
    return render_template('user/edit.html', user=user, roles=roles)

@bp.post('/<int:user_id>/update')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda user_id: url_for('user.edit_user', user_id=user_id))
def update_user(user_id):
    """Actualiza la información de un usuario existente.""" 
    params = request.form

    _, alias, password, activo, role_id = get_user_data(params, optional=True)

    UserService.update_user(
        user_id=user_id,
        alias=alias,
        password=password,
        activo=activo,
        role_id=role_id
    )
    flash("Usuario actualizado exitosamente", "success")
    return redirect(url_for('user.user_detail', user_id=user_id))

@bp.post('/<int:user_id>/delete')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def delete_user(user_id):
    """Elimina un usuario existente.""" 
    UserService.delete_user(user_id)
    flash("Usuario eliminado exitosamente", "success")
    return redirect(url_for('user.list_users'))


@bp.post('/<int:user_id>/block')
@check_permissions(f"{PermissionModel.USER.value}_{PermissionCategory.BLOCK.value}")
@handle_error(lambda user_id: url_for('user.list_users'))
def block_user(user_id):
    """Bloquea un usuario existente.""" 
    UserService.block_user(user_id)
    flash("Usuario bloqueado exitosamente", "success")
    return redirect(url_for('user.list_users'))
