#!/usr/bin/env python
# encoding: utf-8
"""
algor.py

Created by Robert McFadden on 2008-10-22.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os

delims = '\'', '"'
seps = ',', '\t'
reject = '{', '}'

def main():
	parse_test()
	
def parse(the_line):
	the_line = the_line.strip()
	
	#cc = char count, dc = delim count, sc = sep count, fc= field count
	cc = dc = sc = fc = 0
	is_in = False
	nf = False
	delim = None 
	sep = None
	
	buff = ''
	fields = []
	for ch in the_line:
	
		cc += 1
		if cc == 1:
			pass #fc += 1
			
		elif not delim:
			return parse(add_delims_to_line(the_line))
			
		if ch in delims and (not delim or delim == ch):
			if not delim: 
				delim = ch
				
			if delim and delim == ch: #consis delim
				dc += 1
				is_in = not is_in
				if not is_in:
					fc += 1
					fields.append(buff)
					buff = ''
				continue 

		elif not is_in:
			if ch in seps:
				if not sep: 
					sep = ch
				
				if sep and sep == ch:
					sc += 1
				
		if is_in: #is_in
			buff += ch
						
	print fields
	print
	
	assert not dc % 2
	assert (dc/2) - 1 is sc
	assert fc is len(fields)

	print "results: cc=%d, dc=%d, sc=%d, fc=%d" % (cc, dc, sc, fc)
	
class line_object:
	def __init__(self):
		self.fields = []
		self.field_count = 0
		self.sep_count = 0
		self.delim_count = 0
		
def add_delims_to_line(the_line):
	#does line have any seps?
	global delims, seps
	
	the_sep = None
	the_delim = None
	delim_list = list(delims)
	
	for s in seps:
		if the_line.count(s):
			the_sep = s
			break
			
	while delim_list:
		the_delim = delim_list.pop(0)
		if the_line.count(the_delim):
			break
	
	if not the_delim:
		#throw ex here!!!
		print "CANT DO IT..."
		
	if not the_sep:
		print "CANT DO IT..."
	
	#step one, surround w delims
	the_line = the_line.strip()
	the_line = the_line.center(len(the_line)+2, the_delim)
	
	sps = the_sep + ' '
	while the_line.count(sps):
		the_line = the_line.replace(sps, the_sep)
	
	#step two, surround the seps w delims
	dsd = the_delim + the_sep + ' ' + the_delim
	the_line = the_line.replace(the_sep, dsd)
	
	return the_line
	

def parse_test():
	l = [ '"na\'me", "email", "company"'
	"name, email, company"
	"'name',   'e',   'co'" ]
	
	for _l in l:
		parse(_l)
	
		
	
if __name__ == '__main__':
	main()

