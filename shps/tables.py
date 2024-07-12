import django_tables2 as tables
from django_tables2.utils import A
from .models import TempSpatial, Source


class TempSpatialTable(tables.Table):
    id = tables.LinkColumn("shapes:shape_detail", args=[A("pk")], verbose_name="ID")
    name = tables.LinkColumn("shapes:shape_detail", args=[A("pk")], verbose_name="Name")

    class Meta:
        model = TempSpatial
        sequence = (
            "id",
            "name",
        )
        attrs = {"class": "table table-responsive table-hover"}


class SourceTable(tables.Table):
    name = tables.LinkColumn(
        "shapes:source_detail", args=[A("pk")], verbose_name="Name"
    )

    class Meta:
        model = Source
        sequence = (
            "id",
            "name",
            "description",
        )
        attrs = {"class": "table table-responsive table-hover"}
