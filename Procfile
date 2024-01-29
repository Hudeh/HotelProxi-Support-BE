release: python manage.py migrate
web: daphne core.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery worker --app=core.celery.app
celerybeat: celery -A core beat -l INFO