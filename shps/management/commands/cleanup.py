from django.core.management.base import BaseCommand

from shps.models import Source
from vocabs.models import SkosConcept


class Command(BaseCommand):

    help = """Removes objects without relations (Sources and ADMs)"""

    def handle(self, *args, **options):
        no_shps = Source.objects.filter(source_of=None)
        print(f"found {no_shps.count()} Sources without shapes")
        no_shps.delete()
        print("deleted Sources without shapes")
        print("delete not used SkosConcepts")
        no_shps = SkosConcept.objects.filter(adm_unit=None).filter(
            narrower_concepts=None
        )
        print(f"found {no_shps.count()} Vocabs without shapes and children")
        no_shps.delete()
        print("done")
        return "done"
