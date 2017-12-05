# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TranslateCourseStatus.startDate'
        db.alter_column(u'XNF_translatecoursestatus', 'startDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))

        # Changing field 'TranslateCourseStatus.lastUpdate'
        db.alter_column(u'XNF_translatecoursestatus', 'lastUpdate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))

        # Changing field 'Alert.startDate'
        db.alter_column(u'XNF_alert', 'startDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'TranslateCourseStatus.startDate'
        db.alter_column(u'XNF_translatecoursestatus', 'startDate', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True))

        # Changing field 'TranslateCourseStatus.lastUpdate'
        db.alter_column(u'XNF_translatecoursestatus', 'lastUpdate', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True))

        # Changing field 'Alert.startDate'
        db.alter_column(u'XNF_alert', 'startDate', self.gf('django.db.models.fields.DateField')(auto_now=True, auto_now_add=True))

    models = {
        u'XNF.alert': {
            'Meta': {'object_name': 'Alert'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
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
            'lastUpdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'numErrors': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'srcLang': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'trgLang': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['XNF']