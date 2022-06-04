migrate:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

run:
	python manage.py runserver

celery-default:
	celery -A mailing worker -l INFO -P eventlet -n default@%h -Q default

celery-mailing:
	celery -A mailing worker -l INFO -P eventlet -n mailing@%h -Q mailing