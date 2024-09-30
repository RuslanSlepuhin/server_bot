echo "Apply migrations for api."
python manage.py migrate api

echo "Apply migrations for other apps."
python manage.py migrate

echo "Start gunicorn"
gunicorn --bind 0.0.0.0:8000 itcoty_web.wsgi