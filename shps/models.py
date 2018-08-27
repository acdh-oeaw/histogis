from django.urls import reverse
from django.contrib.gis.db import models
from django.core.serializers import serialize
from idprovider.models import IdProvider

from vocabs.models import SkosConcept

DATE_ACCURACY = (
    ('Y', 'Year'),
    ('YM', 'Month'),
    ('DMY', 'Day')
)

QUALITY = (
    ('red', 'red'),
    ('yellow', 'yellow'),
    ('green', 'green'),
)


class Source(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Name",
        help_text="Name of the source")
    description = models.TextField(
        blank=True, null=True,
        verbose_name="Description",
        help_text="Some verbose description of the source"
    )
    quote = models.TextField(
        blank=True, null=True,
        verbose_name="Quote",
        help_text="How to quote."
    )
    original_url = models.URLField(
        blank=True, null=True,
        verbose_name="URL",
        help_text="URL from where the data was downloaded"
        )
    downloaded = models.DateTimeField(
        blank=True, null=True,
        verbose_name="Date of data download",
        help_text="When was the data downloaded"
    )

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse(
            'shapes:source_detail', kwargs={'pk': self.id}
        )

    @classmethod
    def get_listview_url(self):
        return reverse('shapes:browse_sources')

    @classmethod
    def get_createview_url(self):
        return reverse('shapes:source_create')

    def get_next(self):
        next = Source.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Source.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "Source ID: {}".format(self.name)


class TempSpatial(IdProvider):
    """A class for temporalized spatial objects"""

    name = models.CharField(
         max_length=250,
         verbose_name="The objects name",
         help_text="Usually the object's contemporary name",
    )
    alt_name = models.CharField(
         max_length=500,  blank=True,
         verbose_name="Alternative Names",
         help_text="Alternative Names, use '; ' as separator in case of more names"
    )
    start_date = models.DateField(
        verbose_name="Start Date.",
        help_text="Earliest date this entity captures"
    )
    end_date = models.DateField(
        verbose_name="End Date.",
        help_text="Latest date this entity captures"
    )
    date_accuracy = models.CharField(
        verbose_name="How accurate is the given date",
        help_text="The value indicates if the date is accurate per YEAR, MONTH or DAY",
        choices=DATE_ACCURACY, default=DATE_ACCURACY[0][0], max_length=3,
    )
    source = models.ForeignKey(
        Source, null=True, blank=True, related_name="source_of",
        verbose_name="Source",
        help_text="The source of this data.",
        on_delete=models.SET_NULL
    )
    geom = models.MultiPolygonField(
        blank=True, null=True
    )
    administrative_unit = models.ForeignKey(
        SkosConcept, null=True, related_name="adm_unit",
        on_delete=models.SET_NULL, blank=True,
        verbose_name="Contemporary Administraiv unit",
        help_text="A contemporary name of the administrative unit."
    )
    orig_id = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="Any legacy Identifier",
        help_text="The ID of this object from the dataset used to import this data."
    )
    quality = models.CharField(
        verbose_name="Quality of this dataset",
        help_text="An estimation of the HistoGis Team upon the quality of this dataset",
        max_length=25, null=True, choices=QUALITY, default=QUALITY[1][1]
    )

    class Meta:
        ordering = ['id']

    def get_geojson(self):
        geojson = serialize(
            'geojson', TempSpatial.objects.filter(id=self.id),
            geometry_field='geom',
            fields=(
                'name',
            )
        )
        return geojson

    def get_absolute_url(self):
        return reverse(
            'shapes:shape_detail', kwargs={'pk': self.id}
        )

    @classmethod
    def get_listview_url(self):
        return reverse('shapes:browse_shapes')

    @classmethod
    def get_createview_url(self):
        return reverse('shapes:shape_create')

    def get_next(self):
        next = TempSpatial.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = TempSpatial.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def fetch_hierarchy(self):
        return []

    def print_hierarchy(self):
        # hierarchy_string = ""
        # hierarchy = self.fetch_hierarchy()
        # separator = " >> "
        # for x in hierarchy:
        #     hierarchy_string = hierarchy_string + separator + x.name
        # return hierarchy_string[4:]
        return "needs to be implemented"

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "TempStatial ID: {}".format(self.name)


class TempStatialRel(IdProvider):
    """ Describes a temporalized relation between two TempSpatial objects """

    instance_a = models.ForeignKey(
        TempSpatial, null=True,
        related_name='related_instance_a',
        on_delete=models.SET_NULL
    )
    instance_b = models.ForeignKey(
        TempSpatial,
        null=True, related_name='related_instance_b',
        on_delete=models.SET_NULL
    )
    relation_type = models.ForeignKey(
        SkosConcept,
        null=True, related_name="tmp_spatial_rel_relation",
        on_delete=models.SET_NULL
    )
    start_date = models.DateField(
        verbose_name="Start Date.",
        help_text="Earliest date this relation captures"
    )
    end_date = models.DateField(
        verbose_name="End Date.",
        help_text="Latest date this relation captures"
    )
    date_accuracy = models.CharField(
        default="Y", max_length=3, choices=DATE_ACCURACY
    )

    def __str__(self):
        if self.instance_a and self.instance_b and self.relation_type:
            return "{} {} {}".format(
                self.instance_a,
                self.relation_type,
                self.instance_b
            )
        else:
            return "TempStatialRel ID: {}".format(self.id)
