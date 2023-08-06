#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('GtkSource', '4')
from gi.repository import Gtk
from gi.repository import Gdk

from gi.repository import GtkSource
from gi.repository.GtkSource import View, LanguageManager, Buffer, StyleSchemeManager

# import pango
from gi.repository import Pango as pango

import phred.UiComponents as ui

import sys, os.path, string, re
from fnmatch import fnmatch

from phred.Menu import Menu
from phred.Pairs import *
from phred.ChangeRecord import InsertChange, DeleteChange
from phred.Keyboard import HandleKeyHit, ctrl

class Editor( View ):
#	make findBuf and snarfBuf shared
	snarfBuf	= ''
	findBuf		= ''

	def __init__( self, parent, config, filename ):
		super(Editor, self).__init__()
		self.config		= config
		self.filename	= filename
		self.dirname	= '.'
		self.frame		= parent

		self.linguist	= LanguageManager()
		self.textbuf	= Buffer()

#		self.textbuf.set_data( 'languages-manager', self.linguist )
		self.textbuf.languages_manager = self.linguist
		
		ssm = StyleSchemeManager()
		scheme = ssm.get_scheme( self.config.style )
		self.textbuf.set_style_scheme( scheme )
				
		self.set_buffer( self.textbuf )
		self.set_show_line_numbers( self.config.show_line_numbers )
		
#	make findBuf and snarfBuf shared
		self.modified	= False

		self.ClearUndoStack()
		self.OpenFile( filename )

		self.editMenu = Menu(	[
									( "cut",	self.onCut ),
									( "paste",	self.onPaste ),
									( "snarf",	self.onSnarf ),
									( "find",	self.onFind ),
									( "line #",	self.onLine ),
								],
								self.config
							 )

		self.connect( 'button-press-event', self.buttonPressed )

	#	set font

		fontdesc = pango.FontDescription( self.config.font )

		self.modify_font( fontdesc )
		self.setTabStops( fontdesc )

#	make findBuf and snarfBuf shared

	def setTabStops( self, fontdesc ):
		'stupid kludgy hack that will likely not work anywhere else, or if font changes'
		cwid, chgt = self.textsize( ' ', fontdesc )

		nstops = 20
		tabwidth = 4		# like God intended

		tabs = pango.TabArray( nstops, True )

		for i in range( nstops ):
			tabs.set_tab( i, pango.TabAlign.LEFT, tabwidth * (i+1) * cwid )
		self.set_tabs( tabs )

	def textsize( self, str, fontdesc ):
		layout = pango.Layout( self.get_pango_context() )

		layout.set_text( str )
		layout.set_font_description( fontdesc )
		wid, hgt = layout.get_pixel_size()
		return wid, hgt

#-------------------------------------------------------------------------------
#
#	item selection
#
	def PositionFromEvent( self, event ):
		x, y = self.window_to_buffer_coords( Gtk.TextWindowType.TEXT, int( event.x ), int( event.y ) )
		return self.get_iter_at_location( x, y )

	def DoubleClick( self, event ):
		is_over_text, pos = self.PositionFromEvent( event )
		c = pos.get_char()

		if pos.starts_line():
			self.Select( self.BeginningOfLine( pos ),
								self.BeginningOfNextLine( pos ) )
			return True
		elif self.SelectPair( pos ):
			return True
		elif GoodChar( c ):
				self.Select( self.BeginningOfWord( pos ),
									self.EndOfWord( pos ) )
				return True
	#	return False
		return True

	def SelectPair( self, pos ):
		index = pos.get_offset()
		text = self.GetText()
		c = text[index]

		left, right, strict = LeftPair( text[index-1] )

		if left is not None:		#  are we just after a magic char?
			end = ScanForward( text, index, ( left, right, strict ) )

			if end >= 0:
				self.Select( self.PosAtIndex( pos, index ), self.PosAtIndex( pos, end ) )
			else:
				self.Complain( "can't find a '%c' to match '%c'" % ( left, right ) )

			return True
		else:
			left, right, strict = RightPair( text[index] )

			if right is not None:		# are we just before a magic char?
				begin = ScanBackward( text, index-1, ( left, right, strict ) )
				if begin >= 0:
					self.Select( self.PosAtIndex( pos, begin ), self.PosAtIndex( pos, index ) )
				else:
					self.Complain( "can't find a '%c' to match '%c'" % ( left, right ) )
				return True
		return False


	def BeginningOfLine( self, pos ):
		bol = pos.copy()
		bol.backward_line()
		bol.forward_line()
		return bol

	def BeginningOfNextLine( self, pos ):
		bol = pos.copy()
		bol.forward_line()
		return bol

	def BeginningOfWord( self, pos ):
		index = pos.get_offset()
		text = self.GetText()
	
		for i in range( index, 1, -1 ):
			if not GoodChar( text[i-1] ):
				return self.PosAtIndex( pos, i )
		return self.PosAtIndex( pos, 0 )

	def EndOfWord( self, pos ):
		index = pos.get_offset()
		text = self.GetText()
		eot = len( text )

		for i in range( index, eot ):
			if not GoodChar( text[i+1] ):
				return self.PosAtIndex( pos, i+1 )
		return self.PosAtIndex( pos, eot )

	def PosAtIndex( self, pos, index ):
		foo = pos.copy()
		foo.set_offset( index )
		return foo


