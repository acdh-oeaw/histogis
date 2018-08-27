import django_tables2 as tables
from django_tables2.utils import A
from .models import TempSpatial, Source


class TempSpatialTable(tables.Table):
    id = tables.LinkColumn(
        'shapes:shape_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'shapes:shape_detail',
        args=[A('pk')], verbose_name='Name'
    )
    source = tables.Column()
    part_of = tables.Column()
    administrative_unit = tables.Column()

    class Meta:
        model = TempSpatial
        sequence = (
            'id',
            'name',
            'part_of',
        )
        attrs = {"class": "table table-responsive table-hover"}


class SourceTable(tables.Table):
    name = tables.LinkColumn(
        'shapes:source_detail',
        args=[A('pk')], verbose_name='Name'
    )
    administrative_unit = tables.Column()

    class Meta:
        model = Source
        sequence = (
            'id',
            'name',
            'description',
        )
        attrs = {"class": "table table-responsive table-hover"}
