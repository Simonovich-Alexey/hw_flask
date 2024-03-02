from flask import jsonify, request
from flask.views import MethodView
from packages.auth import hash_password, check_password, check_token, check_owner_ad
from packages.error import HttpError
from packages.models import User, Token, Ad
from packages.check_func import add_item, delete_item, update_item, get_item_by_id, validate
from packages.schema import CreateUser, UpdateUser, LoginUser, CreateAd, UpdateAd


class UserView(MethodView):
    @check_token
    def get(self):
        return jsonify(request.token.user.dict)

    def post(self):
        user_data = validate(CreateUser, request.json)
        user_data['password'] = hash_password(user_data['password'])
        user = User(**user_data)
        add_item(user)
        return jsonify(user.dict)

    @check_token
    def patch(self):
        user_data = validate(UpdateUser, request.json)
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
        user_data = validate(LoginUser, request.json)
        user = request.session.query(User).filter_by(name=user_data["name"]).first()
        if user is None:
            raise HttpError(404, "user not found")
        if check_password(user.password, user_data["password"]):
            token = Token(**{"user_id": user.id})
            add_item(token)
            return jsonify({"token": token.token})
        raise HttpError(401, "invalid password")


class AdsView(MethodView):
    def get(self, ad_id: int = None):
        if ad_id is None:
            return jsonify([ad.dict for ad in request.session.query(Ad)])
        ad = get_item_by_id(Ad, ad_id)
        return jsonify(ad.dict)

    @check_token
    def post(self):
        ad_data = validate(CreateAd, request.json)
        owner = request.token.user_id
        ad = Ad(**{'owner': owner}, **ad_data)
        add_item(ad)
        return jsonify(ad.dict)

    @check_token
    def patch(self, ad_id: int):
        ad_data = validate(UpdateAd, request.json)
        data = get_item_by_id(Ad, ad_id)
        check_owner_ad(data)
        ad = update_item(data, ad_data)
        return jsonify(ad.dict)

    @check_token
    def delete(self, ad_id: int):
        data = get_item_by_id(Ad, ad_id)
        check_owner_ad(data)
        delete_item(data)
        return jsonify({"status": "delete"})
