from datetime import datetime, timezone

from core.services.employee_service import EmployeeService
from src.core.database import db
from src.core.models.publication import Publication, PublicationStatusEnum

from web.handlers.auth import get_current_user_id
from src.core.services.user_service import UserService


class PublicationService:

    @staticmethod
    def list_publications(include_deleted=False, filtro=None, order_by=None, ascending=True, page=1, per_page=5):
        publications_query = Publication.query.filter_by(deleted=include_deleted)
        if filtro:
            valid_filters = {key: value for key, value in filtro.items() if hasattr(Publication, key) and value is not None}
            if 'status' in valid_filters:
                publications_query = publications_query.filter(Publication.status == valid_filters['status'])
            if 'title' in valid_filters:
                publications_query = publications_query.filter(Publication.title.ilike(valid_filters['title']))
            if 'start_published_date' in valid_filters:
                publications_query = publications_query.filter(Publication.published_date >= valid_filters['start_published_date'])
            if 'end_published_date' in valid_filters:
                publications_query = publications_query.filter(Publication.published_date <= valid_filters['end_published_date'])
        if order_by:
            if ascending:
                publications_query = publications_query.order_by(getattr(Publication, order_by).asc())
            else:
                publications_query = publications_query.order_by(getattr(Publication, order_by).desc())

        pagination = publications_query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages


    @staticmethod
    def get_publication_by_id(publication_id, include_deleted=False):
        publication = Publication.query.filter_by(id=publication_id)
        if not include_deleted:
            publication = publication.filter_by(deleted = include_deleted)
        if publication is None:
            raise ValueError('La publicacion solicitada no existe')

        return publication.first()

    @staticmethod
    def create_publication(publication_data):
        author_user = UserService.get_user_by_id(get_current_user_id())
        employee = EmployeeService.get_employee_by_id(author_user.employee_id)
        publication_data['author'] = f"{employee.nombre} {employee.apellido}"
        publication = Publication(**publication_data)
        db.session.add(publication)
        db.session.commit()
        return publication

    @staticmethod
    def update_publication(publication_id, publication_data):
        publication = Publication.query.get(publication_id)
        if publication is None:
            raise ValueError('La publicacion solicitada no existe')
        for key, value in publication_data.items():
            setattr(publication, key, value)
        db.session.commit()
        return publication

    @staticmethod
    def delete_publication(publication_id):
        publication = Publication.query.get(publication_id)
        if publication is None:
            raise ValueError('La publicacion solicitada no existe')
        publication.deleted = True
        db.session.commit()

    @staticmethod
    def form_to_dict(form):
        return {
            'title': form.title.data,
            'summary': form.summary.data,
            'content': form.body.data,
            'status': form.status.data,
            'published_date': form.published_at.data,
        }

    @staticmethod
    def create_example_publications():
        """Crea publicaciones de ejemplo para tener cargada la bd"""

        sample_data = [
            {
                "title": "Primer ejemplo",
                "summary": "Este es un resumen del primer ejemplo.",
                "content": "Contenido detallado del primer ejemplo.",
                "status": PublicationStatusEnum.PUBLICADO,
                "author": "Juan Vergara",
                "published_date": datetime.now(timezone.utc),
            },
            {
                "title": "Segundo ejemplo",
                "summary": "Resumen breve del segundo ejemplo.",
                "content": "Este es el contenido del segundo ejemplo.",
                "status": PublicationStatusEnum.BORRADOR,
                "author": "Juan Vergara",
                "published_date": datetime.now(timezone.utc),
            },
            {
                "title": "Tercer ejemplo",
                "summary": "Un resumen interesante para el tercer ejemplo.",
                "content": "Aquí está el contenido del tercer ejemplo.",
                "author": "Autor 3",
                "status": PublicationStatusEnum.ARCHIVADO,
                "author": "Juan Vergara",
                "published_date": datetime.now(timezone.utc),
            },
            {
                "title": "Cuarto ejemplo",
                "summary": "Resumen del cuarto ejemplo.",
                "content": "Contenido extenso para el cuarto ejemplo.",
                "status": PublicationStatusEnum.ARCHIVADO,
                "author": "Juan Vergara",
                "published_date": datetime.now(timezone.utc),
            },
            {
                "title": "Quinto ejemplo",
                "summary": "Resumen del quinto ejemplo.",
                "content": "Contenido bien estructurado del quinto ejemplo.",
                "status": PublicationStatusEnum.BORRADOR,
                "author": "Juan Vergara",
                "published_date": datetime.now(timezone.utc),
            },
        ]

        for data in sample_data:
            publicacion = Publication(**data)
            db.session.add(publicacion)
        db.session.commit()
