from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination
from . models import TempSpatial, Source
from . api_serializers import TempSpatialSerializer, SourceSerializer


class StandardResultsSetPagination(GeoJsonPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 25


class TempSpatialViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows TempSpatial objects to be viewed or edited.
    """

    queryset = TempSpatial.objects.all()
    serializer_class = TempSpatialSerializer
    pagination_class = StandardResultsSetPagination


class SourceViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows TempSpatial objects to be viewed or edited.
    """

    queryset = Source.objects.all()
    serializer_class = SourceSerializer