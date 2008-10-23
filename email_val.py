#!/usr/bin/env python
# encoding: utf-8
"""
email_val.py

Created by Robert McFadden on 2008-10-20.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import glob
import re

__DEBUG__ = False

config = {'overwrite_files' : False, 'has_header' : True}
email_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}'

delims = '"', '\'', '`'
seps = '\t', ','

def main():
	do_config()
	
	csv_files = get_csv_files()
	processed = []

	for fil in csv_files:
		pf_def = process_file(fil)
		processed.append(pf_def)
		
	results(processed)

def get_csv_files():
	files = glob.glob("*.csv");
	return files

def process_file(infile):
	good = 0
	bad = 0
	total = 0
	pf = ProcessedFile()
	
	outfile = outfile_name(infile)
	#open file streams
	instream = open(infile, 'r')
	outstream = open(outfile, 'aw')
	
	lf = None #line_format obj
	for line in instream:
		total += 1
		
		if (total == 1):
			lf = parse_line_for_format(line)
			outstream.write(line) #write header
			continue
		
		#get current line format obj
		cur_line_format = parse_line_for_format(line)
		line_consis = parse_line_for_consis(cur_line_format, lf)
		
		#fields = line_to_fields(line, cur_line_format)
		
		if line_consis and parse_line_for_email(line):
			#write to stream
			outstream.write(line)
			good += 1
		else:
			bad += 1
			debug("Line %d is not consistant" % total)
	
	pf.good_emails = good
	pf.bad_emails = bad
	pf.total_emails = total
	
	#close streams	
	instream.close()
	outstream.close()
	
	ow = get_opt('overwrite_files')
	if ow:
		os.rename(outfile, infile)

	return pf
	
def parse_line_for_email(the_line):
	"""
	Parse the input line for at lease one email
	if email found return true else, return false
	"""
	if re.search(email_regex, the_line):
		return True
	
	return False
	
def parse_line_for_consis(format, match_format):
	"""
	Parse the input line for consistancy, basically meaning that it has 
	an even number of delimeters and half the amount of seperators
	"""
	#format = parse_line_for_format(the_line)
		
	even_num_delims = ((format.delim_count % 2) == 0)
	sep_count_correct = (match_format.field_count == format.field_count)
	#print sep_count_correct
	
	return (even_num_delims & sep_count_correct)

	
class line_format:
	def __init__(self):
		self.sep = None
		self.delim = None
		self.field_count = 0
		self.sep_count = 0
		self.delim_count = 0
		self.delim_indexes = None
		
def parse_line_for_format(the_line):
	global delims, seps
	delim = None
	sep = None
	
	is_in = False
	no_delims = None
	i = 0
	
	field_count = 0
	sep_count = 0
	delim_count = 0
	delim_indexes = []
	
	for ch in the_line:
		i += 1 #add to char count
		if not is_in and ch == ' ':
			continue
			
		if ch in delims:
			no_delims = False
			if not delim:
				delim = ch #set delim
			elif ch != delim:
				continue

			if not is_in:
				pass
				#field_count += 1
			
			#add up the delims
			delim_count += 1
			delim_indexes.append(i)
			
			is_in = not is_in #reverse is_in
			
		elif is_in:
			if not no_delims:
				print "no delims...."
			continue
			#pass #print 'reg data', ch	
			
		else: #is sep
			if ch == ' ' or ch == '\n':
				continue
		
			sep_count += 1
			field_count += 1
						
			if not sep: 
				sep = ch
			elif sep and sep != ch:
				#throw inconsis sep error
				pass
			is_in = False
	
	lf = line_format()
	lf.sep = sep
	lf.delim = delim
	lf.field_count = field_count
	lf.delim_count = delim_count
	lf.sep_count = sep_count
	lf.delim_indexes = delim_indexes
	
	#print field_count, 'is the field count '
	#debug("line has %d fields, %d delims and %d seps" % (field_count, delim_count, sep_count))
	return lf

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


def line_to_fields(the_line, format):
	indexes = format.delim_indexes
	fields_to_return = []
	f = None
	
	while indexes:
		pair = indexes[:2]
		st = pair[0]
		en = pair[1] - 1
		f = the_line[st:en]
		fields_to_return.append(f)

		del indexes[:2]
	
	return fields_to_return
	
class FileParts:
	pass
	
class ProcessedFile:
	def __init__(self):
		self.orig_name = ''
		self.new_name = ''
		
		self.good_emails = 0
		self.bad_emails = 0
		self.total_emails = 0
		
		self.bad_email_list = []


def usage(*args):
	#print usage
	if args:
		print "unknown arg(s): ",
		for arg in args:
			print arg,
		print
		
	#reg usage
	print """usage python email_val.py [opts]
	"""
	
	exit()
	
def results(p_res):
	print "Email Parse Results:"
	print "processed %d files" % len(p_res)
	if p_res:
		print "--------------------------------"
		i = 1
		for p_now in p_res:
			print "file %d had %d total lines (emails) %d were good, %d were bad" \
				% (i, p_now.total_emails, p_now.good_emails, p_now.bad_emails)
			i += 1

def do_config():
	avail_opts = {'-o' : "overwrite_files"}
	args = sys.argv
	
	i = 1
	while i < len(args):
		#print args[i], 'is the arg'
		try:
			cur_arg = args[i]
			set_opt(avail_opts[cur_arg])
		except KeyError:
			return usage(cur_arg)
		
		i += 1
	#if len(args) > 0:
	#	for a in sys.argv:
	#		print 'arg', a
	#		try:
	#			set_opt(avail_opts[a])
	#		except KeyError:
	#			return usage()

def set_opt(opt):
	global config
	config[opt] = True
	
def get_opt(opt):
	global config
	
	try:
		value = config[opt]
	except KeyError:
		 value = ''
	return value

def debug(msg):
	global __DEBUG__
	if __DEBUG__:
		print msg

if __name__ == '__main__':
	main()

