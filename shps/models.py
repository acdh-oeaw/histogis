from django.urls import reverse
from django.contrib.gis.db import models
from django.core.serializers import serialize
from idprovider.models import IdProvider

from vocabs.models import SkosConcept


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
        blank=True, null=True, max_length=250, verbose_name="The objects name"
    )
    start_date = models.DateField(
        blank=True, null=True,
        verbose_name="Start Date.",
        help_text="Earliest date this entity captures"
    )
    end_date = models.DateField(
        blank=True, null=True,
        verbose_name="End Date.",
        help_text="Latest date this entity captures"
    )
    source = models.ForeignKey(
        Source, null=True, blank=True, related_name="source_of",
        verbose_name="Source",
        help_text="The source of this data.",
        on_delete=models.SET_NULL
    )
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def get_geojson(self):
        geojson = serialize(
            'geojson', TempSpatial.objects.filter(id=self.id),
            geometry_field='polygon',
            fields=('name', 'start_date', )
        )
        return geojson

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "TempStatial ID: {}".format(self.name)


class TempStatialRel(IdProvider):
    """ Describes a temporalized relation between two TempSpatial objects """

    instance_a = models.ForeignKey(
        TempSpatial, blank=True, null=True,
        related_name='related_instance_a',
        on_delete=models.SET_NULL
    )
    instance_b = models.ForeignKey(
        TempSpatial, blank=True,
        null=True, related_name='related_instance_b',
        on_delete=models.SET_NULL
    )
    relation_type = models.ForeignKey(
        SkosConcept, blank=True,
        null=True, related_name="tmp_spatial_rel_relation",
        on_delete=models.SET_NULL
    )
    start_date = models.DateField(
        blank=True, null=True,
        verbose_name="Start Date.",
        help_text="Earliest date this relation describes"
    )
    end_date = models.DateField(
        blank=True, null=True,
        verbose_name="End Date.",
        help_text="Latest date this relation describes"
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
