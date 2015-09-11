# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('short_name', models.CharField(max_length=20, blank=True)),
                ('extra_short_name', models.CharField(max_length=5, blank=True)),
                ('supercompartment', models.PositiveSmallIntegerField(choices=[(1, b'Periphery/Plasma Membrane'), (2, b'Cytoplasmic'), (3, b'Nuclear')])),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('common_name', models.CharField(unique=True, max_length=10)),
                ('sequence', models.CharField(unique=True, max_length=15)),
                ('wormbase_id', models.CharField(unique=True, max_length=15)),
                ('in_paper', models.BooleanField(default=True)),
                ('network_x_coordinate', models.PositiveIntegerField(null=True)),
                ('network_y_coordinate', models.PositiveIntegerField(null=True)),
            ],
            options={
                'ordering': ['common_name'],
            },
        ),
        migrations.CreateModel(
            name='SignalMerged',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('strength', models.PositiveSmallIntegerField(db_index=True, choices=[(0, b'absent'), (1, b'na'), (2, b'weak'), (3, b'present')])),
                ('compartment', models.ForeignKey(to='website.Compartment')),
                ('protein', models.ForeignKey(to='website.Protein')),
            ],
            options={
                'ordering': ['protein', 'compartment', 'timepoint'],
            },
        ),
        migrations.CreateModel(
            name='SignalRaw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('strength', models.PositiveSmallIntegerField(db_index=True, choices=[(0, b'absent'), (1, b'na'), (2, b'weak'), (3, b'present')])),
                ('compartment', models.ForeignKey(to='website.Compartment')),
            ],
            options={
                'ordering': ['video', 'compartment', 'timepoint'],
            },
        ),
        migrations.CreateModel(
            name='Strain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, blank=True)),
                ('genotype', models.CharField(max_length=100, blank=True)),
                ('note', models.CharField(max_length=75, blank=True)),
                ('protein', models.ForeignKey(to='website.Protein')),
            ],
        ),
        migrations.CreateModel(
            name='Timepoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('short_name', models.CharField(max_length=5)),
                ('cell_cycle_category', models.PositiveSmallIntegerField(choices=[(1, b'1-Cell'), (2, b'AB'), (3, b'P1')])),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(unique=True, max_length=30)),
                ('movie_number', models.PositiveSmallIntegerField()),
                ('excel_id', models.PositiveSmallIntegerField(unique=True, null=True)),
                ('date_filmed', models.DateField()),
                ('date_scored', models.DateField(null=True)),
                ('lens', models.CharField(max_length=5, blank=True)),
                ('mode', models.CharField(max_length=70, blank=True)),
                ('summary', models.CharField(max_length=2000, blank=True)),
                ('protein', models.ForeignKey(to='website.Protein')),
                ('strain', models.ForeignKey(to='website.Strain')),
            ],
            options={
                'ordering': ['movie_number'],
            },
        ),
        migrations.AddField(
            model_name='signalraw',
            name='timepoint',
            field=models.ForeignKey(to='website.Timepoint'),
        ),
        migrations.AddField(
            model_name='signalraw',
            name='video',
            field=models.ForeignKey(to='website.Video'),
        ),
        migrations.AddField(
            model_name='signalmerged',
            name='timepoint',
            field=models.ForeignKey(to='website.Timepoint'),
        ),
        migrations.AddField(
            model_name='protein',
            name='representative_video',
            field=models.OneToOneField(related_name='representative', null=True, to='website.Video'),
        ),
        migrations.AlterUniqueTogether(
            name='protein',
            unique_together=set([('network_x_coordinate', 'network_y_coordinate')]),
        ),
    ]
