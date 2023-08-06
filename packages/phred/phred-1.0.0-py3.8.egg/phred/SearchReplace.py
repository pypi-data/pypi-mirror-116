#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys, os, os.path, string
from subprocess import *

import phred.UiComponents as ui

class SearchReplace( Gtk.Window ):
	def __init__( self, owner, config ):
		super( SearchReplace, self ).__init__( Gtk.WindowType.TOPLEVEL )
		self.owner = owner
		self.config = config

		self.set_border_width( 0 )
		self.set_title( 'Search/Replace' )
		self.Layout()
		
	def Layout( self ):
		self.targetEntry = Gtk.Entry()
		self.replaceEntry = Gtk.Entry()

		buttons = ui.HBox(
							ui.Button( "Search",		self.Search ),
							ui.Button( "Replace",		self.Replace ),
						#	ui.Button( "Replace All",	self.ReplaceAll ),
							ui.Button( "Done",			self.Quit )
						)

		table = ui.Table( [
							[ Gtk.Label( "Search for" ),	self.targetEntry ],
							[ Gtk.Label( "Replace with" ),	self.replaceEntry ],
							[ ( buttons, 2, 1 ) ]
						] )

		self.add( table )
		self.show_all()

	def Search( self, widget, data ):
		target = self.targetEntry.get_text()

		if target:
			self.owner.editor.doFind( target )

	def Replace( self, widget, data ):
		target = self.targetEntry.get_text()
		replacement = self.replaceEntry.get_text()

		if target:
			self.owner.editor.doReplace( replacement )
			self.owner.editor.doFind( target )

	def ReplaceAll( self, widget, data ):
		print( 'replace all not implemented' )

	def Quit( self, widget, data ):
		self.destroy()


if __name__ == '__main__':
	pass


