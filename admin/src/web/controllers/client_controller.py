from core.services.employee_service import EmployeeService
from core.services.equestrian_service import EquestrianService
from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.client_service import ClientService
from src.web.handlers.auth import check_permissions
from src.web.handlers import handle_error
from src.web.handlers import get_int_param, get_str_param, get_bool_param
from src.core.enums.permission_enums import PermissionCategory, PermissionModel
from src.web.forms.client_forms.create_client_form import ClientFirstForm, ClientSecondForm, ClientThirdForm, ClientFourthForm, ClientFifthForm, ClientSixthForm, ClientSeventhForm
from flask import session


clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.get('/')
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.INDEX.value}")
@handle_error(lambda: url_for('index'))
def search_clients():
    """Lista todos los clientes con paginación."""
    """params = request.args.keys()
    
    page = params['page'] if params['page'] is not None else 1
    per_page = params['per_page'] if params['per_page'] is not None else 25
    
    filtro = None
    
    users, total, pages = ClientService.get_clients(filtro=filtro,page=page, per_page=per_page)
    
    return render_template('user/list.html', users=users, total=total, pages=pages, current_page=page, per_page=per_page)"""
    clients, total, pages = ClientService.get_clients()
    return render_template('client/show_data.html', data=clients, titulo='Search_clients')

@clients_bp.get('/<int:user_id>')
@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.SHOW.value}")
@handle_error(lambda user_id: url_for('clients.search_clients'))
def detail_clients(user_id):
    """Muestra los detalles de un cliente por su ID.""" 
    cliente = ClientService.get_client_by_id(user_id)
    return render_template('client/show_data.html', titulo="Detail Clients",data=cliente)

@clients_bp.route('/create', methods=['GET','POST'])
#@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}")
#@handle_error(lambda: url_for('auth.index'))
def new_client():
    paso = session.get('paso',default=0)
    paso = paso if (paso < 7) else 0
    forms = [ClientFirstForm(),ClientSecondForm(), ClientThirdForm(), ClientFourthForm(), ClientFifthForm(), ClientSixthForm(), ClientSeventhForm()]
    
    if (paso == 6) or (paso == 5):
        empleados = [(emp.id, emp.dni + ': ' + emp.nombre + ' ' + emp.apellido) for emp in EmployeeService.get_all_employees()]
        forms[paso if paso == 6 else 6].propuesta_trabajo.profesor.choices = empleados
        forms[paso if paso == 6 else 6].propuesta_trabajo.conductor.choices = empleados
        forms[paso if paso == 6 else 6].propuesta_trabajo.auxiliar.choices = empleados
        forms[paso if paso == 6 else 6].propuesta_trabajo.caballo.choices = [(eq.id, str(eq.id)+ ': ' + eq.nombre) for eq in EquestrianService.get_all_equestrian()[0]]
    
    if request.method == 'POST' and forms[paso].validate_on_submit():
        datos = dict()
        if paso == 0:
            for f1 in forms[paso]:
                if f1.name == 'csrf_token':
                    continue
                
                if f1.name == 'contacto_emergencia':
                    datos[f1.name] = {
                        'nombre': f1.form.nombre.data,
                        'telefono': f1.form.telefono.data
                    }
                    
                elif f1.name == 'domicilio':
                    datos[f1.name] = f1.form.calle.data +' N'+f1.form.numero.data
                    if f1.form.departamento.data:
                        datos[f1.name] += ' dpto ' + f1.form.departamento.data
                    
                    datos[f1.name] += ' ' + f1.form.localidad.data
                    datos[f1.name] += ', ' + f1.form.provincia.data
                
                elif f1.name == 'lugar_nacimiento':
                    datos[f1.name] = f1.form.localidad_nacimiento.data + ' provincia de ' + f1.form.provincia_nacimiento.data
                    
                else:
                    datos[f1.name] = f1.data
        
        elif paso == 1:
            for f24 in forms[paso]:
                if f24.name == 'csrf_token':
                    continue
                
                if f24.name == 'otro_cert' and f24.data is not None and f24.data:
                    datos['cert_discapacidad'] = f24.data
                else:
                    datos[f24.name] = f24.data # guardo segundo paso
        
        elif paso == 2 or paso == 4:
            for f3 in forms[paso]:
                if f3.name == 'csrf_token':
                    continue
                
                datos[f3.name] = f3.data # tercera parte
                
        elif paso == 3:
            institucion = dict()
            for f4 in forms[paso].institucion_escolar.form:
                if f4.name == 'csrf_token':
                    continue
                
                if f4.name == 'direccion':
                    for dato in f4.direccion:
                        institucion[dato.name] = dato.data
                else:
                    institucion[f4.name] = f4.data
            
            datos['institucion_escolar'] = institucion
        
        elif paso == 5:
            responsables = dict()
            for f5 in forms[paso]:
                if f5.name == 'csrf_token':
                    continue
                
                for tutor in f5:
                    for campo in tutor.form:
                        if campo.name == 'csrf_token':
                            continue
                        
                        if campo.name == 'domicilio':
                            responsables[campo.name] = campo.form.calle.data +' N'+campo.form.numero.data
                            if campo.form.departamento.data:
                                responsables[campo.name] += ' dpto ' + campo.form.departamento.data
                            
                            responsables[campo.name] += ' ' + campo.form.localidad.data
                            responsables[campo.name] += ', ' + campo.form.provincia.data
                        
                        else:
                            responsables[campo.name] = campo.data
            
            datos['tutores_responsables'] = responsables
            
        elif paso == 6:
            propuesta_trabajo = dict()
            for f6 in forms[paso].propuesta_trabajo.form:
                if f6.name == 'csrf_token':
                        continue
                
                if f6.name in ['profesor','conductor','auxiliar']:
                    EmployeeService.get_employee_by_id(f6.data)
                    propuesta_trabajo[f6.name] = f6.data
                else:
                    propuesta_trabajo[f6.name] = f6.data
                    
            datos['propuesta_trabajo'] = propuesta_trabajo

        session['cliente'] = datos if (paso == 0) else {**session['cliente'], **datos} # guardo datos
        
        paso += 1
        session['paso'] = paso
        
        print(session['cliente'])
    
    
    if paso <= 6:
        form = forms[paso]
        
        return render_template('/client/paginated_form.html', form=form, ruta_post=url_for('.new_client'), activa=paso,tabs=["Datos Personales", "Detalles", "Situacion previsional", "Institucion Escolar", "Atención", "Tutores Legales", "Propuesta de Trabajo"])
    else:
        ClientService.create_client(**session['cliente'])
        del session['cliente']
        del session['paso']
        return redirect(url_for('clients.search_clients'))

@clients_bp.route('/create/cancelar', methods=['GET','POST'])
#@check_permissions(f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}")
#@handle_error(lambda: url_for('auth.index'))
def cancelar_form():
    if session.get('cliente',0):
        del session['cliente']
    if session.get('paso',0):
        del session['paso']
    return redirect(url_for('clients.search_clients'))