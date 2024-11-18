from src.core.database import db
from src.core.models.publication import Publication
class PublicationService:

    @staticmethod
    def list_publications(page, per_page):
        pagination = Publication.query.paginate(page=page, per_page=per_page, error_out=False)
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

