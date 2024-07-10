#!/usr/bin/env bash
# create_fixtures.sh

# make sure you ran `pip install django-fixture-magic` and added `'fixture_magic'` to INSTALLED_APPS
mkdir ./shps/fixtures
touch ./shps/fixtures/dump.json
echo "create fixtures_courtdecission"
python manage.py dump_object shps.tempspatial 9910 11385 > ./shps/fixtures/dump.json

echo "done"