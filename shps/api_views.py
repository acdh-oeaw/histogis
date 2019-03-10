from rest_framework.schemas import AutoSchema
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
import coreapi
import coreschema


class StandardResultsSetPagination(GeoJsonPagination):
    page_size = 1
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
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "page_size",
                required=False,
                location='query',
                schema=coreschema.String(description="Defaults to 1 due to performance reasons.")
            ),
            coreapi.Field(
                "lat",
                required=True,
                location='query',
                schema=coreschema.String(description="Latitude of the place to query for.")
            ),
            coreapi.Field(
                name="lng",
                required=True,
                location='query',
                schema=coreschema.String(description="Longitude of the place to query for.")
            ),
            coreapi.Field(
                "when",
                required=False,
                location='query',
                schema=coreschema.String(
                    description="Date the TempSpatial temporal extent has to contain."
                )
            ),
        ]
    )

    def get_queryset(self):
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        pnt = Point(float(lng), float(lat))
        qs = TempSpatial.objects.filter(geom__contains=pnt)
        when = self.request.query_params.get('when', None)
        if when is not None:
            try:
                when = parse(when)
            except ValueError:
                when = None
            if when:
                qs = qs.filter(temp_extent__contains=when)

        return qs
