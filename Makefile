#development variables
PORT ?= 8000
DB_NAME = fourth-project-hexlet
LOCAL_DB_USER = ypekatoros

install:
		poetry install

migrate:
		poetry run python manage.py migrate

setup: migrate
		echo Create a super user
		poetry run python manage.py createsuperuser

build-db: db-drop db-create schema-data-load

collectstatic:
		poetry run python manage.py collectstatic --no-input

db-start:
		sudo service postgresql start

db-status:
		sudo service postgresql status

db-stop:
		sudo service postgresql stop

db-create:
		createdb $(DB_NAME)

db-drop:
		dropdb $(DB_NAME)

db-reset:
	dropdb $(DB_NAME) || true
	createdb $(DB_NAME)

dbs-show:
		psql -l

db-connect:
		psql -d $(DB_NAME)


db-show-log:
		vim /var/log/postgresql/postgresql-14-main.log

db-dump:
		pg_dump -h localhost -d $(DB_NAME) -U $(LOCAL_DB_USER) -W -Ft > db-project.dump

db-railway-update:
		pg_restore -U postgres -h containers-us-west-152.railway.app -p 8050 -W -Ft -d railway db-project.dump

start:
		poetry run python3 manage.py runserver 0.0.0.0:8000

lint:
		poetry run flake8 .

test:
		poetry run coverage run --source='.' manage.py test

transprepare:
		poetry run django-admin makemessages --locale ru --add-location file
		poetry run django-admin makemessages --locale ru --add-location file --domain djangojs

transcompile:
		poetry run django-admin compilemessages

show-active-ports:
		sudo lsof -i -P -n | grep LISTEN
# kill -9 processid - force comand to kill process

.PHONY: install