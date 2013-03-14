# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Video.strain'
        db.add_column('website_video', 'strain',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Strain'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Video.strain'
        db.delete_column('website_video', 'strain_id')


    models = {
        'website.compartment': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'Compartment'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'extra_short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miyeko_excel_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'supercompartment': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'website.protein': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'Protein'},
            'common_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'representative_video': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'representative'", 'unique': 'True', 'null': 'True', 'to': "orm['website.Video']"}),
            'sequence': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
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
            'Meta': {'ordering': "['protein', 'name']", 'object_name': 'Strain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"}),
            'vector': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'website.timepoint': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'Timepoint'},
            'cell_cycle_category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kahn_merge_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'miyeko_excel_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'website.video': {
            'Meta': {'ordering': "['protein', 'filename']", 'object_name': 'Video'},
            'date_filmed': ('django.db.models.fields.DateField', [], {}),
            'date_scored': ('django.db.models.fields.DateField', [], {}),
            'excel_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lens': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"}),
            'strain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Strain']", 'null': 'True'}),
            'strain_name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'vector': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'website.videonotes': {
            'Meta': {'object_name': 'VideoNotes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '700'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        }
    }

    complete_apps = ['website']