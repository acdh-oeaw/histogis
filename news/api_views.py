import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, filters
from .serializers import NewsFeedSerializer, UserSerializer
from .models import NewsFeed
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NewsFeedFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr="icontains"
        )
    body = django_filters.CharFilter(
        lookup_expr="icontains"
        )

    class Meta:
        model = NewsFeed
        fields = [
            'author', 'title', 'body',
        ]


class NewsFeedViewSet(viewsets.ModelViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = NewsFeedFilter
    search_fields = ('title', 'body')
    ordering_fields = ('created', 'updated', 'title')
