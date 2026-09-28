from browsing.utils import BaseCreateView, BaseUpdateView, GenericListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from .filters import (
    SkosConceptListFilter,
    SkosConceptSchemeListFilter,
    SkosLabelListFilter,
)
from .forms import (
    SkosConceptForm,
    SkosConceptFormHelper,
    SkosConceptSchemeForm,
    SkosConceptSchemeFormHelper,
    SkosLabelForm,
    SkosLabelFormHelper,
)
from .models import SkosConcept, SkosConceptScheme, SkosLabel
from .tables import SkosConceptSchemeTable, SkosConceptTable, SkosLabelTable


class SkosConceptListView(GenericListView):
    model = SkosConcept
    table_class = SkosConceptTable
    filter_class = SkosConceptListFilter
    formhelper_class = SkosConceptFormHelper
    init_columns = [
        "id",
        "pref_label",
        "broader_concept",
    ]


class SkosConceptDetailView(DetailView):
    model = SkosConcept
    template_name = "vocabs/skosconcept_detail.html"


class SkosConceptCreate(BaseCreateView):
    model = SkosConcept
    form_class = SkosConceptForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptUpdate(BaseUpdateView):
    model = SkosConcept
    form_class = SkosConceptForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptDelete(DeleteView):
    model = SkosConcept
    template_name = "vocabs/confirm_delete.html"
    success_url = reverse_lazy("vocabs:browse_vocabs")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


#####################################################
#   ConceptScheme
#####################################################


class SkosConceptSchemeListView(GenericListView):
    model = SkosConceptScheme
    table_class = SkosConceptSchemeTable
    filter_class = SkosConceptSchemeListFilter
    formhelper_class = SkosConceptSchemeFormHelper
    init_columns = [
        "id",
        "dc_title",
    ]


class SkosConceptSchemeDetailView(DetailView):
    model = SkosConceptScheme
    template_name = "vocabs/skosconceptscheme_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["concepts"] = SkosConcept.objects.filter(scheme=self.kwargs.get("pk"))
        return context


class SkosConceptSchemeCreate(BaseCreateView):
    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptSchemeUpdate(BaseUpdateView):
    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptSchemeDelete(DeleteView):
    model = SkosConceptScheme
    template_name = "vocabs/confirm_delete.html"
    success_url = reverse_lazy("vocabs:browse_schemes")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


###################################################
# SkosLabel
###################################################


class SkosLabelListView(GenericListView):
    model = SkosLabel
    table_class = SkosLabelTable
    filter_class = SkosLabelListFilter
    formhelper_class = SkosLabelFormHelper
    init_columns = [
        "id",
        "label",
    ]


class SkosLabelDetailView(DetailView):
    model = SkosLabel
    template_name = "vocabs/skoslabel_detail.html"


class SkosLabelCreate(BaseCreateView):
    model = SkosLabel
    form_class = SkosLabelForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosLabelUpdate(BaseUpdateView):
    model = SkosLabel
    form_class = SkosLabelForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosLabelDelete(DeleteView):
    model = SkosLabel
    template_name = "vocabs/confirm_delete.html"
    success_url = reverse_lazy("vocabs:browse_skoslabels")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
