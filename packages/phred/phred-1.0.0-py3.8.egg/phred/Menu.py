#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Pango as pango


# import pango

import sys, os.path
from types import *

KLUDGE = 4

class Menu( Gtk.Menu ):
	def __init__( self, items, config ):
		'items: [ ( label, callback ) ] '
		self.lastPick = 0

		Gtk.Menu.__init__( self )

	#	calculate font height

		fontdesc = pango.FontDescription( config.font )
		self.modify_font( fontdesc )

		cwid, self.fontheight = self.textsize( ' ', fontdesc )
		self.fontheight += KLUDGE

	#	create menuitems

		self.actions = {}
		id = 0

		for label, action in items:
			item = Gtk.MenuItem( label )
			item.modify_font( fontdesc )

			self.append( item )

			if type( action ) is list:
				submenu = Menu( action, config ) 
				submenu.modify_font( fontdesc )
				item.set_submenu( submenu )
			else:
				self.actions[id] = action
				item.connect_object( 'activate', self.OnSelected, id )
			id += 1

	def textsize( self, str, fontdesc ):
		layout = pango.Layout( self.get_pango_context() )

		layout.set_text( str )
		layout.set_font_description( fontdesc )
		wid, hgt = layout.get_pixel_size()
		return wid, hgt

#	menuItem callback

	def OnSelected( self, index ):
		callback = self.actions[ index ]
		self.lastPick = index

		callback( None )

	def Popup( self, event ):
		x = int( event.x_root ) - 20

	#	does y calc make sense?
	#	y = int( event.y_root ) - ( (self.lastPick+1) * self.fontheight - self.fontheight/4 )

		y = int( event.y_root ) - ( (self.lastPick+1) * (self.fontheight + 2 ) )

		def func( menu, _a, _b, _user_data ):
			return x, y, True

		if event.button in ( 2, 3 ):
			self.popup( None, None, func, None, event.button, event.time )
			self.show_all()
		return True

