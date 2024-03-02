import flask
from flask import request, jsonify

from packages.app import get_app
from packages.error import HttpError
from packages.models import Session, MODEL_TYPE, MODEL
from packages.views import UserView, LoginView, AdsView


app = get_app()


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error': error.massage})
    response.status_code = error.status_code
    return response


def get_item_by_id(model: MODEL_TYPE, item_id: int) -> MODEL:
    item = request.session.query(model).get(item_id)
    if item is None:
        return jsonify({'error': 'item not found'}), 404
    return item


user_view = UserView.as_view('user_view')
login_view = LoginView.as_view('login_view')
ads_view = AdsView.as_view('ads_view')

app.add_url_rule('/login',
                 view_func=login_view,
                 methods=['POST'])

app.add_url_rule('/user',
                 view_func=user_view,
                 methods=['POST', 'GET', 'PATCH', 'DELETE'])

app.add_url_rule('/ads',
                 view_func=ads_view,
                 methods=['GET', 'POST'])

app.add_url_rule('/ads/<int:ad_id>',
                 view_func=ads_view,
                 methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run()
