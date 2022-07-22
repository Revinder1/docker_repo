#!/bin/sh
sleep 5
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8000 stocks_products.wsgi

exec "$@"