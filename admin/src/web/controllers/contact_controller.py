from core.enums.message import StatuEnum
from core.enums.permission_enums import PermissionCategory, PermissionModel
from core.services.message_service import MessageService
from flask import Blueprint, flash, redirect, render_template, request, url_for
from web.forms.contact_form.contact_search_form import SearchContactForm
from web.forms.contact_form.contact_update_form import ContactUpdateForm
from web.handlers.auth import check_permissions
from src.web.handlers import get_int_param, get_str_param, handle_error

bp = Blueprint('contact',__name__,url_prefix='/contact')

@bp.route('/listado', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CONTACT.value}_{PermissionCategory.INDEX.value}") 
@handle_error(lambda: url_for('home'))
def search():
    params = request.args
    
    filtros = {
        'status': get_str_param(params, 'status', "TODOS",optional=True),
    }

    if filtros['status'] == 'TODOS':
        filtros = None
    else:
        filtros['status'] = StatuEnum[filtros['status']]

    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 5, optional=True)
    order_by = get_str_param(params, 'order_by', 'created_at', optional=True)
    ascending = params.get('ascending', '1') == '1'

    form= SearchContactForm(**params.to_dict())

    messages, total, pages = MessageService.get_messages(
        filtro=filtros,
        page=page,
        per_page=per_page,
        order_by=order_by,
        ascending=ascending,
        like=True
    )

    lista_diccionarios = []

    for msg in messages:
        lista_diccionarios.append({
            'id': msg.id,
            'Titulo':msg.title,
            'Estado': msg.status.name.capitalize(),
            'Fecha recepción': msg.created_at.strftime("%d-%m-%Y"),
            'Fecha cierre': msg.closed_at.strftime("%d-%m-%Y") if msg.closed_at else "Sin concluir"
        })

    return render_template(
        'search_box_msg.html',
        form=form,
        entidad='contact',
        anterior=url_for('home'),
        lista_diccionarios=lista_diccionarios,
        total=total,
        current_page=page,
        per_page =per_page,
        pages=pages,
        titulo='Listado de mensajes recibidos'
    )


@bp.route('/update/<int:id>', methods=['GET','POST'])
@check_permissions(f"{PermissionModel.CONTACT.value}_{PermissionCategory.UPDATE.value}") 
@handle_error(lambda id: url_for('contact.search'))
def update(id):
    """Editar un mensaje existente"""
    id= int(id)
    message = MessageService.get_message_by_id(id)
    if not message:
        flash("El mensaje seleccionado no existe", "danger")
        return redirect(url_for('contac.search'))
    form = ContactUpdateForm()
    
    if form.validate_on_submit():
            message_data =   {
                'status': form.status.data,
                'comentario': form.coment.data
                }
            MessageService.update_message(message.id, **message_data)
            flash(f"El mensaje  de {message.title} actualizado con éxito", "success")
            return redirect(url_for('contact.search'))
    form.status.data= message.status
    form.info.data=message.description
    form.coment.data=message.comentario
    
    context = {
        'form': form,
        'titulo': 'Editar un mensaje de consulta',
        'url_post': url_for('contact.update', id = id),
        'url_volver': url_for('contact.search')
    }
    return render_template('form.html', **context)

@bp.post('/delete/<int:id>')
@check_permissions(f"{PermissionModel.CONTACT.value}_{PermissionCategory.DESTROY.value}")
@handle_error(lambda id: url_for('contact.search'))
def delete(id):
    """Eliminar un mensaje de manera logica"""
    message = MessageService.get_message_by_id(id)
    if not message:
        flash("El mensaje seleccionado no existe", "danger")
        return redirect(url_for('contact.search'))

    MessageService.delete_menssage(id)
    flash("Se elimino el mensaje exitosamente", "success")
    return redirect(url_for('contact.search'))

@bp.route('/detail/<int:id>', methods=['GET'])
@check_permissions(f"{PermissionModel.CONTACT.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda id: url_for('contact.search')) 
def detail(id): 
      """Muestra los datos o detalles de un mensaje"""
      message= MessageService.get_message_by_id(id).to_dict()

      if not message['Fecha de cierre'] :
            message['Fecha de cierre']= "Sin concluir"
      else: message['Fecha de cierre']=message['Fecha de cierre'].strftime("%d-%m-%Y")
      
      return render_template( 'detail.html',titulo="Mensaje", entidad='contact', diccionario=message, anterior= url_for('contact.search') )
    