
echo "Apply migrations for other apps."
python manage.py migrate contenttypes

echo "Apply migrations for other apps."
python manage.py migrate auth

echo "Apply migrations for other apps."
python manage.py migrate api 0001_initial

echo "Apply migrations for other apps."
python manage.py migrate account

echo "Apply migrations for other apps."
python manage.py migrate admin

echo "Apply migrations for other apps."
python manage.py migrate authtoken

echo "Apply migrations for other apps."
python manage.py migrate sessions

echo "Apply migrations for other apps."
python manage.py migrate sites

echo "Apply migrations for other apps."
python manage.py migrate socialaccount

echo "Apply migrations for api."
python manage.py migrate api 0002_vacancies_certificate_filter_follower_quizz_and_more

echo "Create a superuser."
python manage.py createsuperuser-ifnot

echo "Collect static files."
python manage.py collectstatic --noinput

echo "Start the server."
python manage.py runserver 0.0.0.0:8000
