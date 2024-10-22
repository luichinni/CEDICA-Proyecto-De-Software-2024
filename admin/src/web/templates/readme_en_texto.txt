Vistas Principales
search_box: listados de entidades
form: formularios de entidad 
detail: detalles de entidad
different_detail: detalle de entidad con apartado de listado de archivos

Especificaciones de las vistas
search_box -> para listados:
    anterior => ruta a la que volver ej, "url_for('home')=localhost:5000/" lleva al inicio

    lista_diccionarios => listado de elementos en formato dict, deben tener obligatoriamente la id
                            ej: [
                                    {   
                                        'id':'1',
                                        'nombre':'pepe'   
                                    },
                                    {
                                        'id':'10',
                                        'nombre':'esteban'
                                    }
                                ]
                        importante! los campos de la tabla se toman del elemento 0 y el resto de elementos deben tener los campos

    entidad => nombre del blueprint donde debe respetar tener los siguientes métodos:
                        search_<entidad> -> para listados, manda por args los parametros:
                                busqueda: string del campo de texto
                                tipo_filtro: atributo que se quiere buscar con el campo busqueda
                                orden_filtro: campo por el que se quiere ordenar
                                orden: tipo de orden, asc o desc
                                page: pagina que se quiere con el filtro anterior (puede no haber filtro)
                                per_page: cantidad de elementos por pagina a retornar
                                >>> mirar el form de ejemplo para la busqueda
                            Debe retornar los argumentos que pide la vista

                        detail_<entidad> -> detalle de la entidad respectiva, usa parametros de ruta <int:id>
                                recibe el parametro id
                            Debe retornar la vista detail (anotada más adelante)

                        new_<entidad> -> formulario de creacion de la entidad respectiva, no recibe parametros
                            Debe retornar la vista form (anotada más adelante)

                        update_<entidad> -> formulario de actualización de datos de la entidad respectiva, usa param de ruta <int:id>
                                recibe el parametro id
                            Debe retornar la vista form (anotada más adelante)
                            
                        delete_<entidad> -> eliminacion logica de la entidad respectiva, recibe param de ruta <int:id>
                                recibe el parametro id
                            Debe eliminar logicamente la entidad y retornar la página a gusto.

    form => clase de flask-wtforms con los campos:
                        busqueda -> StringField
                        tipo_filtro -> SelectField
                        orden_filtro -> SelectField
                        orden -> RadioField

    total => total de tuplas de la entidad, no confundir con catidad de paginas

    current_page => pagina actual del listado

    per_page => cantidad de elementos por pagina

    pages => total de paginas disponibles

form -> para formularios:
    titulo => titulo del formulario

    ruta_post => ruta donde el formulario hará el post (por temas de checkeo y mostrar errores, conviene que sea la misma ruta del form)
                    ej: ruta_post = '/clients/create'
                        puede mandarse con
                        url_for('clients.new_clients')

    form => clase de flask-wtforms que representa el formulario, no se debe incluir el submit en la clase.

    url_volver => ruta a la que volver ej, "url_for('home')=localhost:5000/" lleva al inicio

    NOTA: tiene un espacio {% block complementos %} para agregar logica con js heredando si es necesario


detail -> detalle de la entidad correspondiente:
    titulo => titulo de la pagina de detalle, ej "Detalle de Luciano Macias - 44130359"

    anterior => ruta a la que volver ej, "url_for('home')=localhost:5000/" lleva al inicio

    diccionario => diccionario con los campos que se desean listar en el detalle, ID OBLIGATORIA, ej:
                    {
                        'id': 1,
                        'nombre':'Luciano',
                        'apellido':'Macias',
                        'DNI':'44130359',
                        'Detalles extra': '[...]'
                    }
    
    entidad => nombre del blueprint, debe respetar lo anteriormente listado en search_box


different_detail -> detalle de entidad con apartado para archivos:
    titulo => titulo de la pagina de detalle, ej "Detalle de Luciano Macias - 44130359"

    anterior => ruta a la que volver ej, "url_for('home')=localhost:5000/" lleva al inicio

    diccionario => diccionario con los campos que se desean listar en el detalle, ID OBLIGATORIA, ej:
                    {
                        'id': 1,
                        'nombre':'Luciano',
                        'apellido':'Macias',
                        'DNI':'44130359',
                        'Detalles extra': '[...]'
                    }
    
    entidad => nombre del blueprint, debe respetar lo anteriormente listado en search_box

    activo => que tab está activa por defecto al entrar, valores posibles:
                    'informacion': detalle activo por defecto
                    'documents': listado de archivos activo por defecto

    form => clase de flask-wtforms con los campos:
                        busqueda -> StringField
                        tipo_filtro -> SelectField
                        orden_filtro -> SelectField
                        orden -> RadioField

    lista_diccionarios => listado de elementos en formato dict, deben tener obligatoriamente la id
                            ej: [
                                    {   
                                        'id':'1',
                                        'titulo':'archivo.pdf'   
                                    },
                                    {
                                        'id':'10',
                                        'titulo':'fotocopia dni en drive'
                                    }
                                ]
                        importante! los campos de la tabla se toman del elemento 0 y el resto de elementos deben tener los campos
                        IMPORTANTE! los diccionarios de archivos deben tener el campo "es_link"
    
    total => total de tuplas de la entidad, no confundir con catidad de paginas

    current_page => pagina actual del listado

    per_page => cantidad de elementos por pagina

    pages => total de paginas disponibles

    entidad_archivos => lo mismo que entidad pero del blueprint de los archivos