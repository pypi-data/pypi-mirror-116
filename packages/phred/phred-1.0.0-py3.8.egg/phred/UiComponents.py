#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

import os, json

#	selections

def GetPrimarySelection():
	cb = Gtk.Clipboard.get( Gdk.SELECTION_PRIMARY )
	return cb.wait_for_text()

def SetPrimarySelection( text ):
	cb = Gtk.Clipboard( selection = Gdk.SELECTION_CLIPBOARD )
	cb.set_text( text )
	

#	Configuration

OkStyles = ['kate', 'tango', 'classic']
BadDarkStyles = [ 'cobalt', 'oblivion', 'solarized-dark', 'solarized-light',  ]
DefaultStyle = 'tango'

class Config( object ):
	def __init__( self, dict = {} ):
		self.font = dict.get( 'font', 'Liberation Mono 10' )
		self.style = dict.get( 'style', DefaultStyle )
		self.show_line_numbers = dict.get( 'show_line_numbers', False )
		self.create = False

		self.force_space_indentation = dict.get( 'force_space_indentation' )

def GetConfig():
	configFile = os.path.join(  os.environ['HOME'], '.phredrc' )
	try:
		return Config( json.loads( open( configFile, 'r' ).read() ) )
	except Exception as e:
		print( 'failed to read config file', configFile, ':', e )
		return Config()


#	Tables

def inventory( rows ):
	ncols = 0

	for row in rows:
		ncols = max( ncols, len( row ) )
	return len( rows ), ncols

			
class Table( Gtk.Table ):
	def __init__( self, rows ):
		nrows, ncols = inventory( rows )
		super( Table, self ).__init__( nrows, ncols, False )
		self.Layout( rows )

	def Layout( self, rows ):
		r = 0

		for row in rows:
			c = 0
			for item in row:
				if item:
					wid = 1
					if type( item ) is tuple:
						component, wid, hgt = item
					else:
						wid = hgt = 1
						component = item
					self.attach( component, c, c+wid, r, r+hgt, xoptions=Gtk.AttachOptions.SHRINK, yoptions=Gtk.AttachOptions.SHRINK )
					component.show()
				c += 1
			r += 1
		self.show()


class HBox( Gtk.HBox ):
	def __init__( self, *items ):
		super( HBox, self ).__init__( False, 0 )
		for item in items:
			self.pack_start( item, True, True, 0 )
			item.show()
		self.show()

class VBox( Gtk.VBox ):
	def __init__( self, *items ):
		super( VBox, self ).__init__( False, 0 )
		for item in items:
			self.pack_start( item, True, True, 0 )
			item.show()
		self.show()

class Button( Gtk.Button ):
	def __init__( self, label, callback ):
		super( Button, self ).__init__( label )
		self.connect( 'clicked', callback, label )

class RadioHBox( Gtk.HBox ):
	def callback( self, widget, data=None ):
		print( 'callback:', widget, data )
		self.value = data

	def GetValue( self ):
		return self.value

	def __init__( self, items ):
		super( RadioHBox, self ).__init__( False, 0 )
		self.value = None
		group = None

		for label, value in items:
			button = Gtk.RadioButton.new_with_label_from_widget( group, label=label )
			group = group or button		# first one is the group
			button.connect( "toggled", self.callback, value )
			self.pack_start( button, True, True, 0 )
			button.show()

		self.show()
