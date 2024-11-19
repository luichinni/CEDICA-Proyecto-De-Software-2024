from src.core.services.client_service import ClientService
from src.core.services.collection_service import CollectionService
from src.core.models.collection import Collection
from src.core.models.client import Clients, PropuestasInstitucionales, Discapacidad
from sqlalchemy import func
from datetime import datetime

class ReportService:

    @staticmethod
    def get_result(keys, values, sort=True):
        """
        Generate a dictionary that maps keys to their corresponding values.

        This method initializes a dictionary with keys provided in the `keys` argument,
        setting their initial values to zero. It then updates the dictionary with values
        from the `values` argument, which should be an iterable of tuples. Optionally, 
        the resulting dictionary can be sorted by value in descending order.

        Args:
            keys (iterable): An iterable containing the keys to initialize in the result dictionary.
            values (iterable): An iterable of tuples where each tuple contains a key and its corresponding value.
            sort (bool): A flag indicating whether to sort the resulting dictionary by values (default is True).

        Returns:
            dict: A dictionary where keys are from the `keys` argument and values are updated from the `values` argument. 
                If `sort` is True, the dictionary is sorted by values in descending order.
        """
        # Inicializado en 0, ya que algunos key podrian no aparecer en values
        res = {key: 0 for key in keys}
        
        for key, value in values:
            res[key] = value
            
        if sort:
            res = dict(sorted(res.items(), key=lambda x: x[1], reverse=True))

        return res



    @staticmethod
    def get_propuestas_ranking() -> dict:
        """
        Obtiene un ranking de las propuestas de trabajo más solicitadas.

        Returns:
            dict: Un diccionario con las propuestas de trabajo como claves y la cantidad
                de veces que cada propuesta fue seleccionada como valores.
        """
        propuestas_counts = [ (propuesta.name, count)  for propuesta, count in (
                Clients.query
                .with_entities(Clients.propuesta_trabajo, func.count(Clients.propuesta_trabajo))
                .group_by(Clients.propuesta_trabajo)
                .all()
            )
        ]
        
        propuestas = [propuesta.name for propuesta in PropuestasInstitucionales]
        return ReportService.get_result(propuestas,propuestas_counts)
    
    @staticmethod
    def get_becados_count() -> dict:
        """
        Obtiene un ranking de clientes becados y no becados.

        Returns:
            dict: Un diccionario con dos elementos: "becados" y "no becados", que 
            indica la cantidad de clientes en cada categoría.
        """
        becado_counts = [
            ("becados" if is_becado else "no becados", count)
            for is_becado, count in (
                Clients.query
                .with_entities(Clients.becado, func.count(Clients.becado))
                .group_by(Clients.becado)
                .all()
            )
        ]

        categorias = {"becados", "no becados"}
        return ReportService.get_result(categorias,becado_counts)

    @staticmethod
    def get_becados_count() -> dict:
        """
        Obtiene un ranking de clientes becados y no becados.

        Returns:
            dict: Un diccionario con dos elementos: "becados" y "no becados", que 
            indica la cantidad de clientes en cada categoría.
        """
        becado_counts = [
            ("becados" if is_becado else "no becados", count)
            for is_becado, count in (
                Clients.query
                .with_entities(Clients.becado, func.count(Clients.becado))
                .group_by(Clients.becado)
                .all()
            )
        ]

        categorias = {"becados", "no becados"}
        return ReportService.get_result(categorias,becado_counts)

    @staticmethod
    def get_income_by_year() -> dict:
        """
        Obtiene la cantidad de ingresos por año.

        Returns:
            dict: Un diccionario donde las claves son cadenas en el formato "YYYY" 
            representando el año y mes, y los valores son la cantidad total de ingresos para cada periodo.
        """
        income_counts = (
            Collection.query
            .with_entities(
                func.extract("year", Collection.payment_date).label("year"),
                func.sum(Collection.amount).label("total_amount")
            )
            .group_by("year")
            .all()
        )
        res = {str(int(year)).zfill(4): total_amount for year, total_amount in income_counts}
        res = dict(sorted(res.items(), key=lambda x: int(x[0])))
        print(res)
        return res

    @staticmethod
    def get_cert_discapacidad_count() -> dict:
        """
        Obtiene el conteo de clientes con o sin certificado de discapacidad.

        Returns:
            dict: Un diccionario con dos elementos: "con_certificado" y "sin_certificado", 
            que indica la cantidad de clientes en cada categoría.
        """
        cert_discapacidad_counts = [
            ("con_certificado" if tiene_certificado_de_disc else "sin_certificado", count)
            for tiene_certificado_de_disc, count in (
                Clients.query
                .with_entities(
                    (Clients.cert_discapacidad.isnot(None)).label("tiene_certificado_de_disc"),
                    func.count()
                )
                .group_by("tiene_certificado_de_disc")
                .all()
            )
        ]

        categorias = {"con_certificado", "sin_certificado"}
        return ReportService.get_result(categorias, cert_discapacidad_counts)

    @staticmethod
    def get_discapacidad_count() -> dict:
        """
        Obtiene el conteo de clientes para cada tipo de discapacidad.

        Returns:
            dict: Un diccionario con cada tipo de discapacidad como clave y la cantidad de 
            clientes con esa discapacidad como valor.
        """
        discapacidad_counts = [
            (discapacidad.name, count)
            for discapacidad, count in (
                Clients.query
                .with_entities(Clients.discapacidad, func.count(Clients.discapacidad))
                .group_by(Clients.discapacidad)
                .all()
            )
        ]

        discapacidades = [discapacidad.name for discapacidad in Discapacidad]
        return ReportService.get_result(discapacidades, discapacidad_counts)


    @staticmethod
    def get_historical_payments_report(start_date: datetime, end_date: datetime, nombre: str = None, apellido: str = None, page: int = 1, per_page: int = 25):
        """
        Obtiene un reporte histórico de cobros en un rango de fechas asociado a una persona.

        Args:
            start_date (datetime): Fecha de inicio del rango.
            end_date (datetime): Fecha de fin del rango.
            nombre (str, optional): Nombre de la persona. Defaults to None.
            apellido (str, optional): Apellido de la persona. Defaults to None.
            page (int, optional): Número de página para la paginación. Defaults to 1.
            per_page (int, optional): Cantidad de resultados por página. Defaults to 25.

        Returns:
            tuple: Una tupla que contiene la lista de cobros, el total de registros y el total de páginas.
        """
        payments, total, total_pages = CollectionService.search_collections(
            start_date=start_date,
            end_date=end_date,
            nombre=nombre,
            apellido=apellido,
            page=page,
            per_page=per_page,
            order_by_date=True,
            ascending=False,
            include_deleted=False
        )
        
        return payments, total, total_pages
    
    
    @staticmethod
    def get_adeudores(page: int = 1, per_page: int = 25) -> tuple:
        """
        Obtiene un reporte de las personas que adeudan pagos.

        Args:
            page (int, optional): Número de página a obtener. Por defecto es 1.
            per_page (int, optional): Cantidad de resultados por página. Por defecto es 25.

        Returns:
            tuple: Una tupla que contiene la lista de clientes que adeudan pagos en la página especificada,
                   el total de resultados y el número total de páginas.
        """
        filtro = {'adeuda': True}
        adeudores, total, total_pages = ClientService.get_clients(filtro=filtro, page=page, per_page=per_page)

        return adeudores, total, total_pages
