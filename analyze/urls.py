from django.urls import path
from . import views

app_name = "analyze"

urlpatterns = [
    path("tempspatials/", views.AnalyzeView.as_view(), name="tempspatials_analyze"),
    path("data/", views.get_datatables_data, name="get_data"),
]
