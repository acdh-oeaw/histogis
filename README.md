# HistoGIS

## About

HistoGIS is a Geographical Information System, workbench and repository to retrieve, collect, create, enrich and preserve historical temporalized spatial data sets.
HistoGIS is based upon django, geodjango and [djangobaseproject](https://github.com/acdh-oeaw/djangobaseproject)


## Install

1. Download or clone this repository.
2. Adapt the information in `webpage/metadata.py` according to your needs.
3. Create and activate a virtual environment and run `pip install -r requirements.txt`.

## First steps

This project uses modularized settings (to keep sensitive information out of version control or to be able to use the same code for development and production). Therefore you'll have to append a `--settings` parameter pointing to the settings file you'd like to run the code with to all `manage.py` commands.

For development just append `--settings={nameOfYouProject}.settings.dev` to the following commands, e.g. `python manage.py makemigrations --settings=histogis.settings.dev`.

6. Run `makemigrations`, `migrate`, and `runserver` and check [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Jupyter notebook

In case you want to use [Jupyter Notebook and Django-Extensions](https://andrewbrookins.com/python/using-ipython-notebook-with-django/) use the `requirements_dev.txt` for your virtual environment.

## Tests

Install required packages

    pip install -r requirements_test.txt

Run tests

    python manage.py test --settings=histogis.settings.test

After running the test a HTML coverage report will be available at cover/index.html
