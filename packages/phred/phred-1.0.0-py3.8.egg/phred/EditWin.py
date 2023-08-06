#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import re, sys, os.path, string

from phred.Menu import Menu
from phred.Editor import Editor
from phred.Selector import Selector
from phred.tags import ReadTagsFile
from phred.Piper import Piper
from phred.SearchReplace import SearchReplace

class EditWin( Gtk.Window ):
	numOpen = 0
	windows = {}

	@classmethod
	def new( cls, config, filename=None ):
		if filename:
			realname = os.path.abspath( filename )
			if not cls.windows.get( realname, False ):
				cls.windows[realname] = EditWin( config, realname )
			return cls.windows[realname]
		else:
			return EditWin( config )

	@classmethod
	def remove( cls, realname ):
		try:
			del cls.windows[ realname ]
		except:
			pass
			
		EditWin.numOpen -= 1
		if EditWin.numOpen < 1:
			Gtk.main_quit()

	def __init__( self, config, filename=None ):
		super(EditWin, self).__init__( Gtk.WindowType.TOPLEVEL )	
		self.connect( 'delete_event', self.deleted )
		self.set_border_width( 0 )
		self.set_default_size( 650, 500 )
	#	self.set_default_size( 900, 600 )
	#	self.set_has_frame( False )


#
#	put the abspath thing here, so unique? or store in windows list?
#	to solve prob of not detecting that /a/b/c and c are same.
#

		self.config		= config
		self.filename	= filename or "JunkFile"
		self.dirname		= '.'
		self.findbuf		= ''

		self.SetTitle()
		self.Layout()
		EditWin.numOpen += 1
		self.tags = ReadTagsFile( '.tags' )
		
	def Layout( self ):
		interior = Gtk.VBox()
	
	#	create editor and file menu
	
		self.editor = Editor( self, self.config, self.filename )

		subitems =  [
						( "browse",	self.onBrowse ),
						( "open",	self.OnOpen ),
						( "pipe",	self.OnPipe ),
						( "search",	self.OnSearch ),
						( "rename",	self.OnRename ),
					]
		self.fileMenu = Menu(	[
									( "read",	self.OnRead ),
									( "write",	self.OnSave  ),
									( "misc",	subitems ),
									( "close",	self.OnMinimize ),
									( "quit",	self.OnExit ),
								],
								self.config
							)

		self.editor.connect( 'button-press-event', self.buttonPressed )
		self.editor.show()

	#	create scrollable text area
	
		textarea = Gtk.ScrolledWindow()
		textarea.set_policy( Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC )
		textarea.add( self.editor )
		interior.pack_start( textarea, True, True, 0 )
		textarea.show()

	#	create status area
	
		self.statusfield = Gtk.Entry()
		interior.pack_start( self.statusfield, False, True, 0 )
		self.statusfield.show()
		
		#Finish window properties
		self.add( interior )
		interior.show()

#	file menu callbacks

	def buttonPressed( self, widget, event ):
		if event.button == 3:
			self.lastButtonEvent = ( int( event.x_root ), int( event.x_root ), event.button, event.time )
			self.fileMenu.Popup( event )
			return True
		else:
			return False
			
#	Event handlers:

	def NotImplemented(self, event):
		print( 'not implemented' )

	def OnAbout(self, event):
		dialog = wx.MessageDialog(self, 'A sample editor\n'
			'in wxPython', 'About Sample Editor', wx.OK)
		dialog.ShowModal()
		dialog.Destroy()

	def OnMinimize( self, event):
		self.Hide()

	def OnExit(self, event):
		if self.editor.WasModified():
			if self.AreYouSure( 'Really quit?', 'Quit' ):
				self.Close()
		else:
			self.Close()

	def OnRead(self, event):
		if self.editor.WasModified():
			if self.AreYouSure( 'Really read?', 'Read' ):
				self.editor.onReadFile( event )
		else:
			self.editor.onReadFile( event )

	def OnSave(self, event):
		textfile = open( os.path.join(self.dirname, self.filename), 'w' )
		textfile.write(self.editor.GetText())
		textfile.close()
		self.editor.Modified( False )

	def OnOpen(self, event):
		if True:
			filename = getFileName( 'WTF???' )
			if filename:
				frame = EditWin.new( self.config, filename )
				frame.show()
		else:
			dialog = Gtk.FileSelection( 'Select file to open' )
			dialog.ok_button.connect_object( 'clicked', self.OpenNewFile, dialog )
			dialog.cancel_button.connect( 'clicked', lambda w: dialog.destroy() )
			dialog.show()

	def OnPipe( self, event ):
		piper = Piper( self, self.config )
		piper.show()

	def OnSearch( self, event ):
		dialog = SearchReplace( self, self.config )
		dialog.show()


	def OnRename(self, event):
		filename = getFileName( 'WTF???' )
		if filename:
			self.filename	= os.path.basename( filename )
			self.dirname	= os.path.dirname( filename )
			self.modified	= True

			self.editor.Modified( True )

	def onBrowse( self, event ):
		target = self.editor.GetSelectedText()

		if target:
			selections = [
						#	goofy lambda args work around python lambda bug
							( ( filename, where ), lambda x,filename=filename,where=where: self.EditFile( filename, where ) )
							for tag, filename, where in self.tags
								if target == tag
						]
			if selections:
				if len( selections ) == 1:
					xx, callback  = selections[0]
					callback( xx )
				else:
					self.selector = Selector( selections, {} )
					self.selector.show()
			else:
				self.editor.Complain( '%s not found' % ( target ) )

	def EditFile( self, filename, where ):
		frame = EditWin.new( self.config, filename )
		frame.show()
		if type( where ) is int:
			frame.editor.SelectLine( where )
		else:
			frame.editor.doFind( where )
		return frame

