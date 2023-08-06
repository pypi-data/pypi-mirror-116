#!/usr/bin/env python

import sys, os.path, string

def ReadTagsFile( tagfile ):
	tags = []

	try:
		for line in open( tagfile, 'r' ).read().split( '\n' ):
			if line and line[0] not in '#!':
				target, file, where = line.split( '\t', 2 )
				try:
					action = int( where ) - 1
				except ValueError:
					action, junk = where.split( ';"', 1 )
			#	strip /^ and $/
				tags.append( ( target, file, action[2:-2] ) )
	except IOError:
		pass

	return tags

