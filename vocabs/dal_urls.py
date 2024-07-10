from django.urls import path
from . import dal_views
from .models import SkosLabel, SkosConcept, SkosConceptScheme

app_name = "vocabs"

urlpatterns = [
    path(
        "skoslabel-autocomplete/",
        dal_views.SkosLabelAC.as_view(
            model=SkosLabel,
            create_field="label",
        ),
        name="skoslabel-autocomplete",
    ),
    path(
        "skosconceptscheme-autocomplete/",
        dal_views.SkosConceptSchemeAC.as_view(
            model=SkosConceptScheme,
            create_field="dc_title",
        ),
        name="skosconceptscheme-autocomplete",
    ),
    path(
        "skosconcept-autocomplete/",
        dal_views.SpecificConcepts.as_view(
            model=SkosConcept,
            create_field="pref_label",
        ),
        name="skosconcept-autocomplete",
    ),
    path(
        "skosconcept-pref-label-autocomplete/",
        dal_views.SkosConceptPrefLabalAC.as_view(),
        name="skosconcept-label-ac",
    ),
    path(
        "skos-constraint-ac/",
        dal_views.SKOSConstraintAC.as_view(model=SkosConcept),
        name="skos-constraint-ac",
    ),
    path(
        "skos-constraint-no-hierarchy-ac/",
        dal_views.SKOSConstraintACNoHierarchy.as_view(model=SkosConcept),
        name="skos-constraint-no-hierarchy-ac",
    ),
    path(
        r"specific-concept-ac/<str:scheme>",
        dal_views.SpecificConcepts.as_view(model=SkosConcept),
        name="specific-concept-ac",
    ),
]
