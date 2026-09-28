from django.contrib import admin

from .models import SkosConcept, SkosConceptScheme, SkosLabel, SkosNamespace

admin.site.register(SkosLabel)
admin.site.register(SkosConcept)
admin.site.register(SkosConceptScheme)
admin.site.register(SkosNamespace)
