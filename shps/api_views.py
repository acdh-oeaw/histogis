import coreapi
import coreschema
from dateutil.parser import parse
from django.contrib.gis.geos import Point
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.schemas import AutoSchema
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_gis.pagination import GeoJsonPagination

from .models import TempSpatial, Source
from .filters import TempSpatialListFilter, SourceListFilter
from .api_serializers import TempSpatialSerializer, SourceSerializer, SimpleSerializer


class SimpledResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"


class StandardResultsSetPagination(GeoJsonPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 25


class TempSpatialViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TempSpatial objects to be viewed or edited.
    """

    queryset = TempSpatial.objects.all()
    serializer_class = TempSpatialSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TempSpatialListFilter


class SimpleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for TempSpatial objects (without GIS data-points)
    """

    queryset = TempSpatial.objects.all()
    serializer_class = SimpleSerializer
    pagination_class = SimpledResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TempSpatialListFilter


class SourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TempSpatial objects to be viewed or edited.
    """

    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SourceListFilter


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
                location="query",
                schema=coreschema.String(
                    description="Defaults to 1 due to performance reasons."
                ),
            ),
            coreapi.Field(
                "lat",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Latitude of the place to query for."
                ),
            ),
            coreapi.Field(
                name="lng",
                required=True,
                location="query",
                schema=coreschema.String(
                    description="Longitude of the place to query for."
                ),
            ),
            coreapi.Field(
                "when",
                required=False,
                location="query",
                schema=coreschema.String(
                    description="Date the TempSpatial temporal extent has to contain."
                ),
            ),
        ]
    )

    def get_queryset(self):
        lat = self.request.query_params.get("lat", None)
        lng = self.request.query_params.get("lng", None)
        try:
            pnt = Point(float(lng), float(lat))
            print("good")
        except TypeError:
            return []
        qs = TempSpatial.objects.filter(geom__contains=pnt)
        when = self.request.query_params.get("when", None)
        if when is not None:
            try:
                when = parse(when)
            except ValueError:
                when = None
            if when:
                qs = qs.filter(temp_extent__contains=when)
        return qs.order_by("spatial_extent")
