#!/bin/sh

#python3 manage.py collectstatic --noinput
# python3 manage.py migrate
if [ -z "$ENVIRONMENT" ]; then
    echo "The ENVIRONMENT variable is set to LOCAL"
#    yes | python manage.py makemigrations
#    yes yes | python manage.py migrate
#    yes | python3 manage.py migrate django_celery_beat
#    yes | python3 manage.py migrate django_celery_results
#    python manage.py loaddata fixtures/data.json
    #python manage.py loaddata fixtures/data_dump.json
fi

gunicorn --workers 2 --timeout 600 --bind 0.0.0.0:8000 book_management.wsgi:application
#gunicorn --workers 2 --timeout 600 --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=book_management.settings book_management.wsgi:application --log-level=debug

