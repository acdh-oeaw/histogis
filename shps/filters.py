import django_filters
from django.db.models import Q
from rest_framework_gis.filters import GeometryFilter

from vocabs.models import SkosConcept
from .models import TempSpatial, Source


class SourceListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=Source._meta.get_field("name").help_text,
        label=Source._meta.get_field("description").verbose_name,
    )

    class Meta:
        model = Source
        exclude = [
            "upload",
        ]


class TempSpatialListFilter(django_filters.FilterSet):
    all_name = django_filters.CharFilter(
        method="all_name_filter",
        label="Name",
        help_text="Fuzzy search in Name and Alternative Name fields",
    )
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text="Fuzzy search (icontains)",
        label=TempSpatial._meta.get_field("name").verbose_name,
    )
    alt_name = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text="Fuzzy search (icontains)",
        label=TempSpatial._meta.get_field("alt_name").verbose_name,
    )
    administrative_unit = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.all(),
        label=TempSpatial._meta.get_field("administrative_unit").verbose_name,
        help_text=TempSpatial._meta.get_field("administrative_unit").help_text,
    )
    source = django_filters.ModelMultipleChoiceFilter(
        queryset=Source.objects.all(),
        label=TempSpatial._meta.get_field("source").verbose_name,
        help_text=TempSpatial._meta.get_field("source").help_text,
    )
    start_date = django_filters.DateFromToRangeFilter(
        label="Start Date", help_text="Start Date not before - not after."
    )
    end_date = django_filters.DateFromToRangeFilter(
        label="End Date", help_text="End Date not before - not after."
    )
    geom = GeometryFilter(
        field_name="geom",
        lookup_expr="contains",
    )

    class Meta:
        model = TempSpatial
        exclude = ["additional_data", "centroid", "temp_extent"]

    def all_name_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(alt_name__icontains=value))
