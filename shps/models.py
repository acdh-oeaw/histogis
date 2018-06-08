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


class Source(models.Model):
    name = models.CharField(max_length=255)
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
    original_url = models.URLField(blank=True, null=True)
    downloaded = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['id']

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

    # def get_absolute_url(self):
    #     return reverse('world:source_detail', kwargs={'pk': self.id})


class TempSpatial(IdProvider):
    """A class for temporalized spatial objects"""

    name = models.CharField(
         max_length=250, verbose_name="The objects name"
    )
    source = models.ForeignKey(
        Source, null=True, blank=True, related_name="source_of",
        verbose_name="Source",
        help_text="The source of this data.",
        on_delete=models.SET_NULL
    )
    part_of = models.ForeignKey(
        'self', related_name='has_children',
        on_delete=models.SET_NULL, null=True, blank=True
        )
    geom = models.MultiPolygonField(blank=True, null=True)
    administrative_unit = models.ForeignKey(
        SkosConcept, null=True, related_name="adm_unit",
        on_delete=models.SET_NULL, blank=True
    )
    orig_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def get_geojson(self):
        geojson = serialize(
            'geojson', TempSpatial.objects.filter(id=self.id),
            geometry_field='geom',
            fields=('name', 'start_date', )
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

    def __str__(self):
        if self.instance_a and self.instance_b and self.relation_type:
            return "{} {} {}".format(
                self.instance_a,
                self.relation_type,
                self.instance_b
            )
        else:
            return "TempStatialRel ID: {}".format(self.id)
