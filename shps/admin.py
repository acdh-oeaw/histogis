from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import *


admin.site.register(Source, LeafletGeoAdmin)
admin.site.register(TempSpatial, LeafletGeoAdmin)
admin.site.register(TempStatialRel, LeafletGeoAdmin)
