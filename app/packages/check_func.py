from flask import request
from sqlalchemy.exc import IntegrityError
from packages.error import HttpError
from packages.models import MODEL_TYPE, MODEL
from pydantic import ValidationError


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


def validate(model, data: dict):
    try:
        return model.model_validate(data).model_dump(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)
