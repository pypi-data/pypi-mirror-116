#
#	Pairs.py
#
#	selection of matching Pairs for Editor class
#

pairs =	[
					(  '{',	'}',	True ),
					( '"',	'"',	False ),
					(  '`',	'`',	True ),
					( '/',	'/',	True ),
					(  '\'','\'',	True ),
					( '[',	']',	True ),
					( '<',	'>',	True ),
					( '(',	')',	True ),
					(  '#',	'#',	True ),
				]

NoPair = ( None, None, None )

def LeftPair( c ):
	for left, right, strict in pairs:
		if left == c:
			return left, right, strict
	return NoPair

def RightPair( c ):
	for left, right, strict in pairs:
		if right == c:
			return left, right, strict
	return NoPair


#
#	scan through text, looking for matching Pairs
#

def ScanForward( text, index, pair ):
	others = 0

	for i in range( index, len( text ) ):
		left, right, strict = pair

		if text[i] == left and left != right:
			others += 1
		elif text[i] ==right:
				if others and strict:
					others -= 1
				else:
					return i

	return -1

def ScanBackward( text, index, pair ):
	others = 0

	for i in range( index, 0, -1 ):
		left, right, strict = pair
		if text[i] == right and left != right:
			others += 1
		elif text[i] == left:
				if others and strict:
					others -= 1
				else:
					return i + 1

	return -1

def test():
	text = '''ScanForward( int index, Pair *pair )
				{
					register const char *cp = Text( index );
				'''

if __name__ == '__main__':
	test()
