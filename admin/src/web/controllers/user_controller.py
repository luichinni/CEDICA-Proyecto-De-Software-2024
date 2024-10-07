from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.user_service import UserService
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error
from src.web.handlers import get_int_param, get_str_param, get_bool_param

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.get('/')
@check_permissions("user_index")
@handle_error(lambda: url_for('user.list_users'))
def list_users():
    """Lista todos los usuarios con paginación."""
    params = request.args
    page = get_int_param(params, 'page', 1, optional= True)
    per_page = get_int_param(params, 'per_page', 25, optional= True)
    
    users, total, pages = UserService.get_all_users(page=page, per_page=per_page)
    
    return render_template('user/list.html', users=users, total=total, pages=pages, current_page=page, per_page=per_page)

@bp.get('/search')
@check_permissions("user_index")
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
@check_permissions("user_show")
@handle_error(lambda user_id: url_for('user.list_users'))
def user_detail(user_id):
    """Muestra los detalles de un usuario por su ID.""" 
    
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('user.list_users'))
    return render_template('user/detail.html', user=user)

@bp.get('/new')
@check_permissions("user_new")
@handle_error(lambda: url_for('user.list_users'))
def new_user():
    """Muestra el formulario para crear un nuevo usuario.""" 
    return render_template('user/create.html')

@bp.post('/create')
@check_permissions("user_new")
@handle_error(lambda: url_for('user.new_user'))
def create_user():
    """Crea un nuevo usuario con los datos proporcionados en el formulario.""" 
    params = request.form
    user = UserService.create_user(
        employee_id=get_int_param(params, "employee_id"),
        alias=get_str_param(params, "alias"),
        password=get_str_param(params, "password"),
        role_id=get_int_param(params, "role_id"),
        activo=get_bool_param(params, "activo")
    )
    flash("Usuario creado exitosamente", "success")
    return redirect(url_for('user.user_detail', user_id=user.id))

@bp.get('/<int:user_id>/edit')
@check_permissions("user_update")
@handle_error(lambda user_id: url_for('user.list_users'))
def edit_user(user_id):
    """Muestra el formulario para editar un usuario existente.""" 
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('user.list_users'))
    return render_template('user/edit.html', user=user)

@bp.post('/<int:user_id>/update')
@check_permissions("user_update")
@handle_error(lambda user_id: url_for('user.edit_user', user_id=user_id))
def update_user(user_id):
    """Actualiza la información de un usuario existente.""" 
    params = request.form
    UserService.update_user(
        user_id=user_id,
        alias=get_str_param(params, "alias", optional= True),
        password=get_str_param(params, "password", optional= True),
        activo=get_bool_param(params, "activo", optional= True),
        role_id=get_int_param(params, "role_id", optional= True)
    )
    flash("Usuario actualizado exitosamente", "success")
    return redirect(url_for('user.user_detail', user_id=user_id))

@bp.post('/<int:user_id>/delete')
@check_permissions("user_destroy")
@handle_error(lambda user_id: url_for('user.list_users'))
def delete_user(user_id):
    """Elimina un usuario existente.""" 
    if UserService.delete_user(user_id):
        flash("Usuario eliminado exitosamente", "success")
    else:
        flash("Usuario no encontrado", "error")
    return redirect(url_for('user.list_users'))


@bp.post('/<int:user_id>/block')
@check_permissions("user_block")
@handle_error(lambda user_id: url_for('user.list_users'))
def block_user(user_id):
    """Elimina un usuario existente.""" 
    if UserService.block_user(user_id):
        flash("Usuario bloqueado exitosamente", "success")
    else:
        flash("Usuario no encontrado", "error")
    return redirect(url_for('user.list_users'))
