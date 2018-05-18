import django_tables2 as tables
from django_tables2.utils import A
from .models import TempSpatial


class TempSpatialTable(tables.Table):
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
