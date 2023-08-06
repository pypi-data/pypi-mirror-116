#
#	ChangeRecord.py
#

class ChangeRecord:
	def __init__( self, editor, old, pos ):
		self.editor		= editor
		self.deleted	= old
		self.pos		= pos

class DeleteChange( ChangeRecord ):
		def __init__( self, editor,  old, pos ):
			ChangeRecord.__init__( self, editor, old, pos )

		def  Undo():
			self.editor.SelectText( pos )
			self.editor.AddText( deleted, len( deleted ) )


class InsertChange( ChangeRecord ):
		def __init__( self, editor, old, pos, l ):
			ChangeRecord.__init__( self, editor, old, pos )
			self.len = l

		def Undo( self ):
			self.editor.SelectText( pos, pos + len );
			self.editor.DeleteSelection()
			self.editor.AddText( deleted, deleted.Length() )

