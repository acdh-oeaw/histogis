import glob
import os

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_bootstrap5.bootstrap5 import BS5Accordion
from crispy_forms.bootstrap import AccordionGroup

from leaflet.forms.widgets import LeafletWidget

from .models import TempSpatial, Source
from .process_upload import import_shapes, unzip_shapes


class WhereWasForm(forms.Form):
    lat = forms.FloatField(required=True)
    lng = forms.FloatField(required=True)
    when = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(WhereWasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "submit"),
        )


class SourceForm(forms.ModelForm):
    import_shapes = forms.BooleanField(
        required=False,
        initial=False,
        label="Import/Update related shapes?",
        help_text="Would you like to import or update the realted shapes?",
    )

    class Meta:
        model = Source
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )

    def save(self, commit=True):
        # make sure the temp folder is clean
        [os.remove(f) for f in glob.glob(os.path.join(settings.TEMP_DIR, "*.*"))]
        instance = super(SourceForm, self).save(commit=True)
        if self.cleaned_data["import_shapes"]:
            uploaded_file = instance.upload
            temp_dir = settings.TEMP_DIR
            shapefiles = unzip_shapes(uploaded_file.path, temp_dir)
            try:
                import_shapes(shapefiles, instance)
            except Exception as e:
                [
                    os.remove(f)
                    for f in glob.glob(os.path.join(settings.TEMP_DIR, "*.*"))
                ]
                raise ValidationError(e)

            # remove unzipped files
            [os.remove(f) for f in glob.glob(os.path.join(settings.TEMP_DIR, "*.*"))]

        return instance


class SourceFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SourceFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.form_tag = False
        self.layout = Layout(
            BS5Accordion(
                AccordionGroup(
                    "Basic Search",
                    "name",
                    "administrative_division",
                    css_id="basic_search_fields",
                ),
                AccordionGroup(
                    "Advanced search",
                    "description",
                    css_id="extended",
                ),
                always_open=True,
            ),
        )


class TempSpatialForm(forms.ModelForm):
    class Meta:
        model = TempSpatial
        fields = "__all__"
        widgets = {
            "geom": LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(TempSpatialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class TempSpatialFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TempSpatialFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.form_tag = False
        self.layout = Layout(
            BS5Accordion(
                AccordionGroup(
                    "Basic Search",
                    "all_name",
                    "name",
                    "alt_name",
                    "administrative_division",
                    "in_between",
                    css_id="basic_search_fields",
                ),
                AccordionGroup(
                    "Advanced search",
                    "start_date",
                    "end_date",
                    "administrative_unit",
                    "source",
                    css_id="extended",
                ),
                always_open=True,
            )
        )
