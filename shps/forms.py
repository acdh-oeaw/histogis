from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup
from leaflet.forms.widgets import LeafletWidget

from .models import TempSpatial


class TempSpatialForm(forms.ModelForm):
    class Meta:
        model = TempSpatial
        fields = "__all__"
        widgets = {
            'geom': LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(TempSpatialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class TempSpatialFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TempSpatialFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'description',
                    css_id="more"
                    ),
                )
            )
