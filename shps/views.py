import json
import geopandas as gp
import pandas as pd
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from shapely import wkt
from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from .models import TempSpatial, Source
from .tables import TempSpatialTable, SourceTable
from .filters import TempSpatialListFilter, SourceListFilter
from .forms import (
    WhereWasForm,
    TempSpatialFilterFormHelper,
    TempSpatialForm,
    SourceFilterFormHelper,
    SourceForm,
)


class PermaLinkView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        shp = get_object_or_404(TempSpatial, unique=kwargs["unique"])
        url = shp.get_absolute_url()
        return url


class WhereWas(FormView):
    template_name = "shps/where_was.html"
    form_class = WhereWasForm
    success_url = "."

    def form_valid(self, form, **kwargs):
        context = super(WhereWas, self).get_context_data(**kwargs)
        cd = form.cleaned_data
        pnt = Point(cd["lng"], cd["lat"])
        qs = TempSpatial.objects.filter(geom__contains=pnt)
        when = cd["when"]
        if when is not None:
            qs = qs.filter(temp_extent__contains=when)
        else:
            qs = qs
        if qs:
            context["answer"] = qs.order_by("spatial_extent")
        else:
            context["answer"] = ["No Match"]
        context["point"] = pnt
        return render(self.request, self.template_name, context)


class TempSpatialListView(GenericListView):
    model = TempSpatial
    table_class = TempSpatialTable
    filter_class = TempSpatialListFilter
    formhelper_class = TempSpatialFilterFormHelper
    init_columns = [
        "id",
        "name",
        "administrative_unit",
        "start_date",
        "end_date",
    ]

    def get_context_data(self, **kwargs):
        context = super(TempSpatialListView, self).get_context_data()
        context["shapes"] = True
        return context

    def render_to_response(self, context, **kwargs):
        if self.request.GET.get("dl-geojson", None):
            df = pd.DataFrame(list(self.get_queryset().values()))
            df["geometry"] = df.apply(lambda row: wkt.loads(row["geom"].wkt), axis=1)
            str_df = df.astype("str").drop(["geom"], axis=1)
            gdf = gp.GeoDataFrame(str_df)
            gdf["geometry"] = gdf.apply(lambda row: wkt.loads(row["geometry"]), axis=1)
            response = HttpResponse(gdf.to_json(), content_type="application/json")
            response["Content-Disposition"] = 'attachment; filename="out.geojson"'
            return response
        else:
            response = super(TempSpatialListView, self).render_to_response(context)
            return response


class TempSpatialDetailView(DetailView):
    model = TempSpatial
    template_name = "shps/shape_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TempSpatialDetailView, self).get_context_data()
        context["more"] = json.loads(self.object.additional_data)
        try:
            project_url = settings.BASE_URL
        except AttributeError:
            project_url = "https//provide/a/base-url"
        context["project_url"] = project_url
        return context


class TempSpatialCreate(BaseCreateView):
    model = TempSpatial
    form_class = TempSpatialForm
    template_name = "shps/generic_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialCreate, self).dispatch(*args, **kwargs)


class TempSpatialUpdate(BaseUpdateView):
    model = TempSpatial
    form_class = TempSpatialForm
    template_name = "shps/generic_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialUpdate, self).dispatch(*args, **kwargs)


class TempSpatialDelete(DeleteView):
    model = TempSpatial
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("shapes:browse_shapes")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialDelete, self).dispatch(*args, **kwargs)


class SourceListView(GenericListView):
    model = Source
    table_class = SourceTable
    filter_class = SourceListFilter
    formhelper_class = SourceFilterFormHelper
    init_columns = [
        "id",
        "name",
        "part_of",
    ]


class SourceDetailView(DetailView):
    model = Source
    template_name = "shps/source_detail.html"


class SourceCreate(BaseCreateView):
    model = Source
    form_class = SourceForm
    template_name = "shps/generic_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SourceCreate, self).dispatch(*args, **kwargs)


class SourceUpdate(BaseUpdateView):
    model = Source
    form_class = SourceForm
    template_name = "shps/generic_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SourceUpdate, self).dispatch(*args, **kwargs)


class SourceDelete(DeleteView):
    model = Source
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("shapes:browse_sources")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SourceDelete, self).dispatch(*args, **kwargs)
