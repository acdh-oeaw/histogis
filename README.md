# HistoGIS

## About

HistoGIS is a Geographical Information System, workbench and repository to retrieve, collect, create, enrich and preserve historical temporalized spatial data sets.
HistoGIS is based upon django, geodjango and [djangobaseproject](https://github.com/acdh-oeaw/djangobaseproject)


## Install

1. Download or clone this repository.
2. Adapt the information in `webpage/metadata.py` according to your needs.
3. Create and activate a virtual environment and run `pip install -r requirements.txt`.


## useful commands

### cleanup
removes not used vocabs and sources without shapes
```bash
python manage.py cleanup
```

### update administrative divisions
updates administrative_division fields according to [this google spreadsheet](https://docs.google.com/spreadsheets/d/14WNuiB7KnnezWndKJslw-j-EdHRF04CH2M1HqVSmPGg)

```bash
python manage.py update_amd
```


### building the image

`docker build -t histogis:latest .`
`docker build -t histogis:latest --no-cache .`

### running the image

To run the image you should provide an `docker.env` file to pass in needed environment variables; see example `docker.env` in this repo:

```bash
docker run -it --network="host" --rm --env-file .env histogis:latest
```

### or use published image:

`docker run -it -p 8020:8020 --rm --env-file docker.env acdhch/histogis:latest`