# Vistas Principales
- `search_box`: Listados de entidades
- `form`: Formularios de entidad 
- `detail`: Detalles de entidad
- `different_detail`: Detalle de entidad con apartado de listado de archivos

## Especificaciones de las vistas

### `search_box` -> para listados:
- **anterior**: Ruta a la que volver, ej: `"url_for('home')=localhost:5000/"` lleva al inicio.

- **lista_diccionarios**: Listado de elementos en formato `dict`, deben tener obligatoriamente la `id`. Ejemplo:
    ```json
    [
        {   
            "id": "1",
            "nombre": "pepe"
        },
        {
            "id": "10",
            "nombre": "esteban"
        }
    ]
    ```
    **Importante**: los campos de la tabla se toman del primer elemento, y el resto de los elementos deben tener los mismos campos.

- **entidad**: Nombre del blueprint. Debe respetar los siguientes métodos:

    - `search_<entidad>`: Para listados, manda por `args` los siguientes parámetros:
        - `busqueda`: String del campo de texto.
        - `tipo_filtro`: Atributo que se quiere buscar con el campo `busqueda`.
        - `orden_filtro`: Campo por el que se quiere ordenar.
        - `orden`: Tipo de orden, `asc` o `desc`.
        - `page`: Página que se quiere con el filtro anterior (puede no haber filtro).
        - `per_page`: Cantidad de elementos por página a retornar.
        
        Debe retornar los argumentos que pide la vista.

    - `detail_<entidad>`: Detalle de la entidad respectiva, usa parámetros de ruta `<int:id>`. Recibe el parámetro `id`.
    
    - `new_<entidad>`: Formulario de creación de la entidad respectiva. No recibe parámetros.
    
    - `update_<entidad>`: Formulario de actualización de la entidad respectiva, usa parámetro de ruta `<int:id>`. Recibe el parámetro `id`.
    
    - `delete_<entidad>`: Eliminación lógica de la entidad respectiva, recibe parámetro de ruta `<int:id>`. Recibe el parámetro `id`.

- **form**: Clase de `Flask-WTForms` con los siguientes campos:
    - `busqueda`: `StringField`
    - `tipo_filtro`: `SelectField`
    - `orden_filtro`: `SelectField`
    - `orden`: `RadioField`

- **total**: Total de tuplas de la entidad. No confundir con la cantidad de páginas.

- **current_page**: Página actual del listado.

- **per_page**: Cantidad de elementos por página.

- **pages**: Total de páginas disponibles.

### `form` -> para formularios:
- **titulo**: Título del formulario.
  
- **ruta_post**: Ruta donde el formulario hará el `POST`. Conviene que sea la misma ruta del formulario. Ejemplo:
    ```python
    ruta_post = '/clients/create'
    ```
    Se puede mandar con:
    ```python
    url_for('clients.new_clients')
    ```

- **form**: Clase de `Flask-WTForms` que representa el formulario. No se debe incluir el `submit` en la clase.

- **url_volver**: Ruta a la que volver, ej: `"url_for('home')=localhost:5000/"` lleva al inicio.

- **NOTA**: Tiene un espacio `{% block complementos %}` para agregar lógica con JS heredando si es necesario.

### `detail` -> Detalle de la entidad correspondiente:
- **titulo**: Título de la página de detalle, ej: `"Detalle de Luciano Macias - 44130359"`.

- **anterior**: Ruta a la que volver, ej: `"url_for('home')=localhost:5000/"` lleva al inicio.

- **diccionario**: Diccionario con los campos que se desean listar en el detalle. La `id` es obligatoria. Ejemplo:
    ```json
    {
        "id": 1,
        "nombre": "Luciano",
        "apellido": "Macias",
        "DNI": "44130359",
        "Detalles extra": "[...]"
    }
    ```

- **entidad**: Nombre del blueprint, debe respetar lo anteriormente listado en `search_box`.

### `different_detail` -> Detalle de entidad con apartado para archivos:
- **titulo**: Título de la página de detalle, ej: `"Detalle de Luciano Macias - 44130359"`.

- **anterior**: Ruta a la que volver, ej: `"url_for('home')=localhost:5000/"` lleva al inicio.

- **diccionario**: Diccionario con los campos que se desean listar en el detalle. La `id` es obligatoria. Ejemplo:
    ```json
    {
        "id": 1,
        "nombre": "Luciano",
        "apellido": "Macias",
        "DNI": "44130359",
        "Detalles extra": "[...]"
    }
    ```

- **entidad**: Nombre del blueprint, debe respetar lo anteriormente listado en `search_box`.

- **activo**: Tab activa por defecto al entrar. Valores posibles:
    - `'informacion'`: Detalle activo por defecto.
    - `'documents'`: Listado de archivos activo por defecto.

- **form**: Clase de `Flask-WTForms` con los siguientes campos:
    - `busqueda`: `StringField`
    - `tipo_filtro`: `SelectField`
    - `orden_filtro`: `SelectField`
    - `orden`: `RadioField`

- **lista_diccionarios**: Listado de elementos en formato `dict`, deben tener obligatoriamente la `id`. Ejemplo:
    ```json
    [
        {   
            "id": "1",
            "titulo": "archivo.pdf"
        },
        {
            "id": "10",
            "titulo": "fotocopia dni en drive"
        }
    ]
    ```
    **Importante**: Los campos de la tabla se toman del primer elemento, y el resto de los elementos deben tener los mismos campos.
    
    **IMPORTANTE**: Los diccionarios de archivos deben tener el campo `"es_link"`.

- **total**: Total de tuplas de la entidad. No confundir con la cantidad de páginas.

- **current_page**: Página actual del listado.

- **per_page**: Cantidad de elementos por página.

- **pages**: Total de páginas disponibles.

- **entidad_archivos**: Lo mismo que `entidad`, pero del blueprint de los archivos.
