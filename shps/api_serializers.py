from rest_framework import serializers
from . serializer_base import LinkedPastsSerializer
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


class TempSpatialSerializer(LinkedPastsSerializer, serializers.HyperlinkedModelSerializer):
    """ A class to serialize TempSpatial objects as GeoJSON compatible data """

    source_name = serializers.CharField(source='source.name')
    adm_name = serializers.CharField(source='administrative_unit.pref_label')
    spatial_extent_sqm = serializers.ReadOnlyField(source="sq_km")
    parents = serializers.ListField("parents")

    class Meta:
        model = TempSpatial
        geo_field = "geom"
        fields = (
            'id',
            'wikidata_id',
            'name',
            'alt_name',
            'source',
            'source_name',
            'administrative_unit',
            'adm_name',
            'start_date',
            'end_date',
            'spatial_extent',
            'spatial_extent_sqm',
            'parents',
        )
        auto_bbox = True
