from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import *
from .models import SkosConcept, SkosConceptScheme, SkosLabel


class GenericFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.add_input(Submit('Filter', 'search'))


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'import'),)


class SkosConceptFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SkosConceptFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'pref_label',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'Advanced search',
                    'scheme',
                    css_id="more"
                    ),
                )
            )


class SkosConceptForm(forms.ModelForm):
    class Meta:
        model = SkosConcept
        fields = "__all__"
        widgets = {
            'label': autocomplete.ModelSelect2Multiple(url='vocabs-ac:skoslabel-autocomplete'),
            'skos_broader': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:skosconcept-autocomplete'),
            'skos_narrower': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:skosconcept-autocomplete'),
            'skos_related': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:skosconcept-autocomplete'),
            'skos_broadmatch': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:skosconcept-autocomplete'),
            'skos_exactmatch': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:skosconcept-autocomplete'),
            'skos_closematch': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:skosconcept-autocomplete'),
            'scheme': autocomplete.ModelSelect2Multiple(
                url='vocabs-ac:skosconceptscheme-autocomplete'
            )
        }

    def __init__(self, *args, **kwargs):
        super(SkosConceptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class SkosConceptSchemeForm(forms.ModelForm):
    class Meta:
        model = SkosConceptScheme
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SkosConceptSchemeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class SkosConceptSchemeFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SkosConceptSchemeFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'dc_title',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'Advanced search',
                    'dct_creator',
                    css_id="more"
                    ),
                )
            )


class SkosLabelForm(forms.ModelForm):
    class Meta:
        model = SkosLabel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SkosLabelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class SkosLabelFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SkosLabelFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
