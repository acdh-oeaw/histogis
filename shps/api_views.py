from rest_framework import generics
from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination
from django_filters import rest_framework
from . models import TempSpatial, Source
from . filters import TempSpatialListFilter
from . api_serializers import TempSpatialSerializer, SourceSerializer
from django.contrib.gis.geos import Point
from dateutil.parser import *
import re


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
    filter_backends = (rest_framework.DjangoFilterBackend, )
    filter_class = TempSpatialListFilter


class SourceViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows TempSpatial objects to be viewed or edited.
    """

    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class TemporalizedSpatialQuery(generics.ListAPIView):

    """
    API endpoint that allows to query TempSpatial objects with long/lat and temp.
    """
    serializer_class = TempSpatialSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        lng = self.request.query_params.get('lng', None)
        lat = self.request.query_params.get('lat', None)
        pnt = Point(float(lng), float(lat))
        qs = TempSpatial.objects.filter(geom__contains=pnt)
        temp_start = self.request.query_params.get('temp_start', None)
        temp_end = self.request.query_params.get('temp_end', None)
        if temp_start is not None:
            if re.match('[0-9]{4}', temp_start):
                temp_start += '-1-1'
            temp_start = parse(temp_start)
            qs = qs.filter(start_date__gte=temp_start)
        if temp_end is not None:
            if re.match('[0-9]{4}', temp_end):
                temp_end += '-12-31'
            temp_end = parse(temp_end)
            qs = qs.filter(end_date__lte=temp_end)
        return qs
