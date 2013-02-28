# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SignalRaw.video'
        db.delete_column('website_signalraw', 'video_id')

        # Adding field 'SignalRaw.hello'
        db.add_column('website_signalraw', 'hello',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Deleting field 'VideoNotes.video'
        db.delete_column('website_videonotes', 'video_id')

        # Deleting field 'Protein.representative_video'
        db.delete_column('website_protein', 'representative_video_id')


    def backwards(self, orm):
        # Adding field 'SignalRaw.video'
        db.add_column('website_signalraw', 'video',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['website.Video']),
                      keep_default=False)

        # Deleting field 'SignalRaw.hello'
        db.delete_column('website_signalraw', 'hello')

        # Adding field 'VideoNotes.video'
        db.add_column('website_videonotes', 'video',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['website.Video']),
                      keep_default=False)

        # Adding field 'Protein.representative_video'
        db.add_column('website_protein', 'representative_video',
                      self.gf('django.db.models.fields.related.OneToOneField')(related_name='representative', unique=True, null=True, to=orm['website.Video']),
                      keep_default=False)


    models = {
        'website.compartment': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'Compartment'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miyeko_excel_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
            'hello': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Timepoint']"})
        },
        'website.timepoint': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'Timepoint'},
            'cell_cycle_category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miyeko_excel_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'date_filmed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'excel_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lens': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"}),
            'strain': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'vector': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'website.videonotes': {
            'Meta': {'object_name': 'VideoNotes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        }
    }

    complete_apps = ['website']