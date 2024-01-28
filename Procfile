release: python manage.py migrate
web: gunicorn core.wsgi.prod --log-file - --log-level debug
