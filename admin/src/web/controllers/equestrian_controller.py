from core.enums.equestrian_enum import SexoEnum, TipoEnum
from core.enums.permission_enums import PermissionCategory, PermissionModel
from core.services.employee_service import EmployeeService
from core.services.equestrian_service import AssociatesService, EquestrianService
from flask import Blueprint, redirect, request, render_template, url_for, flash
from web.forms.client_forms.client_file_search import FileSearchForm
from web.forms.equestrian_form.create_equestrian import AddEmployeeAssing, EquestrianCreateForm
from web.forms.equestrian_form.new_equestrian_file import UploadFile, UploadLink
from web.forms.equestrian_form.search_equestrian import EquestriantSearchForm 
from web.handlers import get_int_param, get_str_param, handle_error
from web.handlers.auth import check_permissions

bp = Blueprint('equestrians', __name__, url_prefix='/equestrians')

@bp.route('/create ', methods= ['GET','POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.NEW.value}") 
@handle_error(lambda: url_for('equestrians.search'))
def new():
    """Crear un empleado"""
    form = EquestrianCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_equestrian_data =   {
            'nombre': form.nombre.data,
            'sexo': form.sexo.data,
            'raza': form.raza.data,
            'compra': form.compra.data.capitalize() == 'True',
            'pelaje': form.pelaje.data, 
            'fecha_ingreso': form.fecha_ingreso.data,
            'fecha_nacimiento': form.fecha_nacimiento.data,
            'sede_asignada': form.sede_asignada.data,
            'tipo_de_jya_asignado': form.tipo_de_jya_asignado.data.upper(), 
        }
        EquestrianService.add_equestrian(**new_equestrian_data)
        flash("Se registro el ecuestre exitosamente", "success")
        

        return redirect(url_for('equestrians.search'))
    context = {
        'form': form,
        'titulo': 'Crear un ecuestre',
        'url_post': url_for('equestrians.new'),
        'url_volver': url_for('equestrians.search')
    }
    return render_template('form.html', **context)
 
@bp.route('/update/<int:id>', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.UPDATE.value}") 
@handle_error(lambda: url_for('equestrians.search'))
def update(id): 
    """Editar un ecuestre existente"""
    id= int(id)
    ecuestre = EquestrianService.get_equestrian_by_id(id)
    if not ecuestre:
        flash("El ecuestre seleccionado no existe", "danger")
        return redirect(url_for('equestrians.search'))
    form = EquestrianCreateForm(obj=ecuestre)
    
    if request.method == 'POST': 
       if form.validate_on_submit():
            ecuestre_data =   {
                'nombre': form.nombre.data,
                'sexo': form.sexo.data,
                'raza': form.raza.data,
                'compra': form.compra.data.capitalize() == 'True',
                'pelaje': form.pelaje.data, 
                'fecha_ingreso': form.fecha_ingreso.data,
                'fecha_nacimiento': form.fecha_nacimiento.data,
                'sede_asignada': form.sede_asignada.data,
                'tipo_de_jya_asignado': form.tipo_de_jya_asignado.data, 
            }
            EquestrianService.update_equestrian(ecuestre.id, **ecuestre_data)
            flash(f"El ecuestre {ecuestre.nombre} actualizado con éxito", "success")
            return redirect(url_for('equestrians.search'))
    form.sexo.data = ecuestre.sexo.name
    context = {
        'form': form,
        'titulo': 'Editar un ecuestre',
        'url_post': url_for('equestrians.update', id = id),
        'url_volver': url_for('equestrians.search')
    }
    return render_template('form.html', **context)
 

@bp.get('/listado')
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('home'))
def search():
    """Lista todos los ecuestres con paginación."""
    params = request.args
    params_dict = params.to_dict()
    
    form = EquestriantSearchForm()
    
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

    per_page = int(getattr(params,'per_page','5'))


    equestrians, total, pages = EquestrianService.search_equestrian(filtro,page,per_page,order_by,ascending, like=True)
    
    listado = []

    if equestrians:
         
        for ecuestre in equestrians:
            listado.append({
                'id': ecuestre.id,
                'Nombre': ecuestre.nombre,
                'Fecha nacimiento': ecuestre.fecha_nacimiento.strftime("%d-%m-%Y"),
                'Fecha ingreso': ecuestre.fecha_ingreso.strftime("%d-%m-%Y"),
            })
    else:
        # por si no hay que listar y que no se rompa
        listado = [{
        'id': '0',
        'Nombre': '',
        'Fecha nacimiento': '',
        'Fecha ingreso': '',
    }]
    
    return render_template('search_box.html', entidad='equestrians', anterior=url_for('home'), form=form, lista_diccionarios=listado, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado de ecuestres')



@bp.get('/detail/<int:id>')
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda: url_for('equestrians.search')) 
def detail(id):
      """Muestra los datos o detalles de un ecuestre"""
     
      return redirect(url_for('equestrian_files.search',id=id,activo='informacion'))
  

@bp.route('/delete/<int:id>', methods=['POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda: url_for('equestrians.search'))
def delete(id):
    """Eliminar un ecuestre de manera logica"""
    equestrian = EquestrianService.get_equestrian_by_id(id)
    if not equestrian:
        flash("El ecuestre seleccionado no existe", "danger")
        return redirect(url_for('equestrians.search'))

    EquestrianService.delete_equestrian(id)
    flash("Se elimino el ecuestre exitosamente", "success")
    return redirect(url_for('equestrians.search'))



bp_file = Blueprint('equestrian_files', __name__, url_prefix='/equestrian_files')

@bp_file.route('/create/<int:id>/<string:es_link>', methods= ['GET','POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.NEW.value}") 
@handle_error(lambda: url_for('equestrian_files.search'))
def new(id,es_link): 
    es_link = (es_link.lower() == 'true')
    form = UploadFile() if not es_link else UploadLink()
    if form.validate_on_submit():
        flash('Cargado exitosamente','success')
        EquestrianService.add_document(id,form.titulo.data,form.archivo.data,form.tipo.data,es_link)
        return redirect(url_for('equestrian_files.search',id=id, activo='documents'))
    
    return render_template('form.html',
                           url_volver=url_for('equestrian_files.search',
                                            id=id,
                                            activo='informacion'
                                        ),
                           ruta_post=url_for('equestrian_files.new',
                                             id=id,
                                             es_link=es_link
                                        ),
                           form=form)

@bp_file.route('/update/<int:id>/<string:es_link>/<int:id_entidad>', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.UPDATE.value}") 
@handle_error(lambda: url_for('equestrian_files.search'))
def  update(id:int, id_entidad: int,es_link:str):
    es_link = es_link=='True'
    
    archivo = EquestrianService.get_document_by_id(id).to_dict()
    if not es_link:
        archivo['titulo'] = ''.join(archivo['titulo'].split('_')[2:])
        
    
    archivo['archivo'] = archivo['ubicacion']
    
    form = None
    
    if request.method=='GET' and es_link and archivo['es_link']:
        form = UploadLink(data=archivo)
    
    elif request.method=='GET' and not es_link and not archivo['es_link']:
        form = UploadFile(data=archivo)
        del form.archivo
        
    elif request.method=='GET':
        raise ValueError('El documento no es válido')
    
    elif request.method == 'POST':
        if es_link:
            form = UploadLink()
        else:
            form = UploadFile()
            del form.archivo
        
        EquestrianService.update_document(id,form.titulo.data,form.tipo.data,form.archivo.data if es_link else '',es_link)
        
        return redirect(url_for('equestrian_files.search',id=id_entidad, activo='documents'))
    
    return render_template('form.html',
                           url_volver=url_for('equestrian_files.search',id=id_entidad, activo='documents'),
                           ruta_post=url_for('equestrian_files.update',
                                             id=id,
                                             id_entidad=id_entidad,
                                             es_link=es_link
                                        ),form=form)

def get_employees_associates (associates):
    empleados_asociados = []
    if associates is not None :  
        for associate in associates: 
             empleado = EmployeeService.get_employee_by_id(associate.employee_id)
             empleados_asociados.append(empleado)
    return empleados_asociados


@bp_file.get('/listado/<int:id>')
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.INDEX.value}") 
#@handle_error(lambda id: url_for('home'))
def search(id):
    #=======================================================================#
    # FILTRO DE LOS ARCHIVOS DEL ECUESTRE E INFORMACION FORMATEADA          #
    #=======================================================================#
    params = request.args

    activo = get_str_param(params, 'activo', default="informacion")

    filtros = {
        'titulo': get_str_param(params, 'titulo', optional=True),
        'tipo': get_str_param(params, 'tipo', 'TODOS',optional=True),
    }

    extension = get_str_param(params, 'extension', default="TODOS" ,optional=True)

    if extension == "TODOS":
        extension = None
    
    if filtros['tipo'] == "TODOS":
        del filtros['tipo']

    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 5, optional=True)
    order_by = get_str_param(params, 'order_by', 'created_at', optional=True)
    ascending = params.get('ascending', '1') == '1'
    deleted = False

    EquestrianFileSearchForm = FileSearchForm(TipoEnum)
    form = EquestrianFileSearchForm(**params.to_dict())

    if False: # deberia chequear que sea admin?
        deleted = get_bool_param(params, 'deleted', False, optional=True) # revisar

    else:
        del form.deleted

    docs, total, pages = EquestrianService.get_documents(
        equestrian_id=id,
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
            'Fecha de carga': doc.created_at
        })
    
    #=======================================================================#
    # DATOS DEL DETALLE DE ECUESTRE FORMATEADOS                             #
    #=======================================================================#
    
    datos_equestrian = EquestrianService.get_equestrian_by_id(id).to_dict()
    
    page2 = int(params.get('page2','1'))
    per_page2 = int(params.get('per_page2','8'))

    associates, total2, pages2 = AssociatesService.get_associate_of_an_equestrian(id,page2,per_page2) #obtengo todas las asociaciones
    cards_data = get_employees_associates(associates)
  
    return render_template(
        'detail_with_targets.html', 
        diccionario=datos_equestrian,
        activo=activo,
        entidad='equestrians',
        entidad_archivo='equestrian_files',
        anterior=url_for(
            'equestrians.detail',
            id=id
        ),
        form=form, 
        lista_diccionarios=lista_diccionarios,
        total=total,
        current_page=page,
        per_page=per_page,
        pages=pages,
        titulo='Detalle',
        cards=cards_data,
        total2=total2,
        current_page2=page2,
        per_page2=per_page2,
        pages2=pages2
    )
     


@bp_file.get('/detail/<int:id>')
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.SHOW.value}") 
@handle_error(lambda: url_for('equestrian_files.search'))
def detail(id):
    archivo = EquestrianService.get_document(id)
    
    if not archivo:
        raise ValueError('No existe el archivo')
    
    return redirect(archivo)


@bp_file.route('/delete/<int:id>/<int:id_entidad>', methods=['POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda: url_for('equestrian_files.search')) 
@handle_error(lambda: url_for('equestrian_files.search'))
def delete(id:int, id_entidad:int):
    EquestrianService.delete_document(id)
    flash("Se elimino el documento exitosamente", "success")
    return redirect(url_for('equestrian_files.search',id=id_entidad, activo='documents'))



bp_associates = Blueprint('associates', __name__, url_prefix='/associates')

@bp_associates.route('/create/<int:id>', methods= ['GET','POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.UPDATE.value}") 
@handle_error(lambda: url_for('equestrian_files.search'))
def new(id):  
    
    empleados,total, pages = EmployeeService.get_employees(filtro={"puesto_laboral": "CONDUCTOR"}, page=1, per_page=25)

    empleados2,total2, pages2 = EmployeeService.get_employees(filtro= {"puesto_laboral":"ENTRENADOR_DE_CABALLOS"}, page=1, per_page=25)
    empleados_asociados= empleados+ empleados2
    form = AddEmployeeAssing()    
    form.empleado.choices = [
    (empleado.id, f"Nombre: {empleado.nombre} {empleado.apellido}, Puesto Laboral: {empleado.puesto_laboral.name}")
      for empleado in empleados_asociados
    ]
    if form.validate_on_submit():
        try: 
            AssociatesService.add_associated(form.empleado.data, id) 
        except Exception: 
            flash('El empleado ya esta asociado con el ecuestre','success')
            return render_template('form.html',
                           url_volver=url_for('equestrian_files.search',
                                            id=id,
                                            activo='informacion'
                                        ),
                           ruta_post=url_for('associates.new',
                                             id=id,
                                        ),
                           form=form)
        else:
            flash('Cargado exitosamente','success') 
        return redirect(url_for('equestrian_files.search',id=id, activo='informacion'))
    
    return render_template('form.html',
                         url_volver=url_for('equestrian_files.search',
                                            id=id,
                                            activo='informacion'
                                        ),
                           ruta_post=url_for('associates.new',
                                             id=id,
                                        ),
                           form=form)


@bp_associates.route('/create/<int:id>/<int:id_empleado>', methods= ['GET','POST'])
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.UPDATE.value}") 
@handle_error(lambda: url_for('equestrian_files.search'))
def delete(id:int, id_empleado:int):
    AssociatesService.delete_associated(id,id_empleado)
    flash("Se elimino el empleado asociado exitosamente", "success")
    return redirect(url_for('equestrian_files.search',id=id, activo='informacion'))
