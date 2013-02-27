# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Timepoint', fields ['display_order']
        db.create_unique('website_timepoint', ['display_order'])

        # Adding unique constraint on 'Timepoint', fields ['timepoint_name']
        db.create_unique('website_timepoint', ['timepoint_name'])

        # Adding unique constraint on 'Compartment', fields ['compartment_name']
        db.create_unique('website_compartment', ['compartment_name'])

        # Adding unique constraint on 'Compartment', fields ['display_order']
        db.create_unique('website_compartment', ['display_order'])


    def backwards(self, orm):
        # Removing unique constraint on 'Compartment', fields ['display_order']
        db.delete_unique('website_compartment', ['display_order'])

        # Removing unique constraint on 'Compartment', fields ['compartment_name']
        db.delete_unique('website_compartment', ['compartment_name'])

        # Removing unique constraint on 'Timepoint', fields ['timepoint_name']
        db.delete_unique('website_timepoint', ['timepoint_name'])

        # Removing unique constraint on 'Timepoint', fields ['display_order']
        db.delete_unique('website_timepoint', ['display_order'])


    models = {
        'website.compartment': {
            'Meta': {'object_name': 'Compartment'},
            'compartment_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supercompartment': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'website.protein': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'Protein'},
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
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timepoint_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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