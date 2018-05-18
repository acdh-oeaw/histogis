from django.conf.urls import url
from . import views

app_name = 'shps'

urlpatterns = [
    url(r'^shapes/$', views.TempSpatialListView.as_view(), name='browse_shapes'),
    url(r'^shape/detail/(?P<pk>[0-9]+)$', views.TempSpatialDetailView.as_view(),
        name='shape_detail'),
    url(r'^shape/delete/(?P<pk>[0-9]+)$', views.TempSpatialDelete.as_view(),
        name='shape_delete'),
    url(r'^shape/edit/(?P<pk>[0-9]+)$', views.TempSpatialUpdate.as_view(),
        name='shape_edit'),
    url(r'^shape/create/$', views.TempSpatialCreate.as_view(),
        name='shape_create'),
]
