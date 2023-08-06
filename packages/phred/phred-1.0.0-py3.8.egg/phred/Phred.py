#!/usr/bin/env python3

import sys, os, os.path, json
from getopt import getopt, gnu_getopt

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

from phred.EditWin import EditWin
import phred.UiComponents as ui

#	consider 'Courier 10 Pitch 12' -> ugly

def GetOpts():
	config = ui.GetConfig()

	opts, args = gnu_getopt( sys.argv[1:], 's:f:c' )
	for opt, val in opts:
		if opt == '-s':
			config.style = val
		elif opt == '-f':
			config.font = val
		elif opt == '-c':
			config.create = True

	return config, args

class NoSuchFile( Exception ): pass
class IsDirectory( Exception ): pass

def validateFile( fname, config ):
	if os.path.isdir( fname ):
		raise IsDirectory( fname )
	elif not config.create:
		if not os.path.exists( fname ):
			raise NoSuchFile( fname )
	return True

def main():
	config, files = GetOpts()

	if files:
		for f in files:
			try:
				validateFile( f, config )
			except NoSuchFile:
				print( f, 'does not exist', file=sys.stderr )
				sys.exit( 1 )
			except IsDirectory:
				print( f, 'is a directory', file=sys.stderr )
				sys.exit( 1 )
			else:
				frame = EditWin.new( config, f )
				frame.show()
	else:
		frame = EditWin.new( config )
		frame.show()
	gtk.main()

if __name__ == '__main__':
	main()
