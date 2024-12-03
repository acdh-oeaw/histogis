from django.urls import path
from . import views
from shps.custom_api_views import shapes_geojson

from archeutils import views as arche_views

app_name = "shps"

urlpatterns = [
    path("geojson", shapes_geojson, name="shapes_geojson"),
    path("map", views.PlotToMapView.as_view(), name="map"),
    path("ids", arche_views.get_ids, name="get_ids"),
    path("arche", arche_views.project_as_arche_graph, name="project_as_arche"),
    path("arche-title-img", arche_views.get_title_img, name="arche_title_img"),
    path("where-was/", views.WhereWas.as_view(), name="where_was"),
    path("shapes/", views.TempSpatialListView.as_view(), name="browse_shapes"),
    path("shape/arche/<int:pk>", arche_views.res_as_arche_graph, name="arche_md"),
    path("permalink/<unique>/", views.PermaLinkView.as_view(), name="permalink-view"),
    path(
        "shape/detail/<int:pk>",
        views.TempSpatialDetailView.as_view(),
        name="shape_detail",
    ),
    path(
        "shape/delete/<int:pk>",
        views.TempSpatialDelete.as_view(),
        name="shape_delete",
    ),
    path(
        "shape/edit/<int:pk>",
        views.TempSpatialUpdate.as_view(),
        name="shape_edit",
    ),
    path("shape/create/", views.TempSpatialCreate.as_view(), name="shape_create"),
    path("sources/", views.SourceListView.as_view(), name="browse_sources"),
    path(
        "source/detail/<int:pk>",
        views.SourceDetailView.as_view(),
        name="source_detail",
    ),
    path(
        "source/delete/<int:pk>",
        views.SourceDelete.as_view(),
        name="source_delete",
    ),
    path(
        "source/edit/<int:pk>",
        views.SourceUpdate.as_view(),
        name="source_edit",
    ),
    path("source/create/", views.SourceCreate.as_view(), name="source_create"),
]
