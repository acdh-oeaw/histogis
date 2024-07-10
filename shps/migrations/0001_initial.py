# Generated by Django 5.0.7 on 2024-07-10 14:40

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.ranges
import django.db.models.deletion
import shps.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("idprovider", "0001_initial"),
        ("vocabs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the source",
                        max_length=255,
                        verbose_name="Name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Some verbose description of the source",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "quote",
                    models.TextField(
                        blank=True,
                        help_text="How to quote.",
                        null=True,
                        verbose_name="Quote",
                    ),
                ),
                (
                    "original_url",
                    models.TextField(
                        blank=True,
                        help_text="URLs from where the data was downloaded, use '; ' as separator",
                        null=True,
                        verbose_name="URLs",
                    ),
                ),
                (
                    "upload",
                    models.FileField(
                        blank=True,
                        help_text="A shape file following the HistoGIS data convention",
                        max_length=250,
                        storage=shps.models.OverwriteStorage(),
                        upload_to="data/",
                        verbose_name="A zipped ESRI Shape File",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="TempSpatial",
            fields=[
                (
                    "idprovider_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="idprovider.idprovider",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Usually the object's contemporary name",
                        max_length=250,
                        verbose_name="Name",
                    ),
                ),
                (
                    "alt_name",
                    models.CharField(
                        blank=True,
                        help_text="Alternative Names, use '; ' as separator in case of more names",
                        max_length=500,
                        verbose_name="Alternative Names",
                    ),
                ),
                (
                    "wikidata_id",
                    models.CharField(
                        blank=True,
                        help_text="The ID of a wiki data entry which can be         reasonable associated with the current object.",
                        max_length=500,
                        verbose_name="Wikidata ID",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        help_text="Earliest date this entity captures",
                        verbose_name="Start Date.",
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        help_text="Latest date this entity captures",
                        verbose_name="End Date.",
                    ),
                ),
                (
                    "date_accuracy",
                    models.CharField(
                        choices=[("Y", "Year"), ("YM", "Month"), ("DMY", "Day")],
                        default="Y",
                        help_text="The value indicates if the date is accurate per YEAR, MONTH or DAY",
                        max_length=3,
                        verbose_name="How accurate is the given date",
                    ),
                ),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                (
                    "orig_id",
                    models.CharField(
                        blank=True,
                        help_text="The ID of this object from the dataset used to import this data.",
                        max_length=255,
                        null=True,
                        verbose_name="Any legacy Identifier",
                    ),
                ),
                (
                    "quality",
                    models.CharField(
                        choices=[
                            ("red", "red"),
                            ("yellow", "yellow"),
                            ("green", "green"),
                        ],
                        default="yellow",
                        help_text="An estimation of the HistoGis Team upon the quality of this dataset",
                        max_length=25,
                        null=True,
                        verbose_name="Quality of this dataset",
                    ),
                ),
                (
                    "additional_data",
                    models.JSONField(
                        blank=True,
                        help_text="Additional data provided from the object's source.",
                        null=True,
                        verbose_name="Additional data",
                    ),
                ),
                (
                    "unique",
                    models.CharField(
                        blank=True, max_length=300, null=True, unique=True
                    ),
                ),
                (
                    "centroid",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True,
                        help_text="The object's centroid",
                        null=True,
                        srid=4326,
                        verbose_name="Centroid",
                    ),
                ),
                (
                    "temp_extent",
                    django.contrib.postgres.fields.ranges.DateRangeField(
                        blank=True,
                        help_text="The objects temporal extent (Start and end date)",
                        null=True,
                        verbose_name="Temporal Extent",
                    ),
                ),
                (
                    "spatial_extent",
                    models.FloatField(
                        blank=True,
                        help_text="Saves the area of the object",
                        null=True,
                        verbose_name="Spatial Extent",
                    ),
                ),
                (
                    "administrative_unit",
                    models.ForeignKey(
                        blank=True,
                        help_text="A contemporary name of the administrative unit.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="adm_unit",
                        to="vocabs.skosconcept",
                        verbose_name="Contemporary Administrative Unit",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        help_text="The source of this data.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="source_of",
                        to="shps.source",
                        verbose_name="Source",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
            bases=("idprovider.idprovider",),
        ),
        migrations.CreateModel(
            name="TempStatialRel",
            fields=[
                (
                    "idprovider_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="idprovider.idprovider",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        help_text="Earliest date this relation captures",
                        verbose_name="Start Date.",
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        help_text="Latest date this relation captures",
                        verbose_name="End Date.",
                    ),
                ),
                (
                    "date_accuracy",
                    models.CharField(
                        choices=[("Y", "Year"), ("YM", "Month"), ("DMY", "Day")],
                        default="Y",
                        max_length=3,
                        verbose_name="Date Accuracy",
                    ),
                ),
                (
                    "instance_a",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="related_instance_a",
                        to="shps.tempspatial",
                    ),
                ),
                (
                    "instance_b",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="related_instance_b",
                        to="shps.tempspatial",
                    ),
                ),
                (
                    "relation_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tmp_spatial_rel_relation",
                        to="vocabs.skosconcept",
                    ),
                ),
            ],
            bases=("idprovider.idprovider",),
        ),
    ]
