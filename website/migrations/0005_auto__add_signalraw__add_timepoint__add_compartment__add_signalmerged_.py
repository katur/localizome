# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SignalRaw'
        db.create_table('website_signalraw', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('strength', self.gf('django.db.models.fields.IntegerField')()),
            ('compartment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Compartment'])),
            ('timepoint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Timepoint'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Video'])),
        ))
        db.send_create_signal('website', ['SignalRaw'])

        # Adding model 'Timepoint'
        db.create_table('website_timepoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell_cycle_category', self.gf('django.db.models.fields.IntegerField')()),
            ('timepoint_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('website', ['Timepoint'])

        # Adding model 'Compartment'
        db.create_table('website_compartment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('compartment_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('website', ['Compartment'])

        # Adding model 'SignalMerged'
        db.create_table('website_signalmerged', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('strength', self.gf('django.db.models.fields.IntegerField')()),
            ('compartment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Compartment'])),
            ('timepoint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Timepoint'])),
            ('protein', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Protein'])),
        ))
        db.send_create_signal('website', ['SignalMerged'])

        # Adding field 'Video.notes'
        db.add_column('website_video', 'notes',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'SignalRaw'
        db.delete_table('website_signalraw')

        # Deleting model 'Timepoint'
        db.delete_table('website_timepoint')

        # Deleting model 'Compartment'
        db.delete_table('website_compartment')

        # Deleting model 'SignalMerged'
        db.delete_table('website_signalmerged')

        # Deleting field 'Video.notes'
        db.delete_column('website_video', 'notes')


    models = {
        'website.compartment': {
            'Meta': {'object_name': 'Compartment'},
            'compartment_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
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
            'strength': ('django.db.models.fields.IntegerField', [], {}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Timepoint']"})
        },
        'website.signalraw': {
            'Meta': {'object_name': 'SignalRaw'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Compartment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strength': ('django.db.models.fields.IntegerField', [], {}),
            'timepoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Timepoint']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Video']"})
        },
        'website.timepoint': {
            'Meta': {'object_name': 'Timepoint'},
            'cell_cycle_category': ('django.db.models.fields.IntegerField', [], {}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timepoint_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'date_filmed': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lens': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"})
        }
    }

    complete_apps = ['website']