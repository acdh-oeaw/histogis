# Generated by Django 2.0.5 on 2018-06-08 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempspatial',
            name='orig_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]