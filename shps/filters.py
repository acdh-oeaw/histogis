import django_filters
from rest_framework_gis.filterset import GeoFilterSet
from django_filters.rest_framework import FilterSet
from rest_framework_gis.filters import GeometryFilter

from .models import TempSpatial, Source


class SourceListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Source._meta.get_field('name').help_text,
        label=Source._meta.get_field('description').verbose_name
        )

    class Meta:
        model = Source
        fields = '__all__'


class TempSpatialListFilter(GeoFilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=TempSpatial._meta.get_field('name').help_text,
        label=TempSpatial._meta.get_field('name').verbose_name
        )
    geom = GeometryFilter(
        name='geom', lookup_expr='contains',
    )

    class Meta:
        model = TempSpatial
        fields = '__all__'
