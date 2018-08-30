from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from django_tables2 import RequestConfig

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from .models import *
from .tables import *
from .filters import *
from .forms import *


class WhereWas(FormView):
    template_name = 'shps/where_was.html'
    form_class = WhereWasForm
    success_url = '.'

    def form_valid(self, form, **kwargs):
        context = super(WhereWas, self).get_context_data(**kwargs)
        cd = form.cleaned_data
        pnt = Point(cd['lat'], cd['lng'])
        qs = TempSpatial.objects.filter(geom__contains=pnt)
        if qs:
            context['answer'] = qs
            # context['no_children'] = qs.exclude(has_children__isnull=False)
        else:
            context['answer'] = "No Match"
        context['point'] = pnt
        return render(self.request, self.template_name, context)


class TempSpatialListView(GenericListView):
    model = TempSpatial
    table_class = TempSpatialTable
    filter_class = TempSpatialListFilter
    formhelper_class = TempSpatialFilterFormHelper
    init_columns = [
        'id',
        'name',
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(TempSpatialListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by
        }).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class TempSpatialDetailView(DetailView):
    model = TempSpatial
    template_name = 'shps/shape_detail.html'


class TempSpatialCreate(BaseCreateView):

    model = TempSpatial
    form_class = TempSpatialForm
    template_name = 'shps/generic_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialCreate, self).dispatch(*args, **kwargs)


class TempSpatialUpdate(BaseUpdateView):

    model = TempSpatial
    form_class = TempSpatialForm
    template_name = 'shps/generic_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialUpdate, self).dispatch(*args, **kwargs)


class TempSpatialDelete(DeleteView):
    model = TempSpatial
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('shapes:browse_shapes')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialDelete, self).dispatch(*args, **kwargs)


class SourceListView(GenericListView):
    model = Source
    table_class = SourceTable
    filter_class = SourceListFilter
    formhelper_class = SourceFilterFormHelper
    init_columns = [
        'id',
        'name',
        'part_of',
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(SourceListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by
        }).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class SourceDetailView(DetailView):
    model = Source
    template_name = 'shps/source_detail.html'


class SourceCreate(BaseCreateView):

    model = Source
    form_class = SourceForm
    template_name = 'shps/generic_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SourceCreate, self).dispatch(*args, **kwargs)


class SourceUpdate(BaseUpdateView):

    model = Source
    form_class = SourceForm
    template_name = 'shps/generic_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SourceUpdate, self).dispatch(*args, **kwargs)


class SourceDelete(DeleteView):
    model = Source
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('shapes:browse_sources')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SourceDelete, self).dispatch(*args, **kwargs)
