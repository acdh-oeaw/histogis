from rest_framework import serializers
from .models import SkosConcept, SkosConceptScheme, SkosLabel, SkosNamespace


class SkosLabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosLabel
        fields = ('label', 'label_type', 'isoCode')


class SkosNamespaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosNamespace
        fields = ('namespace', 'prefix')


class SkosConceptSchemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosConceptScheme
        fields = ('dc_title', 'namespace', 'dct_creator', 'legacy_id')


class SkosConceptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SkosConcept
        fields = (
            'pref_label', 'pref_label_lang', 'scheme', 'definition', 'definition_lang', 'label',
            'notation', 'skos_broader', 'broader', 'skos_narrower', 'narrower', 'url',
            'skos_exactmatch', 'exactmatch', 'skos_closematch', 'closematch', 'legacy_id'
        )
