import os
import hashlib
from datetime import datetime

import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, ConjunctiveGraph
from rdflib.namespace import DC, FOAF, RDFS, XSD
from rdflib.namespace import SKOS

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Centroid, GeoHash
from django.contrib.gis.measure import Distance
from django.contrib.postgres.fields import JSONField, DateRangeField
from django.core.files.storage import FileSystemStorage
from django.core.serializers import serialize
from django.urls import reverse
from django.utils.text import slugify

from idprovider.models import IdProvider
from vocabs.models import SkosConcept


ARCHE = Namespace('https://vocabs.acdh.oeaw.ac.at/schema#')
ACDH = Namespace('https://id.acdh.oeaw.ac.at/')

curent_date = datetime.now().strftime('%Y-%m-%d')


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
    wikidata_id = models.CharField(
         max_length=500,  blank=True,
         verbose_name="Wikidata ID",
         help_text="The ID of a wiki data entry which can be\
         reasonable associated with the current object."
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
    additional_data = JSONField(
        verbose_name="Additional data",
        help_text="Additional data provided from the object's source.",
        blank=True, null=True
    )
    unique = models.CharField(
        blank=True, null=True, max_length=300, unique=True
    )
    centroid = models.PointField(
        blank=True, null=True,
        verbose_name="Centroid",
        help_text="The object's centroid"
    )
    temp_extent = DateRangeField(
        blank=True, null=True,
        verbose_name="Temporal Extent",
        help_text="The objects temporal extent (Start and end date)"
    )
    spatial_extent = models.FloatField(
        blank=True, null=True,
        verbose_name="Spatial Extent",
        help_text="Saves the area of the object"
    )

    def alt_name_list(self):
        """
        returns a list of alt names
        :return: a python list of alt names
        """

        return [x.strip() for x in self.alt_name.split(";")]

    def save(self, *args, **kwargs):
        """ customized save function stores
        centroid, a hash, temp_extent and spatial_extent on save
        """
        if self.geom and not self.centroid:
            cent = self.geom.centroid
            self.centroid = cent
        unique_str = "".join([
            str(self.start_date),
            str(self.end_date),
            str(self.geom.wkt),
            str(self.date_accuracy)
        ]).encode('utf-8')
        self.unique = hashlib.md5(unique_str).hexdigest()
        if self.start_date and self.end_date:
            self.temp_extent = (self.start_date, self.end_date)
        self.spatial_extent = self.geom.area
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(e)

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

    def get_arche_url(self):
        return reverse(
            'shapes:shape_arche', kwargs={'pk': self.id}
        )

    def get_json_url(self):
        return reverse(
            'tempspatial-detail', kwargs={'pk': self.id}
        )

    def get_permalink_url(self):
        return reverse(
            'shapes:permalink-view', kwargs={'unique': self.unique}
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

    def fetch_children(self, distance=0):
        """ returns all TempSpatial objects covered spatially by the current object and with\
        overlapping time spans """
        try:
            # lat = self.Lat
            # coef = cos(lat)
            #
            # buffer_width = 360 * distance / (40000.0 * coef)
            # bufferd_poly = self.geom.buffer(buffer_width)
            bigger = TempSpatial.objects.filter(centroid__within=self.geom)\
                .filter(spatial_extent__lte=self.spatial_extent)\
                .filter(temp_extent__overlap=self.temp_extent)\
                .exclude(id=self.id).exclude(name=self.name).distinct().order_by('spatial_extent')
            return bigger
        except Exception as e:
            return ['Looks like there is some error in a child shape', "{}".format(e)]

    def fetch_parents(self, distance=-0):
        """ returns all TempSpatial objects covering spatially the current object and with\
        overlapping time spans """
        try:
            buffer_width = distance / 40000000.0 * 360.0
            bufferd_poly = self.geom.buffer(buffer_width)
            bigger = TempSpatial.objects.filter(geom__covers=self.centroid)\
                .filter(spatial_extent__gte=self.spatial_extent)\
                .filter(temp_extent__overlap=self.temp_extent)\
                .exclude(id=self.id).exclude(name=self.name).distinct().order_by('spatial_extent')
            return bigger
        except Exception as e:
            return ['Looks like there is some error in a parent shape', "{}".format(e)]

    def parents(self, distance=-0):
        return [
            {
                "id": x.id,
                "start_date": x.start_date,
                "end_date": x.end_date,
                "name": x.name,
                "permalink": x.get_permalink_url()
            } for x in self.fetch_parents(distance=distance)
        ]

    def fetch_close_by(self, radius=10):
        point = self.centroid
        close_by = TempSpatial.objects.filter(
            centroid__distance_lt=(point, Distance(km=radius))
        ).exclude(id=self.id).distinct()
        return close_by

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

    def sq_km(self, ct=3035):
        """ returns the size of the spatial extent in square km"""
        self.geom.transform(ct=ct)
        sq_km = self.geom.area / 1000000
        return sq_km

    def slug_name(self):
        return "{}__{}_{}".format(
            slugify(self.name), self.start_date, self.end_date
        )

    def as_arche_res(self):
        quote = self.source.quote
        pandorfer = URIRef("https://d-nb.info/gnd/1043833846")
        mschloegl = URIRef("https://d-nb.info/gnd/1154715620")
        apiechl = URIRef("https://orcid.org/0000-0002-9239-5577")
        adueck = URIRef("https://orcid.org/0000-0003-3392-2610")
        pmarck = URIRef("https://orcid.org/0000-0003-1816-4823")
        veccol = "https://id.acdh.oeaw.ac.at/histogis/vectordata"
        res_uri = URIRef("{}/{}.geojson".format(veccol, self.slug_name()))

        g = rdflib.Graph()
        g.add((res_uri, RDF.type, ARCHE.Resource))
        g.add((res_uri, ARCHE.hasOwner, URIRef('https://d-nb.info/gnd/1123037736')))
        g.add((res_uri, ARCHE.hasRightsHolder, URIRef('https://d-nb.info/gnd/1123037736')))
        g.add((res_uri, ARCHE.hasLicensor, URIRef('https://d-nb.info/gnd/1123037736')))
        g.add((res_uri, ARCHE.hasLicense, URIRef("https://creativecommons.org/licenses/by/4.0/")))
        g.add((res_uri, ARCHE.isPartOf, URIRef(veccol)))
        g.add((res_uri, ARCHE.hasTitle, Literal(
            "{} ({} - {})".format(self.name, self.start_date, self.end_date), lang="de"
        )))
        g.add((res_uri, ARCHE.hasCoverageStartDate, Literal(self.start_date, datatype=XSD.date)))
        g.add((res_uri, ARCHE.hasCoverageEndDate, Literal(self.end_date, datatype=XSD.date)))
        g.add((res_uri, ARCHE.hasContributor, pandorfer))
        g.add((res_uri, ARCHE.hasContributor, mschloegl))
        if 'Marckhgott' in quote:
            g.add((res_uri, ARCHE.hasCreator, pmarck))
        if 'Piechl' in quote:
            g.add((res_uri, ARCHE.hasCreator, apiechl))
        if 'Dückelmann' in quote:
            g.add((res_uri, ARCHE.hasCreator, adueck))
        g.add((res_uri, ARCHE.hasDescription, Literal(f"{self.source.description}", lang="en")))
        g.add((res_uri, ARCHE.hasAvailableDate, Literal(curent_date, datatype=XSD.date)))
        g.add((res_uri, ARCHE.hasFormat, Literal("application/vnd.geo+json", lang="en")))
        g.add(
            (
                res_uri,
                ARCHE.isPartOf,
                URIRef("https://vocabs.acdh.oeaw.ac.at/archecategory/dataset/geojson")
            )
        )
        return g

    def sanitize_wikidataid(self):
        if self.wikidata_id is not None:
            if self.wikidata_id.startswith('http'):
                return self.wikidata_id
            else:
                return "https://www.wikidata.org/wiki/{}".format(self.wikidata_id)
        else:
            return None

    def __str__(self):
        if self.name:
            return "{} ({} - {})".format(self.name, self.start_date, self.end_date)
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
