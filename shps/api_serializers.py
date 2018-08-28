from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from . models import TempSpatial, Source


class SourceSerializer(serializers.HyperlinkedModelSerializer):

    """ A class to serialize Source objects as JSON compatible data """

    class Meta:
        model = Source
        fields = (
            'name',
            'description',
            'quote',
            'original_url',
        )


class TempSpatialSerializer(GeoFeatureModelSerializer, serializers.HyperlinkedModelSerializer):
    """ A class to serialize TempSpatial objects as GeoJSON compatible data """

    source_name = serializers.CharField(source='source.name')
    adm_name = serializers.CharField(source='administrative_unit.pref_label')

    class Meta:
        model = TempSpatial
        geo_field = "geom"
        fields = (
            'id',
            'name',
            'alt_name',
            'source',
            'source_name',
            'administrative_unit',
            'adm_name',
            'start_date',
            'end_date',
        )
        auto_bbox = True
