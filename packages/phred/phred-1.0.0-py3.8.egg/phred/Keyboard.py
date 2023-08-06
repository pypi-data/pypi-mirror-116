#
#	keyboard.c
#
#	keyboard editing operations for Editor class
#

def ctrl( c ):
	return ord(c) & ~0x60


def HandleKeyHit( editor, key ):
	if key.isModifierKey():
		return

	elif escHit:
		HandleMeta( key )

	elif key == WXK_Escape:
		editor.escHit = True;			# esc

	elif key == ctrl('X'):
		editor.ctrlXHit = true

	elif key in [ META(XK_Home), META(XK_R7), ctrl('A') ]:
		editor.BeginningOfLine()
		editor.SelectText(editor.Dot() )

	elif key in [ XK_Left, ctrl('B') ]:
		editor.BackwardCharacter()
		SelectText( editor.Dot() )

	elif key == ctrl('D'):
		editor.DeleteChar( 1 )

	elif key in [ ctrl('U'), XK_F14, XK_Undo ]:
		editor.UnDo()

	elif key in [ META(XK_End), META(XK_R13), ctrl('E') ]:
		editor.EndOfLine()
		editor.SelectText( editor.Dot() )

	elif key in [ XK_Right, ctrl('F') ]:
		editor.ForwardCharacter()
		editor.SelectText( editor.Dot() )

	elif key == ctrl('G'):
		editor.Show( "%s:%d" % ( Name(), LineNumber( Dot() ) + 1 ) )

	elif key == ctrl('K'):
		editor.KillLine()

	elif key in [ XK_Down, ctrl('N') ]:
		editor.MoveLine( 1 )

	elif key in [ XK_Up, ctrl('P') ]:
		editor.MoveLine( -1 )

	elif key [ ctrl('R'), ctrl('S') ]:
		editor.looker.Appear( this )

	elif keyin [ XK_R15, ctrl('V') ]:
		editor.ForwardPage( 1 );
		editor.SelectText( editor.Dot() );

	elif key == ctrl('Y'):
		editor.Yank();

	elif key in [ '\t', XK_Tab ]:
		editor.InsertChar( lastChar = '\t' )

	elif key in [ ctrl('M'), '\n', XK_Return]:
		editor.InsertChar( lastChar = '\n' )

	elif key in [ ctrl('H'), XK_BackSpace, XK_Delete ]:
		if ( editor.SelectionSize() > 0 ):
			editor.Cut()
		else:
			editor.DeleteChar( -1 )

	elif key in [ XK_Home, XK_R7 ]:
		editor.BeginningOfText()
		editor.SelectText( editor.Dot() )

	elif key in [ XK_End, XK_R13 ]:
		editor.SelectText(editor.Length() )

	elif key == XK_R9:
		editor.BackwardPage( 1 )
		editor.SelectText(editor.Dot() )

	elif key == XK_L10:
		editor.Cut()

	elif key == XK_L8:
		editor.Paste()

	elif key == XK_L6:
		editor.Snarf()

	elif key == XK_L9:
		editor.Find()

	elif key == META('q'):
		editor.Quit()

	elif key in [ XK_F1, XK_F2, XK_F3, XK_F4, XK_F5, XK_F6, XK_F7, XK_F8, XK_F9, XK_F10, XK_F11, XK_F12 ]:
		editor.HandleMacro( c )

	elif key == META('b'):
		editor.Browse()

	elif key == META('o'):
		editor.Open()

#	elif key == META('m'):
#		editor.macroEditor->Appear( this )

#	elif key == META('p'):
#		editor.PopPiper()
	
	elif key == META('e'):
		editor.Visit()

	elif key == META('r'):
		editor.Rename()
	else:
		if isascii( c ) and isprint( c ):
			editor.InsertChar( lastChar = c )
		else:
			editor.Complain( 'Huh? <%s>' % key.tag() )

'''

//#define ctrl( c )	((c)-'@')
// #define ctrl( x )	KEYDEF( x, CTRL_MASK )
#define ctrl( c )	((c)&~0x60)

void
FileEditor :: HandleMeta( KeyDef key )
{
	int c;

	escHit = false;

	switch ( c = key.norm() )
	       {
		case 'b':	textEditor->BackwardWord( 1 );
				SelectText( textEditor->Dot() );
				break;
		case 'f':	textEditor->ForwardWord( 1 );
				SelectText( textEditor->Dot() );
				break;
		case 'v':	textEditor->BackwardPage( 1 );
				SelectText( textEditor->Dot() );
				break;

		case '<':	textEditor->BeginningOfText();
				SelectText( textEditor->Dot() );
				break;

		case '>':	textEditor->EndOfText();
				SelectText( textEditor->Dot() );
				break;

		case '=':	Complain( "not implemented" );
				break;

		case ctrl('G'):	garry->Appear( this );
				break;

		default:	Complain( "Huh? <ESC> <%s>", (const char*)key.tag() );
				break;
	       }
}

void
FileEditor :: MoveLine( int n )	// move forward or backward n lines
{
	int index = textEditor->Dot();
	int offset = textBuffer->LineOffset( index );
	int lineNum = textBuffer->LineNumber( index );

	int bol = textBuffer->LineIndex( lineNum + n );
	int eol = textBuffer->EndOfLine( bol );

	index = bol + offset;
	index = ( index > eol ) ? eol : index;
	SelectText( index );
}

void
FileEditor :: KillLine()		// kill to EOL
{
	int dot = textEditor->Dot();
	int eol = ( textBuffer->IsBeginningOfLine( dot ) )
			? textBuffer->BeginningOfNextLine( dot )
			: textBuffer->EndOfLine( dot );

	SelectText( dot, eol );
	Cut();
}

void
FileEditor :: Yank()		// keyboard controlled paste
{
	Paste();
	SelectText();
}

void
FileEditor :: DeleteChar( self, int n )
{
	int dot = min( Dot(), Mark() );
	int start = ( n < 0 ) ? ( dot + n ) : dot;

	if ( start < 0 )
		start = 0;			// don't go before beginning of buffer

	int len = SelectionSize() + AbsVal( n );

	if ( start + len > Length() )
		len = Length() - start;		// or after end of buffer

	String deleted( Text( start ), len );

	if ( textEditor->Dot() != textEditor->Mark() )
		textEditor->DeleteSelection();

	textEditor->DeleteText( n );

	LogDeletion( deleted, start );
	SetModified( true );
}

void
FileEditor :: InsertChar( self, char c )
{
	int start = min( Dot(), Mark() );
	String replaced( Text( start ), SelectionSize() );

	textEditor->DeleteSelection();
	textEditor->InsertText( &c, 1 );

	LogInsertion( replaced, start, 1 );

        SetModified( true );
	textEditor->ScrollToSelection();
}

'''
