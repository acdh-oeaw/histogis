# Generated by Django 5.1.3 on 2024-12-04 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shps", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="source",
            name="administrative_division",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "adm1",
                        "ADM 1: a primary administrative division of a country, such as a state in the United States",
                    ),
                    (
                        "adm2",
                        "ADM 2: a subdivision of a first-order administrative division",
                    ),
                    (
                        "adm3",
                        "ADM 3: a subdivision of a second-order administrative division",
                    ),
                    (
                        "adm4",
                        "ADM 4: a subdivision of a third-order administrative division",
                    ),
                    (
                        "adm5",
                        "ADM 5: a subdivision of a fourth-order administrative division",
                    ),
                ],
                help_text="Mainly used to group objects by similar hierarchy level; (http://www.geonames.org/export/codes.html)",
                max_length=5,
                null=True,
                verbose_name="administrative division",
            ),
        ),
        migrations.AddField(
            model_name="tempspatial",
            name="administrative_division",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "adm1",
                        "ADM 1: a primary administrative division of a country, such as a state in the United States",
                    ),
                    (
                        "adm2",
                        "ADM 2: a subdivision of a first-order administrative division",
                    ),
                    (
                        "adm3",
                        "ADM 3: a subdivision of a second-order administrative division",
                    ),
                    (
                        "adm4",
                        "ADM 4: a subdivision of a third-order administrative division",
                    ),
                    (
                        "adm5",
                        "ADM 5: a subdivision of a fourth-order administrative division",
                    ),
                ],
                help_text="Mainly used to group objects by similar hierarchy level; (http://www.geonames.org/export/codes.html)",
                max_length=5,
                null=True,
                verbose_name="administrative division",
            ),
        ),
    ]