from flask import request
from sqlalchemy.exc import IntegrityError

from packages.error import HttpError
from packages.models import MODEL_TYPE, MODEL


def add_item(item: MODEL) -> MODEL:
    try:
        request.session.add(item)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'item already exists')


def get_item_by_id(model: MODEL_TYPE, item_id: int) -> MODEL:
    item = request.session.query(model).get(item_id)
    if item is None:
        raise HttpError(404, 'item not found')
    return item


def update_item(item: MODEL, json: dict) -> MODEL:
    for field, value in json.items():
        setattr(item, field, value)
    add_item(item)
    return item


def delete_item(item: MODEL):
    request.session.delete(item)
    request.session.commit()
