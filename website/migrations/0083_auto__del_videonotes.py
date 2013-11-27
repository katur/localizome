# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'VideoNotes'
        db.delete_table(u'website_videonotes')


    def backwards(self, orm):
        # Adding model 'VideoNotes'
        db.create_table(u'website_videonotes', (
            ('note', self.gf('django.db.models.fields.CharField')(max_length=700)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Video'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'website', ['VideoNotes'])


    models = {
        u'website.compartment': {
            'Meta': {'ordering': "['id']", 'object_name': 'Compartment'},
            'extra_short_name': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'supercompartment': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'website.protein': {
            'Meta': {'ordering': "['common_name']", 'unique_together': "(('network_x_coordinate', 'network_y_coordinate'),)", 'object_name': 'Protein'},
            'common_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_paper': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'network_x_coordinate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'network_y_coordinate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'representative_video': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'representative'", 'unique': 'True', 'null': 'True', 'to': u"orm['website.Video']"}),
            'sequence': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        u'website.signalmerged': {
            'Meta': {'ordering': "['protein', 'compartment', 'timepoint']", 'object_name': 'SignalMerged'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Compartment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Protein']"}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Timepoint']"})
        },
        u'website.signalraw': {
            'Meta': {'ordering': "['video', 'compartment', 'timepoint']", 'object_name': 'SignalRaw'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Compartment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Timepoint']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Video']"})
        },
        u'website.strain': {
            'Meta': {'object_name': 'Strain'},
            'genotype': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Protein']"})
        },
        u'website.timepoint': {
            'Meta': {'ordering': "['id']", 'object_name': 'Timepoint'},
            'cell_cycle_category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'website.video': {
            'Meta': {'ordering': "['movie_number']", 'object_name': 'Video'},
            'date_filmed': ('django.db.models.fields.DateField', [], {}),
            'date_scored': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'excel_id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lens': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'movie_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Protein']"}),
            'strain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Strain']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'})
        }
    }

    complete_apps = ['website']