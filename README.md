# HistoGIS

[![Linting](https://github.com/acdh-oeaw/histogis/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/histogis/actions/workflows/lint.yml)
[![Test](https://github.com/acdh-oeaw/histogis/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/histogis/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/acdh-oeaw/histogis/branch/main/graph/badge.svg?token=YX1FMKTH3M)](https://codecov.io/gh/acdh-oeaw/histogis)

## About

HistoGIS is a Geographical Information System, workbench and repository to retrieve, collect, create, enrich and preserve historical temporalized spatial data sets.
HistoGIS is based upon django, geodjango and [djangobaseproject](https://github.com/acdh-oeaw/djangobaseproject)

## Install

* create a postgres database "histogis" with postgis extension
* expose env-varibles, see `.env`

```shell
uv run manage.py migrate
uv run manage.py runserver
```

## Docker

### building the image

```shell
docker build -t histogis:latest .
```

### running the image

```shell
docker run -it --network="host" --rm --env-file .env histogis:latest
```
