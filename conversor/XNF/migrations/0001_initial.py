# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'XNF_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'XNF', ['Document'])

        # Adding model 'TranslateCourseStatus'
        db.create_table(u'XNF_translatecoursestatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseId', self.gf('django.db.models.fields.CharField')(default=None, max_length=200)),
            ('fileId', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('filePath', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('srcLang', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('trgLang', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('startDate', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True, blank=True)),
            ('lastUpdate', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True, blank=True)),
            ('numErrors', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('displayName', self.gf('django.db.models.fields.CharField')(max_length=350)),
            ('displayNameTrg', self.gf('django.db.models.fields.CharField')(max_length=350)),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('status', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'XNF', ['TranslateCourseStatus'])

        # Adding model 'Alert'
        db.create_table(u'XNF_alert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(default=None, max_length=200)),
            ('viewed', self.gf('django.db.models.fields.BooleanField')()),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'XNF', ['Alert'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'XNF_document')

        # Deleting model 'TranslateCourseStatus'
        db.delete_table(u'XNF_translatecoursestatus')

        # Deleting model 'Alert'
        db.delete_table(u'XNF_alert')


    models = {
        u'XNF.alert': {
            'Meta': {'object_name': 'Alert'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {})
        },
        u'XNF.document': {
            'Meta': {'object_name': 'Document'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'XNF.translatecoursestatus': {
            'Meta': {'object_name': 'TranslateCourseStatus'},
            'courseId': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200'}),
            'displayName': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'displayNameTrg': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'fileId': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'filePath': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdate': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'numErrors': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'srcLang': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'startDate': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'trgLang': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['XNF']