from src.core.database import db
from src.core.models.publication import Publication
class PublicationService:

    @staticmethod
    def list_publications(filtro=None, order_by=None, ascending=True, page=1, per_page=5):
        publications_query = Publication.query
        if filtro:
            valid_filters = {key: value for key, value in filtro.items() if hasattr(Publication, key) and value is not None}
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

        pagination = publications_query.query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages


    @staticmethod
    def get_publication_by_id(publication_id):
        publication = Publication.query.get(publication_id)
        if publication is None:
            raise ValueError('La publicacion solicitada no existe')

        return publication

    @staticmethod
    def create_publication(publication_data):
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
        db.session.delete(publication)
        db.session.commit()

    @staticmethod
    def form_to_dict(form):
        return {'title': form.title.data,
            'summary': form.summary.data,
            'content': form.body.data,
            'status': form.status.data,
            'published_date': form.published_at.data,
            'author': 'Current user' #TODO: tomar el usuario que carga la publicacion
        }

