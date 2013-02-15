# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Protein', fields ['common_name']
        db.create_unique('website_protein', ['common_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Protein', fields ['common_name']
        db.delete_unique('website_protein', ['common_name'])


    models = {
        'website.protein': {
            'Meta': {'object_name': 'Protein'},
            'common_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
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