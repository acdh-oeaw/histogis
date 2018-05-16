from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django_tables2 import SingleTableView, RequestConfig
from .models import SkosConcept, SkosConceptScheme, SkosLabel
from .forms import *
from .tables import SkosConceptTable, SkosConceptSchemeTable, SkosLabelTable
from .filters import SkosConceptListFilter, SkosConceptSchemeListFilter, SkosLabelListFilter
from webpage.utils import GenericListView, BaseCreateView, BaseUpdateView


class SkosConceptListView(GenericListView):
    model = SkosConcept
    table_class = SkosConceptTable
    filter_class = SkosConceptListFilter
    formhelper_class = SkosConceptFormHelper
    init_columns = [
        'id',
        'pref_label',
        'broader_concept',
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(SkosConceptListView, self).get_context_data()
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


class SkosConceptDetailView(DetailView):

    model = SkosConcept
    template_name = 'vocabs/skosconcept_detail.html'


class SkosConceptCreate(BaseCreateView):

    model = SkosConcept
    form_class = SkosConceptForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptCreate, self).dispatch(*args, **kwargs)


class SkosConceptUpdate(BaseUpdateView):

    model = SkosConcept
    form_class = SkosConceptForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptUpdate, self).dispatch(*args, **kwargs)


class SkosConceptDelete(DeleteView):
    model = SkosConcept
    template_name = 'vocabs/confirm_delete.html'
    success_url = reverse_lazy('vocabs:browse_vocabs')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptDelete, self).dispatch(*args, **kwargs)


#####################################################
#   ConceptScheme
#####################################################


class SkosConceptSchemeListView(GenericListView):
    model = SkosConceptScheme
    table_class = SkosConceptSchemeTable
    filter_class = SkosConceptSchemeListFilter
    formhelper_class = SkosConceptSchemeFormHelper
    init_columns = [
        'id',
        'dc_title',
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(SkosConceptSchemeListView, self).get_context_data()
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


class SkosConceptSchemeDetailView(DetailView):

    model = SkosConceptScheme
    template_name = 'vocabs/skosconceptscheme_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SkosConceptSchemeDetailView, self).get_context_data(**kwargs)
        context["concepts"] = SkosConcept.objects.filter(scheme=self.kwargs.get('pk'))
        return context


class SkosConceptSchemeCreate(BaseCreateView):

    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptSchemeCreate, self).dispatch(*args, **kwargs)


class SkosConceptSchemeUpdate(BaseUpdateView):

    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptSchemeUpdate, self).dispatch(*args, **kwargs)


class SkosConceptSchemeDelete(DeleteView):
    model = SkosConceptScheme
    template_name = 'vocabs/confirm_delete.html'
    success_url = reverse_lazy('vocabs:browse_schemes')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosConceptSchemeDelete, self).dispatch(*args, **kwargs)


###################################################
# SkosLabel
###################################################


class SkosLabelListView(GenericListView):
    model = SkosLabel
    table_class = SkosLabelTable
    filter_class = SkosLabelListFilter
    formhelper_class = SkosLabelFormHelper
    init_columns = [
        'id',
        'label',
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(SkosLabelListView, self).get_context_data()
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


class SkosLabelDetailView(DetailView):

    model = SkosLabel
    template_name = 'vocabs/skoslabel_detail.html'


class SkosLabelCreate(BaseCreateView):

    model = SkosLabel
    form_class = SkosLabelForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosLabelCreate, self).dispatch(*args, **kwargs)


class SkosLabelUpdate(BaseUpdateView):

    model = SkosLabel
    form_class = SkosLabelForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosLabelUpdate, self).dispatch(*args, **kwargs)


class SkosLabelDelete(DeleteView):
    model = SkosLabel
    template_name = 'vocabs/confirm_delete.html'
    success_url = reverse_lazy('vocabs:browse_skoslabels')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SkosLabelDelete, self).dispatch(*args, **kwargs)
