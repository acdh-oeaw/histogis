import django_filters

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


class TempSpatialListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=TempSpatial._meta.get_field('name').help_text,
        label=TempSpatial._meta.get_field('name').verbose_name
        )

    class Meta:
        model = TempSpatial
        exclude = ['geom']
