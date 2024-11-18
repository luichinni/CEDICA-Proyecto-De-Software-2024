from datetime import datetime

from flask import Blueprint, request, render_template, url_for, flash, redirect

from src.web.handlers import get_int_param
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
    order_by = get_str_param(params, 'order_by', optional=True)
    ascending = params.get('ascending', 'Ascendente') == 'Ascendente'

    publications, total, pages = PublicationService.list_publications(filtros, page, per_page, order_by, ascending)

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