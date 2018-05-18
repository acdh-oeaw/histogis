from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_tables2 import RequestConfig

from webpage.utils import GenericListView, BaseCreateView, BaseUpdateView

from .models import *
from .tables import *
from .filters import *
from .forms import *


class TempSpatialListView(GenericListView):
    model = TempSpatial
    table_class = TempSpatialTable
    filter_class = TempSpatialListFilter
    formhelper_class = TempSpatialFilterFormHelper
    init_columns = [
        'id',
        'name',
        'part_of',
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialListView, self).dispatch(*args, **kwargs)


class TempSpatialDetailView(DetailView):
    model = TempSpatial
    template_name = 'shapes/assignment_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialDetailView, self).dispatch(*args, **kwargs)


class TempSpatialCreate(BaseCreateView):

    model = TempSpatial
    form_class = TempSpatialForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TempSpatialCreate, self).dispatch(*args, **kwargs)


class TempSpatialUpdate(BaseUpdateView):

    model = TempSpatial
    form_class = TempSpatialForm

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
