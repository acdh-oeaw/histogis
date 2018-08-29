import os
import glob
import shutil
import zipfile
import pandas as pd
import geopandas as gp
from osgeo import ogr

from django.core.files import File
from django.contrib.gis import geos
from django.contrib.gis.geos import fromstr
from django.db import IntegrityError
from django.conf import settings

from vocabs.models import SkosConcept, SkosConceptScheme
from . models import TempSpatial, Source


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
        df = gp.read_file(x).to_crs({'proj': 'longlat', 'ellps': 'WGS84', 'datum': 'WGS84'})
        for i, row in df.iterrows():
            if row['geometry'].geom_type == 'MultiPolygon':
                mp = row['geometry'].wkt
            else:
                mp = geos.MultiPolygon(fromstr(row['geometry'].wkt))
            spat, _ = TempSpatial.objects.get_or_create(
                        start_date=row['start_date'],
                        end_date=row['end_date'],
                        date_accuracy=row['date_acc'],
                        geom=mp
                    )
            try:
                adm, _ = SkosConcept.objects.get_or_create(
                    pref_label=row['adm_type']
                )
            except IntegrityError:
                adm, _ = SkosConcept.objects.get_or_create(
                    pref_label="unknown adm"
                )
            adm.scheme.add(adm_scheme)
            spat.administrative_unit = adm
            if row['name']:
                spat.name = row['name']
            if row['name_alt']:
                spat.alt_name = row['name_alt']

            spat.source = source
            spat.save()
            print(spat.id)
            temp_spatial_ids.append(spat.id)
    return temp_spatial_ids
