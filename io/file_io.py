#!/usr/bin/env python
# encoding: utf-8
"""
file_io.py

Created by Robert McFadden on 2008-10-20.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import glob

def outfile_name(infile):
	outfile = infile
		
	parts = infile.split('.')
	ext = parts.pop()
	
	first_pass = True
	while parts:
		if first_pass:
			base = parts.pop(0)
			first_pass = False
		else:
			base += '.' + parts.pop(0)
	
 	tries = 1
	while(glob.glob(outfile)):
		outfile = base + str(tries) + '.' + ext
		tries += 1
		
	return outfile
