from datetime import datetime

from flask import Blueprint, request, render_template, url_for, flash, redirect

from src.web.handlers import get_int_param, get_bool_param
from src.core.services.publication_service import PublicationService
from web.forms.publication_forms.create_publication_form import CreatePublicationForm
from web.forms.publication_forms.search_publication_form import SearchPublicationForm
from web.handlers import get_str_param

bp = Blueprint('publications', __name__, url_prefix='/publications')

@bp.route('/')
def search():
    params = request.args
    start_published_date_str = get_str_param(params, 'start_published_date', optional=True)
    end_published_date_str = get_str_param(params, 'end_published_date', optional=True)

    filtros = {'title': get_str_param(params, 'titulo', optional=True),
               'start_published_date': datetime.strptime(start_published_date_str, '%Y-%m-%d').date() if start_published_date_str else None,
               'end_published_date': datetime.strptime(end_published_date_str, '%Y-%m-%d').date() if end_published_date_str else None}

    page = get_int_param(params, 'page', 1, True)
    per_page = get_int_param(params, 'per_page', 10, True)
    order_by = get_str_param(params, 'order_by', 'title',optional=True)
    ascending = get_bool_param(params, 'ascending', True, optional= True)

    publications, total, pages = PublicationService.list_publications(
        filtro=filtros,
        page=page,
        per_page=per_page,
        order_by=order_by,
        ascending=ascending)

    lista_diccionarios = [publication.to_dict() for publication in publications]

    form = SearchPublicationForm(**params.to_dict())
    return render_template('search_box.html',
                           form=form,
                           entidad='publications',
                           anterior=url_for('home'),
                           lista_diccionarios=lista_diccionarios,
                           total=total,
                           pages=pages,
                           per_page=per_page,
                           current_page=page,
                           titulo='Listado de publicaciones')

@bp.route('/create', methods=('GET', 'POST'))
def new():
    form = CreatePublicationForm()

    if form.validate_on_submit():
        data = PublicationService.form_to_dict(form)
        PublicationService.create_publication(data)
        flash('Publicacion creada exitosamente', 'success')
        return redirect(url_for('publications.search'))

    context = {
               'form': form,
               'titulo': 'Crear una publicacion',
               'url_post': url_for('publications.new'),
               'url_volver': url_for('home')
    }
    return render_template('form.html', **context)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def update(id):
    """Editar una publicacion existente"""
    publication = PublicationService.get_publication_by_id(id)
    if not publication:
        flash("La publicacion seleccionada no existe", "danger")
        return redirect(url_for('publications.search'))
    form = CreatePublicationForm(obj=publication)
    if form.validate_on_submit():
        publication_data = PublicationService.form_to_dict(form)
        PublicationService.update_publication(publication.id, publication_data)
        flash(f"Publicacion {publication.title} actualizada con éxito", "success")
        return redirect(url_for('publications.search'))
    context = {
        'form': form,
        'titulo': 'Editar una publicacion',
        'url_post': url_for('publications.update', id=id),
        'url_volver': url_for('publications.search')
    }
    return render_template('form.html', **context)

@bp.route('<int:id>', methods=['GET'])
def detail(id):
    publication = PublicationService.get_publication_by_id(id)
    if not publication:
        flash(f'Publicacion "{publication.title}" no encontrada', 'warning')
        return redirect(url_for('publications.search'))

    titulo = f'Detalle de la publicacion "{publication.title}"'
    anterior = url_for('publications.search')
    diccionario = publication.to_dict()
    entidad = 'publications'

    return render_template('detail.html', titulo=titulo, anterior=anterior, diccionario= diccionario, entidad=entidad )

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Eliminar una publicacion de manera logica"""
    publication_to_delete = PublicationService.get_publication_by_id(id)
    if not publication_to_delete:
        flash("La publicacion seleccionada no existe", "danger")
    else:
        PublicationService.delete_publication(id)
        flash("Se elimino la publicacion exitosamente", "success")
    return redirect(url_for('publications.search'))