#-------------------------------------------------------------------------------
#
#	edit menu callbacks
#

	def buttonPressed( self, widget, event ):
		if event.button == 1:
			if event.type == Gdk.EventType._2BUTTON_PRESS:
				return self.DoubleClick( event )
		elif event.button == 2:
			self.editMenu.Popup( event )
			return True
		elif False and event.button == 1 and event.type == gdk.EventType._2BUTTON_PRESS:
			self.DoubleClick( event )
			return True
		else:
			return False

	def onCut( self, event ):
		myselection = self.textbuf.get_selection_bounds()
		if myselection:
			start, end = myselection
			Editor.snarfBuf = self.GetSelectedText()
		#	self.LogDeletion( Editor.snarfBuf, start )
			self.textbuf.delete( start, end )
			self.Modified( True )

	def onPaste( self, event ):
		myselection = self.textbuf.get_selection_bounds()
		if myselection:
			start, end = myselection
			replaced = self.GetSelectedText()
		#	self.LogInsertion( replaced, start, end-start )

			self.textbuf.delete( start, end )
		else:
			start = self.textbuf.get_iter_at_mark( self.textbuf.get_insert() )
			
		self.textbuf.insert( start, Editor.snarfBuf )
		self.Modified( True )

	def onSnarf( self, event ):
		text = ui.GetPrimarySelection()	# self.GetSelectedText() or 
		if text:
			Editor.snarfBuf = self.GetSelectedText()

	def doReplace( self, newtext ):
		myselection = self.textbuf.get_selection_bounds()
		if myselection:
			start, end = myselection
			self.textbuf.delete( start, end )
		else:
			start = self.textbuf.get_iter_at_mark( self.textbuf.get_insert() )
			
		self.textbuf.insert( start, newtext )
		self.Modified( True )

	def onFind( self, event ):
		self.doFind( self.GetSelectedText() or Editor.findBuf )

	def doRegexFind( self, RE ):
	#	assume new file, so search from begin of buffer

		if RE:
			begin, end = self.textbuf.get_bounds()
			print( 'begin', begin, 'end', end )
			allText = self.textbuf.get_text( begin, end )
			parts = re.split( RE, allText, 1 )

			if parts[0] != allText:	# found it!
				index = len( parts[0] )
				self.Select( index, index + 10 )
			else:
				self.Complain( '"%s" not found' % ( RE ) )
		else:
			self.Complain( 'provide an RE, idiot!' )

	def doFind( self, target ):
		if target:
			Editor.findBuf = target
			begin = self.textbuf.get_iter_at_mark( self.textbuf.get_insert() )

			index = self.NextPos( begin ).forward_search( target, 0, None )
			
			if index:
				self.Select( index[0], index[1] )
			else:
				firstpos = self.textbuf.get_start_iter()

				index = firstpos.forward_search( target, 0, None )
				if index:
					self.Select( index[0], index[1] )
				else:
					self.Complain( '"%s" not found' % ( target ) )

	def NextPos( self, iter ):
		offset = iter.get_offset()
		return self.textbuf.get_iter_at_offset( offset + 1 )
		  
	def onLine( self, event ):
		selected = self.GetSelectedText()
		try:
			line = extractNum( selected ) - 1	# not zero origin
		except ValueError:
			self.Complain( '"%s" not an int' % ( selected ) )
		else:
			self.SelectLine( line )

	def onReadFile( self, event ):
		self.OpenFile( self.filename )

#-------------------------------------------------------------------------------
#
#		text editing
#

	def FindText( self, pos, length, target ):
		start_iter = self.textbuf.get_start_iter()
		found = start_iter.forward_search( target, 0, None )
		
		if found:
			begin, end = found
			return begin
		else:
			return -1

	def GetText( self ):
		begin, end = self.textbuf.get_bounds()
		return self.textbuf.get_text( begin, end, False )	# GGH include_hidden_chars True?
