from src.core.database import db
from src.core.models.publication import Publication

class PublicationService:

    @staticmethod
    def list_publications(page, per_page):
        return Publication.query.paginate(page=page, per_page=per_page)


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

