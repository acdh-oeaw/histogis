from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from vocabs import api_views
from shps import api_views as shps_api_views

router = routers.DefaultRouter()
router.register(r'skoslabels', api_views.SkosLabelViewSet)
router.register(r'skosnamespaces', api_views.SkosNamespaceViewSet)
router.register(r'skosconceptschemes', api_views.SkosConceptSchemeViewSet)
router.register(r'skosconcepts', api_views.SkosConceptViewSet)
router.register(r'tempspatial', shps_api_views.TempSpatialViewSet)
router.register(r'source', shps_api_views.SourceViewSet)
router.register(r'tempspatial-simple', shps_api_views.SimpleViewSet, basename='tempspatial-simple')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/where-was/', shps_api_views.TemporalizedSpatialQuery.as_view()),
    url('api-docs/', include_docs_urls(title='HistoGIS-API')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^charts/', include('charts.urls', namespace='charts')),
    url(r'^vocabs/', include('vocabs.urls', namespace='vocabs')),
    url(r'^vocabs-ac/', include('vocabs.dal_urls', namespace='vocabs-ac')),
    url(r'^', include('webpage.urls', namespace='webpage')),
    url(r'^shapes/', include('shps.urls', namespace='shapes')),
    url(r'^analyze/', include('analyze.urls', namespace='analyze')),
]
