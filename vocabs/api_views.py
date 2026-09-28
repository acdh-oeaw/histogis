from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework.settings import api_settings

from .api_renderers import RDFRenderer
from .filters import SkosConceptFilter
from .models import SkosConcept, SkosConceptScheme, SkosLabel, SkosNamespace
from .serializers import (
    SkosConceptSchemeSerializer,
    SkosConceptSerializer,
    SkosLabelSerializer,
    SkosNamespaceSerializer,
)


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 10000


class SkosLabelViewSet(viewsets.ModelViewSet):

    queryset = SkosLabel.objects.all()
    serializer_class = SkosLabelSerializer


class SkosNamespaceViewSet(viewsets.ModelViewSet):

    queryset = SkosNamespace.objects.all()
    serializer_class = SkosNamespaceSerializer


class SkosConceptSchemeViewSet(viewsets.ModelViewSet):

    queryset = SkosConceptScheme.objects.all()
    serializer_class = SkosConceptSchemeSerializer


class SkosConceptViewSet(viewsets.ModelViewSet):

    queryset = SkosConcept.objects.all()
    serializer_class = SkosConceptSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SkosConceptFilter
    pagination_class = LargeResultsSetPagination

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (RDFRenderer,)
