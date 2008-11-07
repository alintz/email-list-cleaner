#!/usr/bin/env python
# encoding: utf-8
"""
email_val.py

Created by Robert McFadden on 2008-10-20.
Copyright (c) 2008. All rights reserved.
"""

import sys
import os
import glob
import re

from io.file_io import outfile_name
from validation.email import validate_email, clean_email

__DEBUG__ = False
config = {'overwrite_files' : False, 'has_header' : True}
FILE_PATH = "RDM_EMAIL_REPOS_PATH"

delims = '"', '\'', '`'
seps = '\t', ','

def main():
	do_config()
	
	csv_files = get_csv_files()
	processed = []

	for fil in csv_files:
		#try:
		pf_def = process_file(fil)
		processed.append(pf_def)
        #except:
		#	print "Had an ex"
			#TODO: handle ex properly
		#	pass
		
	results(processed)

def get_csv_files():
	global FILE_PATH
	d = os.getenv(FILE_PATH)
	d = "/Users/d3mcfadden/Desktop/email_list/"

	match_ext = '*.csv'
	
	p = '%s/%s' % (d, match_ext)
	files = glob.glob(p);
	print len(files), "num of files"
	return files

def process_file(infile):
	global config
	
	good = 0
	bad = 0
	cleaned = 0
	total = 0
	pf = ProcessedFile()
	
	outfile = outfile_name(infile)
	#open file streams
	instream = open(infile, 'r')
	outstream = open(outfile, 'aw')
	
	ff = None #file_format obj
	for line in instream:
		total += 1	
		
		if (total == 1 and config['has_header']):
			ff = get_file_format(line)
			if ff.email_field == -1:
				#get it from user
				fields = parse(line)
				email_field = ask_user_which_field_is_email(fields)
				email_field -= 1 #comp for 0 index
				ff.email_field = email_field

			outstream.write(line) #write header
			continue

		fields = parse(line, ff)
		email = fields[ff.email_field]
		email = clean_email(email)
		
		print total, " -- ", len(fields)
		
		if validate_email(email):
			good += 1
			if email != fields[ff.email_field]:
				cleaned += 1
				line = line.replace(fields[ff.email_field], email)
			
			#TODO: need to get the line back from feilds, but for now just write the line
			outstream.write(line)
		else:
			bad += 1
			
	pf.good_emails = good
	pf.bad_emails = bad
	if config['has_header']:
		total -= 1
	pf.total_emails = total
	
	#close streams	
	instream.close()
	outstream.close()
	
	ow = get_opt('overwrite_files')
	if ow:
		os.rename(outfile, infile)

	return pf

def parse(the_line, format=None):
	"""
	doc string needed...
	"""
	
	the_line = the_line.strip()

	#cc = char count, dc = delim count, sc = sep count, fc= field count
	cc = dc = sc = fc = 0
	is_in = False
	nf = False
	delim = None 
	sep = None
	
	if format:
		delim = format.delim
		sep = format.sep
	
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
	
	format.delim = delim
	format.sep = sep
	
	return fields

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
		if  not the_line.count(the_delim):
			break

	if not the_delim:
		#throw ex here!!!
		print "CANT DO IT..."

	#step one, surround w delims
	the_line = the_line.strip()
	the_line = the_line.center(len(the_line)+2, the_delim)
	
	if not the_sep: #single field line
		return the_line
	
	#multi-field line
	sps = the_sep + ' '
	while the_line.count(sps):
		the_line = the_line.replace(sps, the_sep)

	#step two, surround the seps w delims
	dsd = the_delim + the_sep + ' ' + the_delim
	the_line = the_line.replace(the_sep, dsd)

	return the_line

def get_file_format(the_line):
	email_field = -1
	delim = None
	sep = None
	
	fields = parse(the_line)
	debug(fields)
	
	i = 0
	for f in fields:
		if validate_email(f):
			email_field = i
			break
		i += 1
		
	ff = file_format()
	ff.field_count = len(fields)
	ff.email_field = email_field
	
	if ff.email_field == -1 and i == 1: #only one field, assume email
		ff.email_field = 0
		
	return ff

#[depricated]
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

def ask_user_which_field_is_email(fields):
	print '\a' #ding
	prompt = 'Please pick the email field:\n'
	i = 1
	for fi in fields:
		prompt += '%d: %s\n' % (i, fi)
		i += 1
	prompt += '>>> '

	valid = range(1,len(fields)+1)
	while True:
		choice = int(raw_input(prompt))
		if choice in valid:
			return choice
		else:
			print 'bad choice...'

#----------------------------
#Data Model
#----------------------------
class ProcessedFile:
	def __init__(self):
		self.orig_name = ''
		self.new_name = ''
		
		self.good_emails = 0
		self.bad_emails = 0
		self.total_emails = 0
		
		self.bad_email_list = []

class line_format:
	def __init__(self):
		self.sep = None
		self.delim = None
		self.field_count = 0
		self.sep_count = 0
		self.delim_count = 0
		self.delim_indexes = None

class file_format:
	def __init__(self):
		self.field_count = 0
		self.email_field = -1

		self.delim = None
		self.sep = None

class line_object:
	def __init__(self):
		self.fields = []
		self.field_count = 0
		self.sep_count = 0
		self.delim_count = 0
		
#-------------------------------------

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
			per_good = (p_now.good_emails / p_now.total_emails) * 100
			per_bad = (p_now.bad_emails / p_now.total_emails) * 100
			
			print "file %d had %d total lines (emails) %d were good (%0.2f%%), %d were bad" \
				% (i, p_now.total_emails, p_now.good_emails, per_good, p_now.bad_emails)
			i += 1



#----------------------------------------------------
# Config
#----------------------------------------------------
def do_config():
	avail_opts = {'-o' : "overwrite_files", '-d' : 'debug'}
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

