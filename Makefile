migrate:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

run:
	python manage.py runserver