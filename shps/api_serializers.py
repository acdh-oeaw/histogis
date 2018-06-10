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
            'downloaded',
        )


class TempSpatialSerializer(GeoFeatureModelSerializer, serializers.HyperlinkedModelSerializer):
    """ A class to serialize TempSpatial objects as GeoJSON compatible data """

    source_name = serializers.CharField(source='source.name')
    adm_name = serializers.CharField(source='administrative_unit.pref_label')
    part_of_name = serializers.CharField(source='part_of.name', default=None)

    class Meta:
        model = TempSpatial
        geo_field = "geom"
        fields = (
            'id',
            'name',
            'source',
            'source_name',
            'part_of',
            'part_of_name',
            'administrative_unit',
            'adm_name',
            'start_date',
            'end_date',
        )
        auto_bbox = True
