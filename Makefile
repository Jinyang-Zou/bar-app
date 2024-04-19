PROJECT_NAME = bar
PIPENV = pipenv
.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  runserver        : Start Django development server"
	@echo "  migrate          : Apply database migrations"
	@echo "  makemigrations   : Create new database migrations"
	@echo "  createsuperuser  : Create a superuser for the admin"
	@echo "  django_shell     : Start a Django shell"
	@echo "  pipenv_shell     : Start a Pipenv shell"
	@echo "  pipenv_install   : Install dependencies using pipenv"
	@echo "  test             : Run Django project tests"
	@echo "  clean_pipenv     : Remove pipenv virtual environment"
	@echo "  clean_pycache    : Remove Python cache files"
	@echo "  clean            : Remove Python cache files and pipenv virtual environment"
	@echo "  all              : Install dependencies, migrate database, start Django shell"

runserver:
	$(PIPENV) run python manage.py runserver

migrate:
	$(PIPENV) run python manage.py migrate

makemigrations:
	$(PIPENV) run python manage.py makemigrations

createsuperuser:
	$(PIPENV) run python manage.py createsuperuser

django_shell:
	$(PIPENV) run python manage.py shell

pipenv_shell:
	$(PIPENV) shell

pipenv_install:
	$(PIPENV) install

test:
	$(PIPENV) run python manage.py test --pattern="test_*.py"

clean_pipenv:
	$(PIPENV) --rm

clean_pycache:
	find . -type d -name "__pycache__" -exec rm -rf {} +

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/

all: pipenv_install migrate runserver