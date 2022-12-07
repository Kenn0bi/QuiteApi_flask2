from api import app, db, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


@app.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = UserModel.query.get(user_id)
    if user:
        return user_schema.dump(user), 200
    return f'User id={user_id} not found', 404


@app.route('/users/<int:user_id>/role', methods=["PUT"])
@multi_auth.login_required()
def change_user_role(user_id):
    user_data = request.json
    user = UserModel.query.get(user_id)
    if user:
        user.role = user_data["role"]
        db.session.commit()
        return user_schema.dump(user), 200
    return f'User id={user_id} not found', 404


# url: /users
@app.route('/users')
def get_users():
    users = UserModel.query.all()
    if users:
        return users_schema.dump(users), 200
    return f'Users not found', 404


@app.route('/users', methods=["POST"])
@multi_auth.login_required()
def create_user():
    user_data = request.json
    user = UserModel(user_data["username"], user_data["password"])
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201