#-------------------------------------------------------------------------------
#
#		selection handling
#

	def Select( self, begin, end ):
	#	self.SetSelection( begin, end )
		self.textbuf.select_range( begin, end )
	#	iter = self.textbuf.get_iter_at_mark( self.textbuf.get_insert() )
	#	self.scroll_to_iter( iter, 0.0 )
		mark = self.textbuf.get_insert()
		self.scroll_to_mark( mark, 0.0, False, 0, 0 )
	#	SetPrimarySelection( self.GetSelectedText() )

	def GetSelectedText( self ):
		myselection = self.textbuf.get_selection_bounds()
		
		if myselection:
			begin, end = myselection
			return self.textbuf.get_text( begin, end, False )	# GGH - should include_hidden_chars be True?
		else:
			return ui.GetPrimarySelection()

	def SelectLine( self, line ):
		buf = self.textbuf
		lastline = buf.get_line_count() - 1
			
		begin = buf.get_iter_at_line( min( line, lastline ) )
		end = buf.get_iter_at_line( min( line+1, lastline ) )

		if ( begin.get_line() >= 0 ):
			self.Select( begin, end )

#-------------------------------------------------------------------------------
#
#		key handling
#

	def KeyHit( self, event ):
		key = event.GetKeyCode()
		print( 'KeyHit called with', event )

		if key ==  ctrl( 'x' ):
			self.Complain( 'ctrl-X you, man!' )
		else:
			event.Skip()
#		HandleKeyHit( self, key )

#-------------------------------------------------------------------------------
#
#	undo
#

	def LogDeletion( self, deleted, pos ):
		record = DeleteChange( self, deleted , pos )
		self.undoList.append( record )

	def LogInsertion( self, replaced, pos, len ):
		record = InsertChange( self, replaced, pos, len )
		self.undoList.append( record )

	def UnDo():
		try:
			self.undoList.pop().Undo()
		except IndexError:
			self.Complain( "Undo stack is empty" )

	def ClearUndoStack( self ):
		self.undoList = []


#-------------------------------------------------------------------------------
#
#	utilities
#

	def WasModified( self ):
		return self.textbuf.get_modified()

	def Modified( self, state ):
		self.modified = state
		self.textbuf.set_modified( state )
		self.frame.SetTitle()

	def OpenFile( self, filename ):
		self.filename = filename or 'Junkfile'

		if self.filename == '-':
			self.SetText( sys.stdin.read() )
		else:
			try:
				fullpath = os.path.join( self.dirname, self.filename )
				absname = os.path.abspath( fullpath )
				self.SetLanguage( absname )
				fp = open( absname, 'r' )
				self.SetText( fp.read() )
				fp.close()
			except Exception as details:
				print( 'cannot open file %s: %s' % ( fullpath, details ) )
				self.SetText( '' )

		self.Modified( False )

	def GuessLanguage( self, filename ):
		manager = self.linguist
		guess = manager.guess_language( filename )

		if guess:
			return guess
		else:	# try and guess from content
			firstline = open( filename, 'r' ).readline()
			for language in [ 'python', 'erlang', 'sh', 'xml' ]:
				if fnmatch( firstline, f'*{ language }*' ):
					return manager.get_language( language )
		return None

	def SetLanguage( self, filename ):

		if os.path.isabs(filename):
			path = filename
		else:
  			path = os.path.abspath(filename)

		guess = self.GuessLanguage( filename )
		
		if guess:
			self.textbuf.set_highlight_syntax( True )
			self.textbuf.set_language( guess )
		else:
			self.textbuf.set_highlight_syntax( False )

	#	Special hack to enforce Astra standards. Remove or replace.

		if self.config.force_space_indentation \
			or ( guess and guess.get_name() in [ 'Erlang', 'Java' ] ):
				self.set_indent_width( 4 )      				# as God intended
				self.set_insert_spaces_instead_of_tabs( False )	# as idiots intended

	def Complain( self, msg ):
		self.frame.Status( msg )

	def SetText( self, text ):
		self.textbuf.begin_not_undoable_action()
		self.textbuf.set_text( text )
		self.textbuf.end_not_undoable_action()

#-------------------------------------------------------------------------------------------
#
#	utility functions
#

def GoodChar( c ):
	return c.isalnum() or c == '_'
	
def nthLine( text, n ):
	pos = 0
	line = 0
	for t in text.split( '\n' ):
		if line >= n:
			return pos, pos + len( t ) + 1
		else:
			line += 1
			pos += len( t ) + 1
	return -1, -1

def extractNum( S ):
	if S:
		m = re.search( '(\d+)', S )
		if m:
			return int( m.group( 0 ) )
	raise ValueError

