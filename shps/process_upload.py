import os
import glob
import shutil
import zipfile
import pandas as pd
from osgeo import ogr

from django.core.files import File
from django.contrib.gis import geos
from django.contrib.gis.geos import fromstr
from django.db import IntegrityError
from django.conf import settings

from vocabs.models import SkosConcept, SkosConceptScheme
from . models import TempSpatial, Source


def delete_and_create(path):
    try:
        shutil.rmtree(os.path.join(settings.BASE_DIR, path), ignore_errors=False)
    except FileNotFoundError:
        pass
    try:
        temp_dir = os.mkdir(os.path.join(settings.BASE_DIR, path))
        temp_dir = os.path.join(settings.BASE_DIR, path)
    except FileExistsError:
        temp_dir = os.path.join(settings.BASE_DIR, path)
    return temp_dir


def unzip_shapes(path_to_zipfile, shape_temp_dir):
    zf = zipfile.ZipFile(path_to_zipfile, 'r')
    extracted = zf.extractall(shape_temp_dir)
    shape_temp_dir = os.path.join(shape_temp_dir, '*.shp')
    shapefiles = [x for x in glob.iglob(shape_temp_dir, recursive=False)]
    return shapefiles


def import_shapes(shapefiles, source):
    adm_scheme, _ = SkosConceptScheme.objects.get_or_create(dc_title="administrative_unit")
    temp_spatial_ids = []
    for x in shapefiles:
        exceptions = []
        f = None
        shape = None
        layer = None
        shape = ogr.Open(x)
        layer = shape.GetLayer(0)
        filename = os.path.basename(x)
        for i in range(layer.GetFeatureCount()):
            feature = None
            items = None
            feature = layer.GetFeature(i)
            items = feature.items()
            geo = feature.geometry()
            wkt = geo.ExportToWkt()
            try:
                mp = geos.MultiPolygon(fromstr(wkt))
            except TypeError:
                mp = wkt
            spat, _ = TempSpatial.objects.get_or_create(
                start_date=pd.to_datetime(items['start_date']),
                end_date=pd.to_datetime(items['end_date']),
                date_accuracy=items['date_acc'],
                geom=mp
            )
            spat.name = items['name']

            try:
                adm, _ = SkosConcept.objects.get_or_create(
                    pref_label=items['adm_type']
                )
            except IntegrityError:
                adm, _ = SkosConcept.objects.get_or_create(
                    pref_label="unknown adm"
                )
            adm.scheme.add(adm_scheme)
            spat.administrative_unit = adm

            if items['name_alt']:
                spat.alt_name = items['name_alt']

            spat.source = source
            spat.save()
            temp_spatial_ids.append(spat.id)
        shape.Release()
    shutil.rmtree('shapes', ignore_errors=False)
    return temp_spatial_ids
