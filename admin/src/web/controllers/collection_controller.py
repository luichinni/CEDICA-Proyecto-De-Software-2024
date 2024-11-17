from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.models.collection import PaymentMethod
from src.core.services.collection_service import CollectionService
from src.core.services.client_service import ClientService
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error, get_int_param, get_bool_param, get_str_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel
from src.web.forms.collection_forms.create_collection_form import CreateCollectionForm
from src.web.forms.collection_forms.update_collection_form import UpdateCollectionForm
from src.web.forms.collection_forms.search_collection_form import SearchCollectionForm
import re
from datetime import datetime

bp = Blueprint('collections', __name__, url_prefix='/collections')

@bp.get('/search')
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('home'))
def search():
    """Busca cobros con filtros."""
    params = request.args

    start_date_str = get_str_param(params, 'start_date', optional=True)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date_str = get_str_param(params, 'end_date', optional=True)
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    employee_name = get_str_param(params, 'employee_name', optional=True)
    employee_last_name = get_str_param(params, 'employee_last_name', optional=True)
    employee_email = get_str_param(params, 'employee_email', optional=True)
    client_dni = get_str_param(params, 'client_dni', optional=True)
    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 5, optional=True)
    order_by_date = get_bool_param(params, 'order_by_date', default=True, optional=True)
    ascending = get_bool_param(params, 'ascending', default=False, optional=True)
    include_deleted = get_bool_param(params, 'include_deleted', optional=True)

    payment_method_value = get_str_param(params, 'payment_method', optional=True)
    payment_method = PaymentMethod.from_value(payment_method_value) if payment_method_value else None

    collections, total, pages = CollectionService.search_collections(
        start_date=start_date,
        end_date=end_date,
        employee_email=employee_email,
        client_dni=client_dni,
        payment_method=payment_method,
        employee_name=employee_name,
        employee_last_name=employee_last_name,
        page=page,
        per_page=per_page,
        order_by_date=order_by_date,
        ascending=ascending,
        include_deleted=include_deleted
    )
    
    
    collections_list = [collection.to_dict() for collection in collections]
    
    params_dict = params.to_dict()
    # Manejar start_date y end_date para que no de error al pasar **params_dict
    if 'start_date' in params_dict:
        if not params_dict['start_date']: 
            del params_dict['start_date'] 
        else:
            params_dict['start_date'] = datetime.strptime(params_dict['start_date'], '%Y-%m-%d').date()

    if 'end_date' in params_dict:
        if not params_dict['end_date']:  
            del params_dict['end_date']  
        else:
            params_dict['end_date'] = datetime.strptime(params_dict['end_date'], '%Y-%m-%d').date()

    form = SearchCollectionForm(**params_dict)
    
    return render_template('search_box.html', entidad='collections', form=form, lista_diccionarios=collections_list, total=total, current_page=page, per_page=per_page, pages=pages)

@bp.get('/<int:id>')
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda id: url_for('collections.search'))
def detail(id):
    """Obtiene un cobro por ID."""
    collection = CollectionService.get_collection_by_id(id)
    return render_template('detail.html', diccionario=collection.to_dict(), entidad='collections')

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('collections.search'))
def new():
    """Muestra el formulario para crear un nuevo cobro.""" 
    form = CreateCollectionForm()

    if form.validate_on_submit():
        return create_collection()
        
    return render_template('form.html', form=form, url_volver=url_for('collections.search'))

def create_collection():
    """Crea un nuevo cobro."""
    params = request.form

    payment_method_value = get_str_param(params, 'payment_method', optional=False)
    payment_method = PaymentMethod.from_value(payment_method_value)

    id = CollectionService.create_collection(
        employee_id=get_int_param(params, "employee_id", optional=False),
        client_id=get_str_param(params, "client_id", optional=False),
        payment_date=get_str_param(params, 'payment_date', optional=False),
        payment_method=payment_method,
        amount=get_str_param(params, 'amount', optional=False),
        observations=get_str_param(params, 'observations', "Sin observaciones", optional=True)
    ).id
    flash("Cobro creado exitosamente", "success")
    return redirect(url_for('collections.detail',id=id))

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda id: url_for('collections.search'))
def update(id):
    """Muestra el formulario para editar un cobro existente.""" 
    collection = CollectionService.get_collection_by_id(id)

    form = UpdateCollectionForm(collection)

    if form.validate_on_submit():
        return update_collection(id)

    return render_template('form.html', form=form, url_volver=url_for('collections.detail',id=id), titulo=f"Editar cobro del empleado: {collection.employee.email}, sobre el J&A: {collection.client.dni}")

def update_collection(collection_id):
    """Actualiza un cobro existente."""
    params = request.form

    payment_method_value = get_str_param(params, 'payment_method', optional=True)
    payment_method = PaymentMethod.from_value(payment_method_value)
    
    CollectionService.update_collection(
        collection_id=collection_id,
        payment_date=get_str_param(params, 'payment_date', optional=True),
        payment_method=payment_method,
        amount=get_str_param(params, 'amount', optional=True),
        observations=get_str_param(params, 'observations', optional=True)
    )
    flash("Cobro actualizado exitosamente", "success")
    return redirect(url_for('collections.detail', id=collection_id))

@bp.post('/delete/<int:id>')
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda id: url_for('collections.search'))
def delete(id):
    """Elimina un cobro de forma lógica."""
    CollectionService.delete_collection(id)
    flash("Cobro eliminado exitosamente", "success")
    return redirect(url_for('collections.search'))
