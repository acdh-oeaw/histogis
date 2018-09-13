from django.conf.urls import url
from . import views

app_name = 'analyze'

urlpatterns = [
    url(r'^tempspatials/$', views.WorkAnalyze.as_view(), name='tempspatials_analyze'),
    url(r'^data/$', views.get_datatables_data, name='get_data'),
]
