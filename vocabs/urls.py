from django.urls import path
from . import views
from . import import_views

app_name = "vocabs"


urlpatterns = [
    path("", views.SkosConceptListView.as_view(), name="skosconcept_list"),
    path("concepts/browse/", views.SkosConceptListView.as_view(), name="browse_vocabs"),
    path("import/", import_views.import_skos, name="skos_import"),
    path("import-from-csv/", import_views.import_csv, name="skos_csv_import"),
    path(
        "<int:pk>",
        views.SkosConceptDetailView.as_view(),
        name="skosconcept_detail",
    ),
    path("create/", views.SkosConceptCreate.as_view(), name="skosconcept_create"),
    path(
        "update/<int:pk>",
        views.SkosConceptUpdate.as_view(),
        name="skosconcept_update",
    ),
    path(
        "delete/<int:pk>",
        views.SkosConceptDelete.as_view(),
        name="skosconcept_delete",
    ),
    path("scheme/", views.SkosConceptSchemeListView.as_view(), name="browse_schemes"),
    path(
        "scheme/<int:pk>",
        views.SkosConceptSchemeDetailView.as_view(),
        name="skosconceptscheme_detail",
    ),
    path(
        "scheme/create/",
        views.SkosConceptSchemeCreate.as_view(),
        name="skosconceptscheme_create",
    ),
    path(
        "scheme/update/<int:pk>",
        views.SkosConceptSchemeUpdate.as_view(),
        name="skosconceptscheme_update",
    ),
    path(
        "scheme/delete/<int:pk>",
        views.SkosConceptSchemeDelete.as_view(),
        name="skosconceptscheme_delete",
    ),
    path("label/", views.SkosLabelListView.as_view(), name="browse_skoslabels"),
    path(
        "label/<int:pk>",
        views.SkosLabelDetailView.as_view(),
        name="skoslabel_detail",
    ),
    path("label/create/", views.SkosLabelCreate.as_view(), name="skoslabel_create"),
    path(
        "label/update/<int:pk>",
        views.SkosLabelUpdate.as_view(),
        name="skoslabel_update",
    ),
    path(
        "skoslabel/delete/<int:pk>",
        views.SkosLabelDelete.as_view(),
        name="skoslabel_delete",
    ),
]
