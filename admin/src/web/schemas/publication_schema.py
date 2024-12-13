from marshmallow import Schema, fields, post_dump

from src.web.utils import PUBLICATION_MAPPING


class PublicationSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    summary = fields.Str()
    content = fields.Str()
    author = fields.Str()
    published_date = fields.Date()

    @post_dump
    def translate_fields(self, data, **kwargs):
        return {PUBLICATION_MAPPING.get(k, k): v for k, v in data.items()}


publication_schema = PublicationSchema()
publications_schema = PublicationSchema(many=True)
