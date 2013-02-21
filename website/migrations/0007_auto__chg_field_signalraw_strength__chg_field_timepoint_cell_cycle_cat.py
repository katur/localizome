# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SignalRaw.strength'
        db.alter_column('website_signalraw', 'strength', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'Timepoint.cell_cycle_category'
        db.alter_column('website_timepoint', 'cell_cycle_category', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'Timepoint.display_order'
        db.alter_column('website_timepoint', 'display_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'Compartment.display_order'
        db.alter_column('website_compartment', 'display_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'SignalMerged.strength'
        db.alter_column('website_signalmerged', 'strength', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

    def backwards(self, orm):

        # Changing field 'SignalRaw.strength'
        db.alter_column('website_signalraw', 'strength', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Timepoint.cell_cycle_category'
        db.alter_column('website_timepoint', 'cell_cycle_category', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Timepoint.display_order'
        db.alter_column('website_timepoint', 'display_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Compartment.display_order'
        db.alter_column('website_compartment', 'display_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'SignalMerged.strength'
        db.alter_column('website_signalmerged', 'strength', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'website.compartment': {
            'Meta': {'object_name': 'Compartment'},
            'compartment_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'website.protein': {
            'Meta': {'object_name': 'Protein'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'website.signalmerged': {
            'Meta': {'object_name': 'SignalMerged'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Compartment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Timepoint']"})
        },
        'website.signalraw': {
            'Meta': {'object_name': 'SignalRaw'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Compartment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Timepoint']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        },
        'website.timepoint': {
            'Meta': {'object_name': 'Timepoint'},
            'cell_cycle_category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timepoint_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'date_filmed': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lens': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"})
        }
    }

    complete_apps = ['website']