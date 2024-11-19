from core.enums.equestrian_enum import SexoEnum, TipoEnum
from core.enums.permission_enums import PermissionCategory, PermissionModel
from core.services.equestrian_service import EquestrianService
from flask import Blueprint, redirect, request, render_template, url_for, flash
from web.forms.equestrian_form.file_search_equestrian import EquestrianFileSearchForm
from web.forms.equestrian_form.create_equestrian import EquestrianCreateForm
from web.forms.equestrian_form.new_equestrian_file import UploadFile, UploadLink
from web.forms.equestrian_form.search_equestrian import EquestriantSearchForm 
from web.handlers import handle_error
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
                'Fecha nacimiento': ecuestre.fecha_nacimiento,
                'Fecha ingreso': ecuestre.fecha_ingreso,
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
                           anterior=url_for('equestrian_files.search',
                                            id=id,
                                            activo='documents'
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
                           

@bp_file.get('/listado/<int:id>')
@check_permissions(f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.INDEX.value}") 
@handle_error(lambda: url_for('home'))
def search(id):
    """Lista todos los archivos con paginacion."""
    params = request.args
    params_dict = params.to_dict()
    
    form = EquestrianFileSearchForm()
    
    for param, valor in params_dict.items():
        if param in form._fields:
            form._fields[param].data = valor
    
    filtro = None
    extension = params.get('tipo_filtro', None)
    
    if extension and extension.upper() not in ['PDF', 'DOC', 'XLS', 'JPEG','LINK']:
        extension = None
    
    if params.get('tipo_filtro', None) and params.get('busqueda', '') != '':
        # 'PDF', 'DOC', 'XLS', 'JPEG','Link'
        if params.get('tipo_filtro').upper() in ['PDF', 'DOC', 'XLS', 'JPEG']:
            filtro = {
                'titulo': params.get('busqueda')
            }
        elif params.get('tipo_filtro') == 'Link':
            filtro = {
                'titulo': params.get('busqueda')
            }
        else:
            filtro = {
                params['tipo_filtro'].lower(): params.get('busqueda')
            }
    
    activo = params.get('activo', 'informacion')
    
    order_by = params.get('orden_filtro',None)
    
    if not order_by or order_by == 'fecha_de_carga':
        order_by = 'created_at'
    
    ascending = (params.get('orden','Ascendente') == 'Ascendente')
    
    page = int(params.get('page','1'))

    per_page = int(params.get('per_page','5'))
    
    archivos, total, pages = EquestrianService.get_documents(id,filtro,extension,page,per_page,order_by,ascending, like=True)
    
    listado = []

    if archivos:
        for archivo in archivos:
            dict_archivo = archivo.to_dict()
            dict_archivo['tipo'] =  TipoEnum(dict_archivo['tipo']).name.replace('_',' ').capitalize() 
            dict_archivo['ubicacion'] = 'Servidor Local' if dict_archivo['ubicacion'].startswith('client_files/') else 'Servidor Externo'
            dict_archivo['Fecha de carga'] = dict_archivo['created_at']
            del dict_archivo['created_at']
            listado.append(dict_archivo)
    else:
        # por si no hay que listar y que no se rompa
        listado = [{
        'id': '0',
        'Titulo':'',
        'es_link': True,
        'ubicacion': ''
    }]
    
    datos_equestrian = EquestrianService.get_equestrian_by_id(id).to_dict()

    return render_template('different_detail.html', 
                           diccionario=datos_equestrian,
                           activo=activo,
                           entidad='equestrians',
                           entidad_archivo='equestrian_files',
                           anterior=url_for('equestrians.detail',id=id),
                           form=form, 
                           lista_diccionarios=listado,
                           total=total,
                           current_page=page,
                           per_page=per_page,
                           pages=pages,
                           titulo='Detalle'
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
