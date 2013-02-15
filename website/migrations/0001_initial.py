# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Protein'
        db.create_table('website_protein', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sequence', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('website', ['Protein'])

        # Adding model 'Video'
        db.create_table('website_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_filmed', self.gf('django.db.models.fields.DateTimeField')()),
            ('protein', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Protein'])),
        ))
        db.send_create_signal('website', ['Video'])


    def backwards(self, orm):
        # Deleting model 'Protein'
        db.delete_table('website_protein')

        # Deleting model 'Video'
        db.delete_table('website_video')


    models = {
        'website.protein': {
            'Meta': {'object_name': 'Protein'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'website.video': {
            'Meta': {'object_name': 'Video'},
            'date_filmed': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Protein']"})
        }
    }

    complete_apps = ['website']