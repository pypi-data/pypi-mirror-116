#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import sys, os.path, string

from phred.Menu import Menu
from phred.Editor import Editor

class Selector( Gtk.Window ):

	def __init__( self, selections, config ):
		super( Selector, self ).__init__( Gtk.WindowType.TOPLEVEL )
		self.connect( 'delete_event', self.deleted )

		self.set_border_width( 0 )
		self.set_default_size( 400, 200 )

		self.config		= config

		self.set_title( 'Pick one' )
		self.Layout( selections )
		
	def Layout( self, selections ):
		self.callbacks = []
		vbox = Gtk.VBox( False, 8 )

		sw = Gtk.ScrolledWindow()
		sw.set_shadow_type( Gtk.SHADOW_ETCHED_IN )
		sw.set_policy( Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC )
		vbox.pack_start( sw, True, True, 0 )

		self.store = Gtk.ListStore( str, str )

		for values, callback in selections:
			self.store.append( values )
			self.callbacks.append( callback )

		view = Gtk.TreeView( self.store )
	#	self.treeView.set_rules_hint( True )

		for label, id in [ ( 'file', 0 ), ( 'pattern', 1 ) ]:
			cell = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn( label, cell, text = id )
			column.set_sort_column_id( id )
			view.append_column( column )
			
		view.connect( 'row-activated', self.Picked )
		sw.add( view )
		self.add(vbox)
 
		self.show_all()

#	def callback(treeview, path, view_column, user_param1, ...)

	def Picked( self, treeview, path, view_column ):
		index = path[0]

		if index > -1:
			fn = self.callbacks[ index ]
			fn( treeview )
			self.destroy()

#	Helper methods:

	def deleted( self, widget, data=None ):
		self.destroy()
		Gtk.main_quit()
		return False
