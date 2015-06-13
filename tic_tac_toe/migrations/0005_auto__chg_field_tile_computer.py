# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tile.computer'
        db.alter_column(u'tic_tac_toe_tile', 'computer_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['tic_tac_toe.Game']))

    def backwards(self, orm):

        # Changing field 'Tile.computer'
        db.alter_column(u'tic_tac_toe_tile', 'computer_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['tic_tac_toe.Computer']))

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
            'computer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'computer_moves'", 'null': 'True', 'to': "orm['tic_tac_toe.Game']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'tiles'", 'null': 'True', 'to': "orm['tic_tac_toe.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'moves'", 'null': 'True', 'to': "orm['tic_tac_toe.Player']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['tic_tac_toe']