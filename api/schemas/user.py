from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       exclude = ["password_hash"]
       model = UserModel


user_schema = UserSchema()
users_schema = UserSchema(many=True)