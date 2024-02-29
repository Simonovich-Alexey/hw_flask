from flask import request
from flask_bcrypt import Bcrypt

from packages.app import get_app
from packages.error import HttpError
from packages.models import Token

bcrypt = Bcrypt(get_app())


def hash_password(password: str):
    return bcrypt.generate_password_hash(password.encode()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.check_password_hash(password.encode(), hashed_password.encode())


def check_token(handler):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            raise HttpError(401, "token not found")
        token = request.session.query(Token).filter_by(token=token).first()
        if token is None:
            raise HttpError(401, "invalid token")
        request.token = token
        return handler(*args, **kwargs)
    return wrapper
