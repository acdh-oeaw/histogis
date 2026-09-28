from django.core.management.base import BaseCommand

from shps.to_arche import project_to_arche


class Command(BaseCommand):

    help = """Creates ARCHE metadata RDF"""

    def handle(self, *args, **options):
        dump = project_to_arche().serialize("arche.xml", format="application/rdf+xml")

        return dump
