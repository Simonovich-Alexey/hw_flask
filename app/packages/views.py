from flask import jsonify, request
from flask.views import MethodView

from packages.auth import hash_password, check_password, check_token
from packages.error import HttpError
from packages.models import User, Token
from packages.check_func import add_item, delete_item, update_item


class UserView(MethodView):
    @check_token
    def get(self):
        return jsonify(request.token.user.dict)

    def post(self):
        user_data = request.json
        user_data['password'] = hash_password(user_data['password'])
        user = User(**user_data)
        add_item(user)
        return jsonify(user.dict)

    @check_token
    def patch(self):
        user_data = request.json
        user_data['password'] = hash_password(user_data['password'])
        user = request.token.user
        update_item(user, user_data)
        return jsonify(user.dict)

    @check_token
    def delete(self):
        delete_item(request.token.user)
        return jsonify({"status": "delete"})


class LoginView(MethodView):
    def post(self):
        payload = request.json
        user = request.session.query(User).filter_by(name=payload["name"]).first()
        if user is None:
            raise HttpError(404, "user not found")
        if check_password(user.password, payload["password"]):
            token = Token(**{"user_id": user.id})
            add_item(token)
            return jsonify({"token": token.token})
        raise HttpError(401, "invalid password")
