FROM python:3.11-slim

COPY ./app /app
WORKDIR /app
COPY ./app/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT gunicorn main:app --bind 0.0.0.0:5000