# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'tic_tac_toe_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('computer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games', to=orm['tic_tac_toe.Computer'])),
        ))
        db.send_create_signal('tic_tac_toe', ['Game'])

        # Adding model 'Player'
        db.create_table(u'tic_tac_toe_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.OneToOneField')(related_name='player', unique=True, to=orm['tic_tac_toe.Game'])),
        ))
        db.send_create_signal('tic_tac_toe', ['Player'])

        # Adding model 'Computer'
        db.create_table(u'tic_tac_toe_computer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ties', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('losses', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('tic_tac_toe', ['Computer'])

        # Adding model 'Board'
        db.create_table(u'tic_tac_toe_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.OneToOneField')(related_name='board', unique=True, to=orm['tic_tac_toe.Game'])),
        ))
        db.send_create_signal('tic_tac_toe', ['Board'])

        # Adding model 'Tile'
        db.create_table(u'tic_tac_toe_tile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='moves', null=True, to=orm['tic_tac_toe.Player'])),
            ('computer', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='moves', null=True, to=orm['tic_tac_toe.Computer'])),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tiles', to=orm['tic_tac_toe.Board'])),
        ))
        db.send_create_signal('tic_tac_toe', ['Tile'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table(u'tic_tac_toe_game')

        # Deleting model 'Player'
        db.delete_table(u'tic_tac_toe_player')

        # Deleting model 'Computer'
        db.delete_table(u'tic_tac_toe_computer')

        # Deleting model 'Board'
        db.delete_table(u'tic_tac_toe_board')

        # Deleting model 'Tile'
        db.delete_table(u'tic_tac_toe_tile')


    models = {
        'tic_tac_toe.board': {
            'Meta': {'object_name': 'Board'},
            'game': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'board'", 'unique': 'True', 'to': "orm['tic_tac_toe.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tic_tac_toe.computer': {
            'Meta': {'object_name': 'Computer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'tic_tac_toe.game': {
            'Meta': {'object_name': 'Game'},
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': "orm['tic_tac_toe.Computer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tic_tac_toe.player': {
            'Meta': {'object_name': 'Player'},
            'game': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'player'", 'unique': 'True', 'to': "orm['tic_tac_toe.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tic_tac_toe.tile': {
            'Meta': {'object_name': 'Tile'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tiles'", 'to': "orm['tic_tac_toe.Board']"}),
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'moves'", 'null': 'True', 'to': "orm['tic_tac_toe.Computer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'moves'", 'null': 'True', 'to': "orm['tic_tac_toe.Player']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['tic_tac_toe']