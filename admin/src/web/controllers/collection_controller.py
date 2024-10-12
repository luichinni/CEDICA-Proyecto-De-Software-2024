from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.collection_service import CollectionService
from src.core.services.employee_service import EmployeeService
from src.core.services.client_service import ClientService
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error, get_int_param, get_bool_param, get_str_param

bp = Blueprint('collection', __name__, url_prefix='/collection')

@bp.get('/')
@check_permissions("collection_index")
def list_collections():
    """Lista todos los cobros."""
    params = request.args
    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 25, optional=True)
    include_deleted = get_bool_param(params, 'include_deleted', False, optional=True)

    collections, total, pages = CollectionService.get_all_collections(
        page=page, 
        per_page=per_page, 
        include_deleted=include_deleted
    )
    return render_template('collections/list.html', collections=collections, total=total, pages=pages, current_page=page, per_page=per_page)

@bp.get('/search')
@check_permissions("collection_index")
@handle_error(lambda: url_for('collection.list_collections'))
def search_collections():
    """Busca cobros con filtros."""
    params = request.args

    start_date = get_str_param(params, 'start_date', optional=True)
    end_date = get_str_param(params, 'end_date', optional=True)
    payment_method = get_str_param(params, 'payment_method', optional=True)
    nombre = get_str_param(params, 'nombre', optional=True)
    apellido = get_str_param(params, 'apellido', optional=True)
    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 25, optional=True)
    order_by_date = get_bool_param(params, 'order_by_date', optional=True)
    ascending = get_bool_param(params, 'ascending', optional=True)
    include_deleted = get_bool_param(params, 'include_deleted', optional=True)

    collections, total, pages = CollectionService.search_collections(
        start_date=start_date,
        end_date=end_date,
        payment_method=payment_method,
        nombre=nombre,
        apellido=apellido,
        page=page,
        per_page=per_page,
        order_by_date=order_by_date,
        ascending=ascending,
        include_deleted=include_deleted
    )
    return render_template('collections/list.html', collections=collections, total=total, pages=pages, current_page=page, per_page=per_page)

@bp.get('/<int:collection_id>')
@check_permissions("collection_index")
@handle_error(lambda collection_id: url_for('collection.list_collections'))
def collection_detail(collection_id):
    """Obtiene un cobro por ID."""
    collection = CollectionService.get_collection_by_id(collection_id)
    return render_template('collections/detail.html', collection=collection)

@bp.get('/new')
@check_permissions("collection_new")
@handle_error(lambda: url_for('collection.list_collections'))
def new_collection():
    """Muestra el formulario para crear un nuevo cobro.""" 
    return render_template('collection/create.html')

@bp.post('/create')
@check_permissions("collection_new")
@handle_error(lambda: url_for('collection.new_collection'))
def create_collection():
    """Crea un nuevo cobro."""
    params = request.form

    employee_email = get_str_param(params, "employee_email", optional=False)
    employee_id = EmployeeService.get_employee_by_email(employee_email).id if employee_email else None
    
    client_dni = get_str_param(params, "dni", optional=False)
    client_id = ClientService.get_client_by_dni(client_dni).id if client_dni else None

    CollectionService.create_collection(
        employee_id=employee_id,
        client_id=client_id,
        payment_date=get_str_param(params, 'payment_date', optional=False),
        payment_method=get_str_param(params, 'payment_method', optional=False),
        amount=get_str_param(params, 'amount', optional=False),
        observations=get_str_param(params, 'observations', optional=True)
    )
    flash("Cobro creado exitosamente", "success")
    return redirect(url_for('collection.list_collections'))

@bp.get('/<int:collection_id>/edit')
@check_permissions("collection_update")
@handle_error(lambda collection_id: url_for('collection.list_collections'))
def edit_collection(collection_id):
    """Muestra el formulario para editar un cobro existente.""" 
    collection = CollectionService.get_collection_by_id(collection_id)
    return render_template('collection/edit.html', collection=collection)

@bp.post('/<int:collection_id>/update')
@check_permissions("collection_update")
@handle_error(lambda collection_id: url_for('collection.edit_collection', collection_id=collection_id))
def update_collection(collection_id):
    """Actualiza un cobro existente."""
    params = request.form
    CollectionService.update_collection(
        collection_id=collection_id,
        payment_date=get_str_param(params, 'payment_date', optional=True),
        payment_method=get_str_param(params, 'payment_method', optional=True),
        amount=get_str_param(params, 'amount', optional=True),
        observations=get_str_param(params, 'observations', optional=True)
    )
    flash("Cobro actualizado exitosamente", "success")
    return redirect(url_for('collection.collection_detail', collection_id=collection_id))

@bp.post('/<int:collection_id>/delete')
@check_permissions("collection_destroy")
@handle_error(lambda collection_id: url_for('collection.list_collections'))
def delete_collection(collection_id):
    """Elimina un cobro de forma lógica."""
    CollectionService.delete_collection(collection_id)
    flash("Cobro eliminado exitosamente", "success")
    return redirect(url_for('collection.list_collections'))
