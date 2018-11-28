from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'shps'

urlpatterns = [
    url(r'^where-was/$', views.WhereWas.as_view(), name='where_was'),
    url(r'^shapes/$', views.TempSpatialListView.as_view(), name='browse_shapes'),
    path('permalink/<unique>/', views.PermaLinkView.as_view(), name='permalink-view'),
    url(r'^shape/detail/(?P<pk>[0-9]+)$', views.TempSpatialDetailView.as_view(),
        name='shape_detail'),
    url(r'^shape/delete/(?P<pk>[0-9]+)$', views.TempSpatialDelete.as_view(),
        name='shape_delete'),
    url(r'^shape/edit/(?P<pk>[0-9]+)$', views.TempSpatialUpdate.as_view(),
        name='shape_edit'),
    url(r'^shape/create/$', views.TempSpatialCreate.as_view(),
        name='shape_create'),
    url(r'^sources/$', views.SourceListView.as_view(), name='browse_sources'),
    url(r'^source/detail/(?P<pk>[0-9]+)$', views.SourceDetailView.as_view(),
        name='source_detail'),
    url(r'^source/delete/(?P<pk>[0-9]+)$', views.SourceDelete.as_view(),
        name='source_delete'),
    url(r'^source/edit/(?P<pk>[0-9]+)$', views.SourceUpdate.as_view(),
        name='source_edit'),
    url(r'^source/create/$', views.SourceCreate.as_view(),
        name='source_create'),
    url(r'^shape/edit/(?P<pk>[0-9]+)$', views.SourceUpdate.as_view(),
        name='source_edit'),
]
