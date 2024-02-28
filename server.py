from typing import Type
import flask
from pydantic import ValidationError
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from package.models import User, Session, Ad
from package.schema import CreateUser, UpdateUser, CreateAd, UpdateAd


app = Flask('app')


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


def get_user_by_id(user_id: int):
    user = request.session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def get_ad_by_id(ad_id: int):
    ad = request.session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, "ad not found")
    return ad


def add_object(item):
    try:
        request.session.add(item)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "object already exists")


def validate_json(json_data: dict, schema_class):
    try:
        return schema_class(**json_data.dict(exclude_unset=True))
    except ValidationError as er:
        error = er.error()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = request.json
        with Session() as session:
            user = User(**user_data)
            session.add(user)
            session.commit()
            return jsonify(user.dict), 201

    def patch(self, user_id: int):
        user_data = ValidationError(request.json, UpdateUser)
        user = get_user_by_id(user_id)
        for field, value in user_data.items():
            setattr(user, field, value)
        add_object(user)
        return jsonify(user.dict)

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "delete"})


class AdView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)

    def post(self):
        ad_data = validate_json(request.json, CreateAd)
        ad = User(**ad_data)
        add_object(ad)
        return jsonify(ad.dict)

    def patch(self, ad_id: int):
        ad_data = ValidationError(request.json, UpdateAd)
        ad = get_ad_by_id(ad_id)
        for field, value in ad_data.items():
            setattr(ad, field, value)
        add_object(ad)
        return jsonify(ad.dict)

    def delete(self, ad_id: int):
        ad = get_ad_by_id(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"status": "delete"})


user_view = UserView.as_view('user_view')
ad_view = AdView.as_view('ad_view')


app.add_url_rule('/api/user/<int:user_id>',
                 view_func=user_view,
                 methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/api/user',
                 view_func=user_view,
                 methods=['POST'])

app.add_url_rule('/api/ad/<int:ad_id>',
                 view_func=ad_view,
                 methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/api/ad',
                 view_func=ad_view,
                 methods=['POST'])

if __name__ == '__main__':

    app.run()
