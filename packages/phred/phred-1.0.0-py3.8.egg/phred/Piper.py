#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys, os, os.path, string
import subprocess

import phred.UiComponents as ui

SELECTION	= 1
BUFFER		= 2

class Piper( Gtk.Window ):
	Id = 0

	def __init__( self, owner, config ):
		super( Piper, self ).__init__( type=Gtk.WindowType.TOPLEVEL )
		self.owner = owner
		self.config = config

		self.set_border_width( 0 )
		self.set_title( 'Pipe' )
		self.Layout()
		
	def Layout( self ):
		self.callbacks = []

		items = [ [ "none", None ], [ "selection", SELECTION ], [ "buffer", BUFFER ] ]
		self.inputSelector = ui.RadioHBox( items )
		self.command = Gtk.Entry()
		buttons = ui.HBox( ui.Button( "Cancel", self.Quit ), ui.Button( "Execute", self.Execute ) )

		table = ui.Table( [
							[ Gtk.Label( label="Input" ),	self.inputSelector ],
							[ Gtk.Label( label="Command" ),	self.command ],
							[ None,							buttons ]
						] )

		self.add( table )
		self.show_all()

	def Execute( self, widget, data ):
		inType = self.inputSelector.GetValue()
		
		if inType == SELECTION:
			input = ui.GetPrimarySelection()
		elif inType == BUFFER:
			input = self.owner.GetText()
		else:
			input = ''
		
		result = subprocess.run( self.command.get_text().split(),
									input = bytes( input, encoding='utf8' ),
									capture_output=True )
			
		editor = self.owner.EditFile( None, None )
		editor.SetText( str( result.stdout, encoding='utf8' ) )
		editor.show()
		self.destroy()

	def Quit( self, widget, data ):
		print( 'bye mom' )
		self.destroy()

	def nextId( self ):
		id = Piper.Id
		Piper.Id += 1
		return id


if __name__ == '__main__':
	piper = Piper( None, ui.GetConfig() )
	piper.show()
	Gtk.main()


