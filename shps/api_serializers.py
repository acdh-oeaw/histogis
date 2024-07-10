from rest_framework import serializers
from .serializer_base import LinkedPastsSerializer
from .models import TempSpatial, Source


class SimpleSerializer(serializers.HyperlinkedModelSerializer):
    """A class to serialize TempSpatial objects without GIS data points"""

    source_name = serializers.CharField(source="source.name")
    adm_name = serializers.CharField(source="administrative_unit.pref_label")
    spatial_extent_sqm = serializers.ReadOnlyField(source="sq_km")
    slugged_name = serializers.ReadOnlyField(source="slug_name")
    title = serializers.ReadOnlyField(source="name")

    class Meta:
        model = TempSpatial
        fields = (
            "id",
            "url",
            "wikidata_id",
            "title",
            "alt_name",
            "source",
            "source_name",
            "administrative_unit",
            "adm_name",
            "start_date",
            "end_date",
            "date_accuracy",
            "spatial_extent_sqm",
            "slugged_name",
        )


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    """A class to serialize Source objects as JSON compatible data"""

    class Meta:
        model = Source
        fields = (
            "name",
            "description",
            "quote",
            "original_url",
        )


class TempSpatialSerializer(
    LinkedPastsSerializer, serializers.HyperlinkedModelSerializer
):
    """A class to serialize TempSpatial objects as GeoJSON compatible data"""

    source_name = serializers.CharField(source="source.name")
    adm_name = serializers.CharField(source="administrative_unit.pref_label")
    spatial_extent_sqm = serializers.ReadOnlyField(source="sq_km")
    slugged_name = serializers.ReadOnlyField(source="slug_name")
    title = serializers.ReadOnlyField(source="name")

    class Meta:
        model = TempSpatial
        geo_field = "geom"
        fields = (
            "id",
            "wikidata_id",
            "title",
            "name",
            "alt_name",
            "source",
            "source_name",
            "administrative_unit",
            "adm_name",
            "start_date",
            "end_date",
            "date_accuracy",
            "spatial_extent",
            "spatial_extent_sqm",
            "parents",
            "slugged_name",
        )
        auto_bbox = True
