from core.services.equestrian_service import EquestrianService
from flask import Blueprint, redirect, request, render_template, url_for, flash
from web.forms.equestrian_form.search_equestrian import EquestriantSearchForm

bp = Blueprint('equestrians', __name__, url_prefix='/equestrians')

@bp.route('/create ', methods= ['GET','POST'])
def new():

     pass
@bp.get('/update/<int:id>')
def update():
     pass

@bp.get('/listado')
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

    per_page = int(getattr(params,'per_page','25'))


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
    
    return render_template('search_box.html', entidad='equestrian', anterior=url_for('home'), form=form, lista_diccionarios=listado, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado de ecuestres')



@bp.get('/detail/<int:id>')
def detail(equestrian_id):
      """Muestra los datos o detalles de un ecuestre"""
      equestrian= EquestrianService.get_equestrian_by_id(equestrian_id)
      titulo = 'detalle de: '+ equestrian.nombre
      equestrian_dict=equestrian.to_dict()

      return render_template('different_detail.html', diccionario=equestrian_dict, titulo= titulo)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(equestrian_id):
    """Eliminar un ecuestre de manera logica"""
    equestrian = EquestrianService.get_equestrian_by_id(equestrian_id)
    if not equestrian:
        flash("El ecuestre seleccionado no existe", "danger")
        return redirect(url_for('equestrian.search_equestrian'))

    EquestrianService.delete_equestrian(equestrian_id)
    flash("Se elimino el ecuestre exitosamente", "success")
    return redirect(url_for('equestrian.search_equestrian'))



bp_file = Blueprint('equestrian_files', __name__, url_prefix='/equestrian_files')




@bp_file.route('/create ', methods= ['GET','POST'])
def new():

     pass
@bp_file.get('/update/<int:id>')
def update(id):
     pass

@bp_file.get('/listado')
def search():
    pass


@bp_file.get('/detail/<int:id>')
def detail(equestrian_id):
      pass

@bp_file.route('/delete/<int:id>', methods=['POST'])
def delete(equestrian_id):
    pass