#	file selection

	def OpenNewFile( self, dialog ):
		frame = EditWin.new( self.config, dialog.get_filename() )
		frame.show()
		dialog.destroy()	

#	component creation

	def SetTitle(self):
		self.set_title( compressPath( self.filename ) )

	def SetStatusText( self, text ):
		self.statusfield.set_text( text )
		
	def OpenFile( self, filename ):
		self.filename = filename or 'Junkfile'

		if self.filename == '-':
			self.editor.SetValue( sys.stdin.read() )
		else:
			try:
				fp = open( os.path.join( self.dirname, self.filename ), 'r' )
				self.editor.SetValue( fp.read() )
				fp.close()
			except:
				self.editor.SetValue( 'hi mom' )

#	Helper methods:

	def GetFilename(self, **dialogOptions):
		dialog = wx.FileDialog(self, **dialogOptions)

		if dialog.ShowModal() == wx.ID_OK:
			answer = True,dialog.GetFilename(),dialog.GetDirectory()
		else:
			answer = False, self.filename, self.dirname

		dialog.Destroy()
		return answer

	def askUserForFilename(self, **dialogOptions):
		dialog = wx.FileDialog(self, **dialogOptions)
		if dialog.ShowModal() == wx.ID_OK:
			userProvidedFilename = True
			self.filename = dialog.GetFilename()
			self.dirname = dialog.GetDirectory()
			self.SetTitle() # Update the window title with the new filename
		else:
			userProvidedFilename = False
		dialog.Destroy()
		return userProvidedFilename

	def defaultFileDialogOptions(self):
		return dict(message='wtf?', defaultDir=self.dirname, wildcard='*')

#	Browsing


	def Status( self, msg ):
		self.SetStatusText( msg )

	def deleted( self, widget, data=None ):
		self.Close()
		
	def Close( self ):
		self.destroy()
		EditWin.remove( self.filename )
		return False

#	dialogs

	def AreYouSure( self, prompt, action ):
		dialog=Gtk.Dialog( prompt,
							None,0,
							(
								"Cancel", False,
								action, True
							) )
		answer = dialog.run()
		dialog.destroy()
		return answer

	def GetText( self ):
		return self.editor.GetText()

	def SetText( self, text ):
		return self.editor.SetText( text )

def getFileName( prompt="Open" ):
	dialog = Gtk.FileChooserDialog( prompt, None, Gtk.FileChooserAction.OPEN,
									( Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_OPEN, Gtk.ResponseType.OK) )
	dialog.set_default_response( Gtk.ResponseType.OK )
	response = dialog.run()
	if response == Gtk.ResponseType.OK:
		filename = dialog.get_filename()
	elif response == Gtk.RESPONSE_CANCEL:
		filename = ''
	else:
		raise Exception( 'getFileName() got %s???' % response )

	dialog.destroy()
	return filename

#
#	compress all the java crap out of too-long paths
#

def compressPath( path ):
	Subs =	[
				( os.getenv( 'HOME' ), '~' ),
				( 'git/aws/resourceupdatedetectionservice3', 'git' ),
				( 'service/src/main/java/com/att/acp/resourceupdatedetectionservice3', 'ruds3' ),
				( 'resourceupdatedetectionservice3', 'ruds3' ),

				( 'git/aws/common-astra-apis', 'git//apis' ),
				( 'src/main/java/com/att/cso', 'cso' ),
			]

	for pattern, replacement in Subs:
		path = re.sub( pattern, replacement, path )

	return path


TestPaths	= 	[
					'/home/garry/git/aws/resourceupdatedetectionservice3/service/src/main/java/com/att/acp',
					'/home/gh2787/git/aws/resourceupdatedetectionservice3/service/src/main/java/com/att/acp/resourceupdatedetectionservice3/controller/ResourceDetector.java',
					'/home/gh2787/git/aws/common-astra-apis/src/main/java/com/att/cso/astra/common/client/policy/ext',

				]
if __name__ == '__main__':
	for path in TestPaths:
		print( path, '->', compressPath( path ) )
