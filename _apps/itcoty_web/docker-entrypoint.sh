
echo "Apply migrations."
python manage.py migrate

echo "Create a superuser."
python manage.py createsuperuser-ifnot

echo "Collect static files."
python manage.py collectstatic --noinput

echo "Start the server."
python manage.py runserver 0.0.0.0:8000
