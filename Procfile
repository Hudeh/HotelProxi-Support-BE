release: python manage.py migrate
web: daphne core.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A core.celery worker -l info
celerybeat: celery -A core beat -l INFO
celeryworker2: celery -A core.celery worker & celery -A core beat -l INFO & wait -n