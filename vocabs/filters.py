import django_filters
from dal import autocomplete
from .models import SkosConcept, SkosConceptScheme, get_all_children, SkosLabel


django_filters.filters.LOOKUP_TYPES = [
    ('', '---------'),
    ('exact', 'Is equal to'),
    ('iexact', 'Is equal to (case insensitive)'),
    ('not_exact', 'Is not equal to'),
    ('lt', 'Lesser than/before'),
    ('gt', 'Greater than/after'),
    ('gte', 'Greater than or equal to'),
    ('lte', 'Lesser than or equal to'),
    ('startswith', 'Starts with'),
    ('endswith', 'Ends with'),
    ('contains', 'Contains'),
    ('icontains', 'Contains (case insensitive)'),
    ('not_contains', 'Does not contain'),
]


def generous_concept_filter(queryset, name, value):
    """ call this function through "method=generous_concept_filter" """
    if value:
        lookup = '__'.join([name, 'in'])
        print("name: {}".format(name))
        print("value: {}".format(value))
        starter = value[0]
        all = get_all_children(starter, include_self=True)
        print("all :{}".format(all))
        qs = queryset.filter(**{lookup: all})
        return qs
    return queryset


class SkosConceptListFilter(django_filters.FilterSet):

    pref_label = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.Select2Multiple(url='vocabs-ac:skosconcept-autocomplete'),
        queryset=SkosConcept.objects.all(),
        lookup_expr='icontains',
        label='PrefLabel',
        help_text=False,
    )

    scheme = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConceptScheme.objects.all(),
        lookup_expr='icontains',
        label='in SkosConceptScheme',
        help_text=False,
    )

    class Meta:
        model = SkosConcept
        fields = '__all__'


class SkosConceptFilter(django_filters.FilterSet):

    pref_label = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.Select2Multiple(url='vocabs-ac:skosconcept-autocomplete'),
        queryset=SkosConcept.objects.all(),
        lookup_expr='icontains',
        label='PrefLabel',
        help_text=False,
    )

    scheme = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConceptScheme.objects.all(),
        lookup_expr='icontains',
        label='in SkosConceptScheme',
        help_text=False,
    )

    class Meta:
        model = SkosConcept
        fields = '__all__'


class SkosConceptSchemeListFilter(django_filters.FilterSet):

    dc_title = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=SkosConceptScheme._meta.get_field('dc_title').help_text,
        label=SkosConceptScheme._meta.get_field('dc_title').verbose_name
        )
    dct_creator = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=SkosConceptScheme._meta.get_field('dct_creator').help_text,
        label=SkosConceptScheme._meta.get_field('dct_creator').verbose_name
        )

    class Meta:
        model = SkosConceptScheme
        fields = '__all__'


class SkosLabelListFilter(django_filters.FilterSet):

    label = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=SkosLabel._meta.get_field('label').help_text,
        label=SkosLabel._meta.get_field('label').verbose_name
        )

    class Meta:
        model = SkosLabel
        fields = '__all__'
