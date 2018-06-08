# Generated by Django 2.0.5 on 2018-06-08 18:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vocabs', '0001_initial'),
        ('idprovider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Some verbose description of the source', null=True, verbose_name='Description')),
                ('quote', models.TextField(blank=True, help_text='How to quote.', null=True, verbose_name='Quote')),
                ('original_url', models.URLField(blank=True, null=True)),
                ('downloaded', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TempSpatial',
            fields=[
                ('idprovider_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='idprovider.IdProvider')),
                ('name', models.CharField(max_length=250, verbose_name='The objects name')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('administrative_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adm_unit', to='vocabs.SkosConcept')),
                ('part_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_children', to='shps.TempSpatial')),
                ('source', models.ForeignKey(blank=True, help_text='The source of this data.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='source_of', to='shps.Source', verbose_name='Source')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=('idprovider.idprovider',),
        ),
        migrations.CreateModel(
            name='TempStatialRel',
            fields=[
                ('idprovider_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='idprovider.IdProvider')),
                ('instance_a', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_instance_a', to='shps.TempSpatial')),
                ('instance_b', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_instance_b', to='shps.TempSpatial')),
                ('relation_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tmp_spatial_rel_relation', to='vocabs.SkosConcept')),
            ],
            bases=('idprovider.idprovider',),
        ),
    ]