# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FixedModule'
        db.create_table(u'taskgoals_fixedmodule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=3000)),
        ))
        db.send_create_signal(u'taskgoals', ['FixedModule'])

        # Adding model 'Module'
        db.create_table(u'taskgoals_module', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fixedModule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taskgoals.FixedModule'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='modules', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'taskgoals', ['Module'])

        # Adding model 'Task'
        db.create_table(u'taskgoals_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taskgoals.Module'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['auth.User'])),
            ('body', self.gf('django.db.models.fields.TextField')(default='', max_length=3000, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('progress', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'taskgoals', ['Task'])


    def backwards(self, orm):
        # Deleting model 'FixedModule'
        db.delete_table(u'taskgoals_fixedmodule')

        # Deleting model 'Module'
        db.delete_table(u'taskgoals_module')

        # Deleting model 'Task'
        db.delete_table(u'taskgoals_task')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taskgoals.fixedmodule': {
            'Meta': {'object_name': 'FixedModule'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '200'})
        },
        u'taskgoals.module': {
            'Meta': {'object_name': 'Module'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'modules'", 'to': u"orm['auth.User']"}),
            'fixedModule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taskgoals.FixedModule']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'taskgoals.task': {
            'Meta': {'object_name': 'Task'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '3000', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taskgoals.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'progress': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['taskgoals']