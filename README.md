[![DOI](https://zenodo.org/badge/95352230.svg)](https://zenodo.org/badge/latestdoi/95352230)

# Django Base Project

## About

As the name suggests, this is a basic Django project. The idea of this base project is mainly to bootstrap the web application development process through setting up such a Django Base Project which already provides a couple of Django apps providing quite generic functionalities needed for building web application bound to the Digital Humanities Domain.

## Install

1. Download or clone this repository.
2. Rename the root folder of this project `histogis` and the `histogis` folder in your projects root folder to the name chosen for your new project (e.g. to `mynewproject`).
3. In all files in the project directory, rename `histogis` to the name chosen for your new project. (Use `Find and Replace All` feature provided by your code editor.)
4. Adapt the information in `webpage/metadata.py` according to your needs.
5. Create and activate a virtual environment and run `pip install -r requirements.txt`.

## First steps

This project uses modularized settings (to keep sensitive information out of version control or to be able to use the same code for development and production). Therefore you'll have to append a `--settings` parameter pointing to the settings file you'd like to run the code with to all `manage.py` commands.

For development just append `--settings={nameOfYouProject}.settings.dev` to the following commands, e.g. `python manage.py makemigrations --settings=histogis.settings.dev`.

6. Run `makemigrations`, `migrate`, and `runserver` and check [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Jupyter notebook

In case you want to use [Jupyter Notebook and Django-Extensions](https://andrewbrookins.com/python/using-ipython-notebook-with-django/) use the `requirements_dev.txt` for your virtual environment.

## Next steps

Build your custom awesome Web App.

## Tests

Install required packages

    pip install -r requirements_test.txt

Run tests

    python manage.py test --settings=histogis.settings.test

After running the test a HTML coverage report will be available at cover/index.html
