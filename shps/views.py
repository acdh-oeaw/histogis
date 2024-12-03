import json
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

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


class PlotToMapView(TemplateView):
    template_name = "shps/map.html"


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
    paginate_by = 25
    init_columns = [
        "id",
        "name",
        "administrative_unit",
        "start_date",
        "end_date",
    ]
    exclude_columns = [
        "geom",
    ]

    template_name = "shps/shapes_list.html"

    def get_context_data(self, **kwargs):
        context = super(TempSpatialListView, self).get_context_data()
        context["shapes"] = True
        return context


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
    paginate_by = 25
    init_columns = [
        "id",
        "name",
    ]
    template_name = "shps/generic_list.html"


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
