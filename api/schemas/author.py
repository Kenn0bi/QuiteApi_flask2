from api import ma
from api.models.author import AuthorModel


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthorModel

    id = ma.auto_field()
    name = ma.auto_field()
    surname = ma.auto_field()


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
