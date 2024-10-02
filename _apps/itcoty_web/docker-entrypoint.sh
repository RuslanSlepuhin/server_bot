
echo "Apply migrations for api."
python manage.py migrate api

echo "Apply migrations for other apps."
python manage.py migrate

echo "Collect static files."
python manage.py collectstatic --noinput

echo "Start server."
python manage.py runserver 0.0.0.0:8000
