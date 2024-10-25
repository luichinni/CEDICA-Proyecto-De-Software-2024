from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.models.collection import PaymentMethod
from src.core.services.collection_service import CollectionService
from src.core.services.employee_service import EmployeeService
from src.core.services.client_service import ClientService
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error, get_int_param, get_bool_param, get_str_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel
from src.web.forms.collection_forms.search_collection_form import SearchCollectionForm

from src.web.forms.collection_forms.create_collection_form import CreateCollectionForm
from src.web.forms.collection_forms.update_collection_form import UpdateCollectionForm

bp = Blueprint('collections', __name__, url_prefix='/collections')

@bp.get('/search')
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('home'))
def search():
    """Busca cobros con filtros."""
    params = request.args

    start_date = get_str_param(params, 'start_date', optional=True)
    end_date = get_str_param(params, 'end_date', optional=True)
    payment_method = get_str_param(params, 'payment_method', optional=True)
    nombre = get_str_param(params, 'nombre', optional=True)
    apellido = get_str_param(params, 'apellido', optional=True)
    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 25, optional=True)
    order_by_date = get_bool_param(params, 'order_by_date', default=True, optional=True)
    ascending = get_bool_param(params, 'ascending', default=False, optional=True)
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
    
    
    collections_list = [collection.to_dict() for collection in collections] if collections else [{
        'id': '0',
        "employee_id": '',
        "client_id": '',
        "payment_date": '',
        "payment_method": '',
        "amount": '',
        "remarks": '',
        "created_at": '',
        "updated_at": ''
    }]
    
    form = SearchCollectionForm()
    
    for param, valor in params.to_dict().items():
        if param in form._fields:
            form._fields[param].data = valor

    return render_template('search_box.html', entidad='collections', anterior=url_for('home'), form=form, lista_diccionarios=collections_list, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado de cobros')

@bp.get('/<int:collection_id>')
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda collection_id: url_for('collections.search'))
def detail(collection_id):
    """Obtiene un cobro por ID."""
    collection = CollectionService.get_collection_by_id(collection_id)
    return render_template('detail.html', titulo='Detalle de cobro', anterior = url_for('collections.search'), diccionario=collection.to_dict(), entidad='collections')

@bp.route('/create', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.NEW.value}")
@handle_error(lambda: url_for('collections.search'))
def new():
    """Muestra el formulario para crear un nuevo cobro.""" 
    employee_choices = [(e.id, e.email) for e in EmployeeService.get_all_employees()]
    if not employee_choices:
        raise ValueError("No hay empleados registrados.")
    
    client_choices = [(e.id, e.dni) for e in ClientService.get_clients()]
    if not employee_choices:
        raise ValueError("No hay clientes registrados.")
    

    form = CreateCollectionForm()
    form.employee_id.choices = employee_choices
    form.client_id.choices = client_choices

    if form.validate_on_submit():
        return create_collection()
        
    return render_template('form.html', form=form)

def create_collection():
    """Crea un nuevo cobro."""
    params = request.form

    employee_id = get_int_param(params, "employee_id", optional=False)
    
    client_id = get_int_param(params, "client_id", optional=False)
    
    payment_method_value = get_str_param(params, 'payment_method', optional=False)
    payment_method = PaymentMethod.from_value(payment_method_value)

    CollectionService.create_collection(
        employee_id=employee_id,
        client_id=client_id,
        payment_date=get_str_param(params, 'payment_date', optional=False),
        payment_method=payment_method,
        amount=get_str_param(params, 'amount', optional=False),
        observations=get_str_param(params, 'observations', "Sin observaciones", optional=True)
    )
    flash("Cobro creado exitosamente", "success")
    return redirect(url_for('collections.search'))

@bp.route('/<int:collection_id>/update', methods=['GET', 'POST'])
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.UPDATE.value}")
@handle_error(lambda collection_id: url_for('collections.search'))
def edit(collection_id):
    """Muestra el formulario para editar un cobro existente.""" 
    collection = CollectionService.get_collection_by_id(collection_id)

    form = UpdateCollectionForm()
    form.populate_obj(collection)

    if form.validate_on_submit():
        return update_collection(collection_id)

    return render_template('form.html', form=form)

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
    return redirect(url_for('collections.detail', collection_id=collection_id))

@bp.post('/<int:collection_id>/delete')
@check_permissions(f"{PermissionModel.COLLECTION.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda collection_id: url_for('collections.search'))
def delete(collection_id):
    """Elimina un cobro de forma lógica."""
    CollectionService.delete_collection(collection_id)
    flash("Cobro eliminado exitosamente", "success")
    return redirect(url_for('collections.search'))
