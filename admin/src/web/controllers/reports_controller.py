from flask import Blueprint, request, render_template, url_for
from web.forms.search_form import SearchForm
from src.web.handlers import handle_error, get_int_param, get_bool_param, get_str_param

from src.core.services.reports_service import ReportService

bp = Blueprint('reports',__name__,url_prefix='/reports')


@bp.get('/')
@handle_error(lambda: url_for('home'))
def reports():
    return render_template('reports/reports.html')

@bp.get('/charts')
@handle_error(lambda: url_for('home'))
def get_graficos():
    jobs_ranking = ReportService.get_propuestas_ranking()
    becados_count = ReportService.get_becados_count()
    year_income_counts = ReportService.get_income_by_year()
    cert_discapacidad_count = ReportService.get_cert_discapacidad_count()
    discapacidad_count = ReportService.get_discapacidad_count()

    return render_template('reports/charts.html',charts_data=[{"chart_data":jobs_ranking,"chart_type":"pie","chart_name":"Ranking de propuestas de trabajo"},
                                                              {"chart_data":becados_count,"chart_type":"bar","chart_name":"Conteo de becados y no becados"},
                                                              {"chart_data":year_income_counts,"chart_type":"bar","chart_name":"Cantidad de ingresos por año","order_by":"key","sort_order":"ascending"},
                                                              {"chart_data":cert_discapacidad_count,"chart_type":"pie","chart_name":"Cantidad de J&A que tienen certificado de discapacidad"},
                                                              {"chart_data":discapacidad_count,"chart_type":"bar","chart_name":"Contabilidad de tipos de discapacidad"},
                                                              #{"chart_data":{"Manzanas": 10, "Naranjas": 15, "Peras": 20},"chart_type":"pie","chart_name":"Frutas vendidas"},
                                                              #{"chart_data":{"Manzanas": 10, "Naranjas": 15, "Peras": 20},"chart_type":"bar","chart_name":"Frutas vendidas v2"},
                                                              
                                                              ])


@bp.get('/debtors')
@handle_error(lambda: url_for('home'))
def search():
    """Busca usuarios según criterios específicos con paginación."""
    params = request.args
    
    # TODO: Luego reemplazar esta seccion
    key = params.get('tipo_filtro', None)
    value = params.get('busqueda', '') if params.get('busqueda', '') and params.get('busqueda', '') != '' else None
    
    page = int(value) if key == 'page' and value and value.isdigit() else 1 
    per_page = int(value) if key == 'per_page' and value and value.isdigit() else 25 
    # Hasta aca reemplazar

    adeudores, total, pages = ReportService.get_adeudores(page=1, per_page=25)
        
    adeudores_list = [{
                'id': e.id,
                'Nombre': e.nombre,
                'Apellido': e.apellido,
                'DNI': e.dni,
                'Atendido por': e.atendido_por
            } for e in adeudores] if adeudores else [{
        'id': '0',
        'Nombre': '',
        'Apellido': '',
        'DNI': '',
        'Atendido por': ''
    }]
    
    form = SearchForm()

    busqueda = []
    orden = []
    form.tipo_filtro.choices = [(campo, campo.replace('_',' ').capitalize()) for campo in busqueda]
    form.orden_filtro.choices = [(campo, campo.replace('_', ' ').capitalize()) for campo in orden]
    
    for param, valor in params.to_dict().items():
        if param in form._fields:
            form._fields[param].data = valor

    return render_template('reports/reports_search_box.html', entidad='reports', anterior=url_for('reports.reports'), form=form, lista_diccionarios=adeudores_list, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado de reportes')


@bp.get('/historical_payments')
@handle_error(lambda: url_for('home'))
def historical_payments():
    """Busca usuarios según criterios específicos con paginación."""
    params = request.args
    
    start_date = get_str_param(params, 'start_date', optional=True)
    end_date = get_str_param(params, 'end_date', optional=True)
    nombre = get_str_param(params, 'nombre', optional=True)
    apellido = get_str_param(params, 'apellido', optional=True)
    page = get_int_param(params, 'page', 1, optional=True)
    per_page = get_int_param(params, 'per_page', 25, optional=True)

    historical_payments, total, pages = ReportService.get_historical_payments_report(start_date = start_date, end_date = end_date, nombre = nombre, apellido = apellido, page = page, per_page = per_page)
        
    historical_payments_list = [collection.to_dict() for collection in historical_payments] if historical_payments else []
    
    form = SearchForm()

    busqueda = []
    orden = []
    form.tipo_filtro.choices = [(campo, campo.replace('_',' ').capitalize()) for campo in busqueda]
    form.orden_filtro.choices = [(campo, campo.replace('_', ' ').capitalize()) for campo in orden]
    
    for param, valor in params.to_dict().items():
        if param in form._fields:
            form._fields[param].data = valor

    return render_template('reports/reports_search_box.html', entidad='reports', anterior=url_for('reports.reports'), form=form, lista_diccionarios=historical_payments_list, total=total, current_page=page, per_page=per_page, pages=pages,titulo='Listado de reportes')


@bp.get('/proposals_rank')
@handle_error(lambda: url_for('home'))
def proposals_rank():
    jobs_ranking = ReportService.get_propuestas_ranking()
    return render_template('reports/reports_list_v2.html',jobs_ranking=jobs_ranking)
