from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from vocabs import api_views
from shps import api_views as shps_api_views

router = routers.DefaultRouter()
router.register(r"skoslabels", api_views.SkosLabelViewSet)
router.register(r"skosnamespaces", api_views.SkosNamespaceViewSet)
router.register(r"skosconceptschemes", api_views.SkosConceptSchemeViewSet)
router.register(r"skosconcepts", api_views.SkosConceptViewSet)
router.register(r"tempspatial", shps_api_views.TempSpatialViewSet)
router.register(r"source", shps_api_views.SourceViewSet)
router.register(
    r"tempspatial-simple", shps_api_views.SimpleViewSet, basename="tempspatial-simple"
)


urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api/where-was/",
        shps_api_views.TemporalizedSpatialQuery.as_view(),
        name="where_was_api",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("vocabs/", include("vocabs.urls", namespace="vocabs")),
    path("vocabs-ac/", include("vocabs.dal_urls", namespace="vocabs-ac")),
    path("", include("webpage.urls", namespace="webpage")),
    path("shapes/", include("shps.urls", namespace="shapes")),
    path("analyze/", include("analyze.urls", namespace="analyze")),
]
