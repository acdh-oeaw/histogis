from django.core.management.base import BaseCommand

from shps.models import Source, TempSpatial
from shps.utils import gsheet_to_df


class Command(BaseCommand):

    help = """updates administrative_division fields according to
    https://docs.google.com/spreadsheets/d/14WNuiB7KnnezWndKJslw-j-EdHRF04CH2M1HqVSmPGg"""

    def handle(self, *args, **options):
        df = gsheet_to_df("14WNuiB7KnnezWndKJslw-j-EdHRF04CH2M1HqVSmPGg")
        for i, row in df.iterrows():
            adm = row["adm"].lower().replace(" ", "")
            source = Source.objects.get(id=row["id"])
            source.administrative_division = adm
            source.save()
            print(f"processing objects related to {source}")
            for x in TempSpatial.objects.filter(source=source):
                x.administrative_division = adm
                x.save()
        print("done")
