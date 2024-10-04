from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.user_service import UserService

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.get('/')
def list_users():
    """Lista todos los usuarios con paginación."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    
    users, total, pages = UserService.get_all_users(page=page, per_page=per_page)
    
    return render_template('user/list.html', users=users, total=total, pages=pages, current_page=page, per_page=per_page)

@bp.get('/search')
def search_users():
    """Busca usuarios según criterios específicos con paginación."""
    email = request.args.get('email')
    activo = request.args.get('activo', type=lambda x: x.lower() == 'true')  # Convierte a booleano
    role_id = request.args.get('role_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    order_by = request.args.get('order_by', 'created_at')
    ascending = request.args.get('ascending', 'true', type=lambda x: x.lower() == 'true')

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
def user_detail(user_id):
    """Muestra los detalles de un usuario por su ID.""" 
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('user.list_users'))
    return render_template('user/detail.html', user=user)

@bp.get('/new')
def new_user():
    """Muestra el formulario para crear un nuevo usuario.""" 
    return render_template('user/create.html')

@bp.post('/create')
def create_user():
    """Crea un nuevo usuario con los datos proporcionados en el formulario.""" 
    params = request.form
    try:
        user = UserService.create_user(
            employee_id=params["employee_id"],
            alias=params["alias"],
            password=params["password"],
            role_id=params["role_id"],
            activo=params.get("activo", "on") == "on"
        )
        flash("Usuario creado exitosamente", "success")
        return redirect(url_for('user.user_detail', user_id=user.id))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('user.new_user'))

@bp.get('/<int:user_id>/edit')
def edit_user(user_id):
    """Muestra el formulario para editar un usuario existente.""" 
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('user.list_users'))
    return render_template('user/edit.html', user=user)

@bp.post('/<int:user_id>/update')
def update_user(user_id):
    """Actualiza la información de un usuario existente.""" 
    params = request.form
    try:
        UserService.update_user(
            user_id=user_id,
            alias=params.get("alias"),
            password=params.get("password"),
            activo=params.get("activo") == "on",
            role_id=params.get("role_id")
        )
        flash("Usuario actualizado exitosamente", "success")
        return redirect(url_for('user.user_detail', user_id=user_id))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('user.edit_user', user_id=user_id))

@bp.post('/<int:user_id>/delete')
def delete_user(user_id):
    """Elimina un usuario existente.""" 
    if UserService.delete_user(user_id):
        flash("Usuario eliminado exitosamente", "success")
    else:
        flash("Usuario no encontrado", "error")
    return redirect(url_for('user.list_users'))
