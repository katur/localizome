# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Timepoint.miyeko_excel_name'
        db.delete_column('website_timepoint', 'miyeko_excel_name')

        # Deleting field 'Timepoint.display_order'
        db.delete_column('website_timepoint', 'display_order')

        # Deleting field 'Compartment.miyeko_excel_name'
        db.delete_column('website_compartment', 'miyeko_excel_name')

        # Deleting field 'Compartment.display_order'
        db.delete_column('website_compartment', 'display_order')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Timepoint.miyeko_excel_name'
        raise RuntimeError("Cannot reverse this migration. 'Timepoint.miyeko_excel_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Timepoint.display_order'
        raise RuntimeError("Cannot reverse this migration. 'Timepoint.display_order' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Compartment.miyeko_excel_name'
        raise RuntimeError("Cannot reverse this migration. 'Compartment.miyeko_excel_name' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Compartment.display_order'
        raise RuntimeError("Cannot reverse this migration. 'Compartment.display_order' and its values cannot be restored.")

    models = {
        'website.compartment': {
            'Meta': {'ordering': "['id']", 'object_name': 'Compartment'},
            'extra_short_name': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'supercompartment': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'website.protein': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'Protein'},
            'common_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative_video': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'representative'", 'unique': 'True', 'null': 'True', 'to': "orm['website.Video']"}),
            'sequence': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        'website.signalmerged': {
            'Meta': {'ordering': "['protein', 'compartment', 'timepoint']", 'object_name': 'SignalMerged'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Compartment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Timepoint']"})
        },
        'website.signalraw': {
            'Meta': {'ordering': "['video', 'compartment', 'timepoint']", 'object_name': 'SignalRaw'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Compartment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Timepoint']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        },
        'website.strain': {
            'Meta': {'object_name': 'Strain'},
            'genotype': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"})
        },
        'website.timepoint': {
            'Meta': {'ordering': "['id']", 'object_name': 'Timepoint'},
            'cell_cycle_category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kahn_merge_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'website.video': {
            'Meta': {'ordering': "['movie_number']", 'object_name': 'Video'},
            'date_filmed': ('django.db.models.fields.DateField', [], {}),
            'date_scored': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'excel_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lens': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'movie_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"}),
            'strain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Strain']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'website.videonotes': {
            'Meta': {'object_name': 'VideoNotes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '700'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        }
    }

    complete_apps = ['website']