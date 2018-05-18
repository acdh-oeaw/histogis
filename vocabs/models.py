import os
from django.db import models
from django.conf import settings
from django.db import models
from django.urls import reverse

from django.utils.text import slugify
from django.utils.functional import cached_property



try:
    DEFAULT_NAMESPACE = settings.VOCABS_SETTINGS['default_nsgg']
except KeyError:
    DEFAULT_NAMESPACE = "http://www.vocabs/provide-some-namespace/"

try:
    DEFAULT_PREFIX = settings.VOCABS_SETTINGS['default_prefix']
except KeyError:
    DEFAULT_PREFIX = "provideSome"

try:
    DEFAULT_LANG = settings.VOCABS_SETTINGS['default_lang']
except KeyError:
    DEFAULT_LANG = "eng"


LABEL_TYPES = (
    ('prefLabel', 'prefLabel'),
    ('altLabel', 'altLabel'),
    ('hiddenLabel', 'hiddenLabel'),
)


class SkosNamespace(models.Model):
    namespace = models.URLField(blank=True, default=DEFAULT_NAMESPACE)
    prefix = models.CharField(max_length=50, blank=True, default=DEFAULT_PREFIX)

    def __str__(self):
        return "{}".format(self.prefix)


class SkosConceptScheme(models.Model):
    dc_title = models.CharField(max_length=300, blank=True)
    namespace = models.ForeignKey(
        SkosNamespace, blank=True, null=True, on_delete=models.SET_NULL
    )
    dct_creator = models.URLField(blank=True)
    legacy_id = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if self.namespace is None:
            temp_namespace, _ = SkosNamespace.objects.get_or_create(
                namespace=DEFAULT_NAMESPACE, prefix=DEFAULT_PREFIX)
            temp_namespace.save()
            self.namespace = temp_namespace
        else:
            pass
        super(SkosConceptScheme, self).save(*args, **kwargs)

    @classmethod
    def get_listview_url(self):
        return reverse('vocabs:browse_schemes')

    @classmethod
    def get_createview_url(self):
        return reverse('vocabs:skosconceptscheme_create')

    def get_absolute_url(self):
        return reverse('vocabs:skosconceptscheme_detail', kwargs={'pk': self.id})

    def get_next(self):
        next = SkosConceptScheme.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = SkosConceptScheme.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return "{}:{}".format(self.namespace, self.dc_title)


class SkosLabel(models.Model):
    label = models.CharField(max_length=100, blank=True, help_text="The entities label or name.")
    label_type = models.CharField(
        max_length=30, blank=True, choices=LABEL_TYPES, help_text="The type of the label.")
    isoCode = models.CharField(
        max_length=3, blank=True, help_text="The ISO 639-3 code for the label's language.")

    @classmethod
    def get_listview_url(self):
        return reverse('vocabs:browse_skoslabels')

    @classmethod
    def get_createview_url(self):
        return reverse('vocabs:skoslabel_create')

    def get_absolute_url(self):
        return reverse('vocabs:skoslabel_detail', kwargs={'pk': self.id})

    def get_next(self):
        next = SkosLabel.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = SkosLabel.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.label_type != "":
            return "{} @{} ({})".format(self.label, self.isoCode, self.label_type)
        else:
            return "{} @{}".format(self.label, self.isoCode)


class SkosConcept(models.Model):
    pref_label = models.CharField(max_length=300, blank=True)
    pref_label_lang = models.CharField(max_length=3, blank=True, default=DEFAULT_LANG)
    scheme = models.ManyToManyField(
        SkosConceptScheme, blank=True, related_name="has_concepts"
    )
    definition = models.TextField(blank=True)
    definition_lang = models.CharField(max_length=3, blank=True, default=DEFAULT_LANG)
    label = models.ManyToManyField(SkosLabel, blank=True)
    notation = models.CharField(max_length=300, blank=True)
    namespace = models.ForeignKey(
        SkosNamespace, blank=True, null=True, on_delete=models.SET_NULL
    )
    broader_concept = models.ForeignKey(
        'SkosConcept', help_text="Broader Term.",
        verbose_name="Broader Term",
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name="narrower_concepts"
    )
    skos_broader = models.ManyToManyField(
        'SkosConcept', blank=True, related_name="narrower"
    )
    skos_narrower = models.ManyToManyField(
        'SkosConcept', blank=True, related_name="broader"
    )
    skos_related = models.ManyToManyField(
        'SkosConcept', blank=True, related_name="related"
    )
    skos_broadmatch = models.ManyToManyField(
        'SkosConcept', blank=True, related_name="broadmatch"
    )
    skos_exactmatch = models.ManyToManyField(
        'SkosConcept', blank=True, related_name="exactmatch"
    )
    skos_closematch = models.ManyToManyField(
        'SkosConcept', blank=True, related_name="closematch"
    )
    legacy_id = models.CharField(max_length=200, blank=True)
    name_reverse = models.CharField(
        max_length=255,
        verbose_name='Name reverse',
        help_text='Inverse relation like: \
        "is sub-class of" vs. "is super-class of".',
        blank=True
    )

    def get_broader(self):
        broader = self.skos_broader.all()
        broader_reverse = SkosConcept.objects.filter(skos_narrower=self)
        all_broader = set(list(broader)+list(broader_reverse))
        return all_broader

    def get_narrower(self):
        narrower = self.skos_narrower.all()
        narrower_reverse = SkosConcept.objects.filter(skos_broader=self)
        all_narrower = set(list(narrower)+list(narrower_reverse))
        return all_narrower

    @property
    def all_schemes(self):
        return ', '.join([x.dc_title for x in self.scheme.all()])

    def save(self, *args, **kwargs):
        if self.notation == "":
            temp_notation = slugify(self.pref_label, allow_unicode=True)
            concepts = len(SkosConcept.objects.filter(notation=temp_notation))
            if concepts < 1:
                self.notation = temp_notation
            else:
                self.notation = "{}-{}".format(temp_notation, concepts)
        else:
            pass

        if self.namespace is None:
            temp_namespace, _ = SkosNamespace.objects.get_or_create(
                namespace=DEFAULT_NAMESPACE, prefix=DEFAULT_PREFIX)
            temp_namespace.save()
            self.namespace = temp_namespace
        else:
            pass
        super(SkosConcept, self).save(*args, **kwargs)

    @cached_property
    def label(self):
        # 'borrowed from https://github.com/sennierer'
        d = self
        res = self.pref_label
        while d.broader_concept:
            res = d.broader_concept.pref_label + ' >> ' + res
            d = d.broader_concept
        return res

    @classmethod
    def get_listview_url(self):
        return reverse('vocabs:browse_vocabs')

    @classmethod
    def get_createview_url(self):
        return reverse('vocabs:skosconcept_create')

    def get_absolute_url(self):
        return reverse('vocabs:skosconcept_detail', kwargs={'pk': self.id})

    def get_next(self):
        next = SkosConcept.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = SkosConcept.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return self.pref_label


def get_all_children(self, include_self=True):
    # many thanks to https://stackoverflow.com/questions/4725343
    r = []
    if include_self:
        r.append(self)
    for c in SkosConcept.objects.filter(broader_concept=self):
        _r = get_all_children(c, include_self=True)
        if 0 < len(_r):
            r.extend(_r)
    return r
