from django.conf.urls import url
from django.urls import path
from . import views
from . import dal_views
from .models import SkosLabel, SkosConcept, SkosConceptScheme

app_name = 'vocabs'

urlpatterns = [
    url(
        r'^skoslabel-autocomplete/$', dal_views.SkosLabelAC.as_view(
            model=SkosLabel, create_field='label',),
        name='skoslabel-autocomplete',
    ),
    url(
        r'^skosconceptscheme-autocomplete/$', dal_views.SkosConceptSchemeAC.as_view(
            model=SkosConceptScheme,
            create_field='dc_title',),
        name='skosconceptscheme-autocomplete',
    ),
    url(
        r'^skosconcept-autocomplete/$', dal_views.SpecificConcepts.as_view(
            model=SkosConcept,
            create_field='pref_label',),
        name='skosconcept-autocomplete',
    ),
    url(
        r'^skosconcept-pref-label-autocomplete/$',
        dal_views.SkosConceptPrefLabalAC.as_view(),
        name='skosconcept-label-ac',
    ),
    url(
        r'^skos-constraint-ac/$', dal_views.SKOSConstraintAC.as_view(model=SkosConcept),
        name='skos-constraint-ac',
    ),
    url(
        r'^skos-constraint-no-hierarchy-ac/$', dal_views.SKOSConstraintACNoHierarchy.as_view(
            model=SkosConcept),
        name='skos-constraint-no-hierarchy-ac',
    ),
    path(
        r'specific-concept-ac/<str:scheme>', dal_views.SpecificConcepts.as_view(
            model=SkosConcept),
        name='specific-concept-ac',
    )
]
