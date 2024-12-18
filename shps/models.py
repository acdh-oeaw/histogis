import os
import hashlib
from datetime import datetime

from rdflib import Namespace
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import DateRangeField
from django.core.files.storage import FileSystemStorage
from django.core.serializers import serialize
from django.urls import reverse
from django.utils.text import slugify
from next_prev import next_in_order, prev_in_order

from idprovider.models import IdProvider
from vocabs.models import SkosConcept


ARCHE = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
ACDH = Namespace("https://id.acdh.oeaw.ac.at/")
ADM_CHOICES = (
    (
        "adm1",
        "ADM 1: a primary administrative division of a country, such as a state in the United States",
    ),
    ("adm2", "ADM 2: a subdivision of a first-order administrative division"),
    ("adm3", "ADM 3: a subdivision of a second-order administrative division"),
    ("adm4", "ADM 4: a subdivision of a third-order administrative division"),
    ("adm5", "ADM 5: a subdivision of a fourth-order administrative division"),
)

curent_date = datetime.now().strftime("%Y-%m-%d")


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


DATE_ACCURACY = (("Y", "Year"), ("YM", "Month"), ("DMY", "Day"))

QUALITY = (
    ("red", "red"),
    ("yellow", "yellow"),
    ("green", "green"),
)


class Source(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Name", help_text="Name of the source"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Some verbose description of the source",
    )
    quote = models.TextField(
        blank=True, null=True, verbose_name="Quote", help_text="How to quote."
    )
    administrative_division = models.CharField(
        blank=True,
        null=True,
        choices=ADM_CHOICES,
        max_length=5,
        verbose_name="administrative division",
        help_text="Mainly used to group objects by similar hierarchy level; (http://www.geonames.org/export/codes.html)",
    )
    original_url = models.TextField(
        blank=True,
        null=True,
        verbose_name="URLs",
        help_text="URLs from where the data was downloaded, use '; ' as separator",
    )
    upload = models.FileField(
        max_length=250,
        blank=True,
        verbose_name="A zipped ESRI Shape File",
        help_text="A shape file following the HistoGIS data convention",
        upload_to="data/",
        storage=OverwriteStorage(),
    )

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("shapes:source_detail", kwargs={"pk": self.id})

    def delete(self, using=None, keep_parents=False):
        """Delete the file from disk because Django doesn't do it. Kudos to AlexanderWatzinger"""
        self.upload.delete()
        super(Source, self).delete(using, keep_parents)

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "Source ID: {}".format(self.name)

    @classmethod
    def get_listview_url(self):
        return reverse("shapes:browse_sources")

    @classmethod
    def get_createview_url(self):
        return reverse("shapes:source_create")

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.id
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.id
        return False

    def get_file_size(self):
        try:
            return "{}".format(self.upload.size)
        except:  # noqa: E722
            return None

    @property
    def end_date(self):
        try:
            return f"{self.source_of.all().order_by('end_date').last().end_date}"
        except AttributeError:
            return None

    @property
    def start_date(self):
        try:
            return f"{self.source_of.all().order_by('start_date').last().start_date}"
        except AttributeError:
            return None

    def slug_name(self):
        return "{}__{}_{}".format(slugify(self.name), self.start_date, self.end_date)


