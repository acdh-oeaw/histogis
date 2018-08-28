from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup
from leaflet.forms.widgets import LeafletWidget

from . models import TempSpatial, Source
from . process_upload import delete_and_create, import_shapes, unzip_shapes


class WhereWasForm(forms.Form):
    lat = forms.FloatField(required=True)
    lng = forms.FloatField(required=True)
    not_before = forms.DateField(required=False)
    not_after = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(WhereWasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'submit'),)


class SourceForm(forms.ModelForm):
    import_shapes = forms.BooleanField(
        required=False, initial=False,
        label="Import/Update related shapes?",
        help_text="Would you like to import or update the realted shapes?"
    )

    class Meta:
        model = Source
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)

    def save(self, commit=True):
        print("HI from SAVE METHOD")
        instance = super(SourceForm, self).save(commit=True)
        if self.cleaned_data['import_shapes']:
            uploaded_file = instance.upload
            temp_dir = delete_and_create('shapes')
            shapefiles = unzip_shapes(uploaded_file.path, temp_dir)
            print(shapefiles)
            import_shapes(shapefiles, instance)
            print("temp_dir: {}, uploaded_file_path: {}".format(temp_dir, uploaded_file.path))

        return instance


class SourceFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SourceFilterFormHelper, self).__init__(*args, **kwargs)
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
                    'start_date',
                    'end_date',
                    'administrative_unit',
                    'source',
                    css_id="more"
                    ),
                )
            )
