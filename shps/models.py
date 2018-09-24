import os
from django.conf import settings
from django.contrib.gis.db import models
from django.core.files.storage import FileSystemStorage
from django.core.serializers import serialize
from django.urls import reverse

from idprovider.models import IdProvider
from vocabs.models import SkosConcept


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
    original_url = models.TextField(
        blank=True, null=True,
        verbose_name="URLs",
        help_text="URLs from where the data was downloaded, use '; ' as separator"
        )
    upload = models.FileField(
        max_length=250, blank=True,
        verbose_name="A zipped ESRI Shape File",
        help_text="A shape file following the HistoGIS data convention",
        upload_to='data/', storage=OverwriteStorage(),
    )

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse(
            'shapes:source_detail', kwargs={'pk': self.id}
        )

    def delete(self, using=None, keep_parents=False):
        """ Delete the file from disk because Django doesn't do it. Kudos to AlexanderWatzinger"""
        self.upload.delete()
        super(Source, self).delete(using, keep_parents)

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "Source ID: {}".format(self.name)

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

    def get_file_size(self):
        try:
            return "{}".format(self.upload.size)
        except Exception as e:
            return None


class TempSpatial(IdProvider):
    """A class for temporalized spatial objects"""

    name = models.CharField(
         max_length=250, blank=True,
         verbose_name="Name",
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
        on_delete=models.CASCADE
    )
    geom = models.MultiPolygonField(
        blank=True, null=True, srid=4326
    )
    administrative_unit = models.ForeignKey(
        SkosConcept, null=True, related_name="adm_unit",
        on_delete=models.SET_NULL, blank=True,
        verbose_name="Contemporary Administrative Unit",
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

    def fetch_children(self):
        bigger = TempSpatial.objects.filter(geom__within=self.geom).exclude(id=self.id).distinct()
        if bigger:
            tuples = [(x, x.geom.length) for x in bigger]
            sorted = tuples.sort(key=lambda tup: tup[1])
            return [x[0] for x in tuples]
        else:
            return None

    def fetch_parents(self):
        bigger = TempSpatial.objects.filter(geom__contains=self.geom).exclude(id=self.id).distinct()
        if bigger:
            tuples = [(x, x.geom.length) for x in bigger]
            sorted = tuples.sort(key=lambda tup: tup[1], reverse=True)
            return [x[0] for x in tuples]
        else:
            return None

    def print_parents(self):
        hierarchy_string = ""
        hierarchy = self.fetch_parents()
        if hierarchy:
            separator = " >> "
            for x in hierarchy:
                hierarchy_string = hierarchy_string + separator + x.name
            return hierarchy_string[4:]
        else:
            return []

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "TempStatial ID: {}".format(self.id)


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
        verbose_name="Date Accuracy",
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
