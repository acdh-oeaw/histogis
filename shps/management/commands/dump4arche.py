from shps.to_arche import project_to_arche

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = """Creates ARCHE metadata RDF"""

    def handle(self, *args, **options):
        dump = project_to_arche().serialize("arche.xml", format="application/rdf+xml")

        return dump
