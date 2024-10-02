
echo "Apply migrations for api."
python manage.py migrate api

echo "Apply migrations for other apps."
python manage.py migrate

echo "Create a superuser."
python manage.py createsuperuser-ifnot

echo "Collect static files."
python manage.py collectstatic --noinput

echo "Start server."
python manage.py runserver 0.0.0.0:8000
