from django.contrib import admin
from .models import SkosLabel, SkosConcept, SkosConceptScheme, SkosNamespace

admin.site.register(SkosLabel)
admin.site.register(SkosConcept)
admin.site.register(SkosConceptScheme)
admin.site.register(SkosNamespace)