class TempSpatial(IdProvider):
    """A class for temporalized spatial objects"""

    name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Name",
        help_text="Usually the object's contemporary name",
    )
    alt_name = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Alternative Names",
        help_text="Alternative Names, use '; ' as separator in case of more names",
    )
    administrative_division = models.CharField(
        blank=True,
        null=True,
        choices=ADM_CHOICES,
        max_length=5,
        verbose_name="administrative division",
        help_text="Mainly used to group objects by similar hierarchy level; (http://www.geonames.org/export/codes.html)",
    )
    wikidata_id = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Wikidata ID",
        help_text="The ID of a wiki data entry which can be\
         reasonable associated with the current object.",
    )
    start_date = models.DateField(
        verbose_name="Start Date.", help_text="Earliest date this entity captures"
    )
    end_date = models.DateField(
        verbose_name="End Date.", help_text="Latest date this entity captures"
    )
    date_accuracy = models.CharField(
        verbose_name="How accurate is the given date",
        help_text="The value indicates if the date is accurate per YEAR, MONTH or DAY",
        choices=DATE_ACCURACY,
        default=DATE_ACCURACY[0][0],
        max_length=3,
    )
    source = models.ForeignKey(
        Source,
        null=True,
        blank=True,
        related_name="source_of",
        verbose_name="Source",
        help_text="The source of this data.",
        on_delete=models.CASCADE,
    )
    geom = models.MultiPolygonField(blank=True, null=True, srid=4326)
    administrative_unit = models.ForeignKey(
        SkosConcept,
        null=True,
        related_name="adm_unit",
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Contemporary Administrative Unit",
        help_text="A contemporary name of the administrative unit.",
    )
    orig_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Any legacy Identifier",
        help_text="The ID of this object from the dataset used to import this data.",
    )
    quality = models.CharField(
        verbose_name="Quality of this dataset",
        help_text="An estimation of the HistoGis Team upon the quality of this dataset",
        max_length=25,
        null=True,
        choices=QUALITY,
        default=QUALITY[1][1],
    )
    additional_data = models.JSONField(
        verbose_name="Additional data",
        help_text="Additional data provided from the object's source.",
        blank=True,
        null=True,
    )
    unique = models.CharField(blank=True, null=True, max_length=300, unique=True)
    centroid = models.PointField(
        blank=True,
        null=True,
        verbose_name="Centroid",
        help_text="The object's centroid",
    )
    temp_extent = DateRangeField(
        blank=True,
        null=True,
        verbose_name="Temporal Extent",
        help_text="The objects temporal extent (Start and end date)",
    )
    spatial_extent = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Spatial Extent",
        help_text="Saves the area of the object",
    )

    def alt_name_list(self):
        """
        returns a list of alt names
        :return: a python list of alt names
        """

        return [x.strip() for x in self.alt_name.split(";")]

    def save(self, *args, **kwargs):
        """customized save function stores
        centroid, a hash, temp_extent and spatial_extent on save
        """
        if self.geom and not self.centroid:
            cent = self.geom.centroid
            self.centroid = cent
        unique_str = "".join(
            [
                str(self.start_date),
                str(self.end_date),
                str(self.geom.wkt),
                str(self.date_accuracy),
            ]
        ).encode("utf-8")
        self.unique = hashlib.md5(unique_str).hexdigest()
        if self.start_date and self.end_date:
            self.temp_extent = (self.start_date, self.end_date)
        self.spatial_extent = self.geom.area
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(e)

    class Meta:
        ordering = ["id"]

    def get_geojson(self):
        geojson = serialize(
            "geojson",
            TempSpatial.objects.filter(id=self.id),
            geometry_field="geom",
            fields=("name",),
        )
        return geojson

    def get_absolute_url(self):
        return reverse("shapes:shape_detail", kwargs={"pk": self.id})

    def get_arche_url(self):
        return reverse("shapes:arche_md", kwargs={"pk": self.id})

    def get_json_url(self):
        return reverse("tempspatial-detail", kwargs={"pk": self.id})

    def get_permalink_url(self):
        return reverse("shapes:permalink-view", kwargs={"unique": self.unique})

    @classmethod
    def get_listview_url(self):
        return reverse("shapes:browse_shapes")

    @classmethod
    def get_createview_url(self):
        return reverse("shapes:shape_create")

    def get_next(self):
        next = next_in_order(self)
        if next:
            return next.id
        return False

    def get_prev(self):
        prev = prev_in_order(self)
        if prev:
            return prev.id
        return False

    def sq_km(self, ct=3035):
        """returns the size of the spatial extent in square km"""
        self.geom.transform(ct=ct)
        sq_km = self.geom.area / 1000000
        return sq_km

    def slug_name(self):
        return f"{slugify(self.name)}__{self.start_date}_{self.end_date}"

    def sanitize_wikidataid(self):
        if self.wikidata_id is not None:
            if self.wikidata_id.startswith("http"):
                return self.wikidata_id
            else:
                return f"https://www.wikidata.org/wiki/{self.wikidata_id}"
        else:
            return None

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.start_date}–{self.end_date})"
        else:
            return f"TempStatial ID: {self.id}"


class TempStatialRel(IdProvider):
    """Describes a temporalized relation between two TempSpatial objects"""

    instance_a = models.ForeignKey(
        TempSpatial,
        null=True,
        related_name="related_instance_a",
        on_delete=models.SET_NULL,
    )
    instance_b = models.ForeignKey(
        TempSpatial,
        null=True,
        related_name="related_instance_b",
        on_delete=models.SET_NULL,
    )
    relation_type = models.ForeignKey(
        SkosConcept,
        null=True,
        related_name="tmp_spatial_rel_relation",
        on_delete=models.SET_NULL,
    )
    start_date = models.DateField(
        verbose_name="Start Date.", help_text="Earliest date this relation captures"
    )
    end_date = models.DateField(
        verbose_name="End Date.", help_text="Latest date this relation captures"
    )
    date_accuracy = models.CharField(
        verbose_name="Date Accuracy", default="Y", max_length=3, choices=DATE_ACCURACY
    )

    def __str__(self):
        if self.instance_a and self.instance_b and self.relation_type:
            return "{} {} {}".format(
                self.instance_a, self.relation_type, self.instance_b
            )
        else:
            return "TempStatialRel ID: {}".format(self.id)
