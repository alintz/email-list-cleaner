seps = ',' , '	'
delims = '\'', '"'

def main():
	l = '"email", "comp\'any"'
	l2 = "email"
	l3 = '"email"'
	l4 = '"Email Address"'
	l5 = 'Email Address'
	l8 = "'Email Address'"
	l6 = "bob o'hare"
	l7 = "billy's great co, inc."
	l9 = "'billys great co, inc.', 'billy here'"
	l10 = "billy's tab co, inc	new name"
	lines = [l, l2, l3, l4, l5, l6, l7]
	parse(l7)
	return

	for line in lines:
		parse(line)
		
def parse(the_line):
	the_line = the_line.strip()
	#nc = num chars, nd = num delims, ns = num seps, nf = num fields - pretty much dep on seps
	nc = nd = ns = nf = 0
	
	is_in = False
	delim = None
	sep = None
	
	for ch in the_line:
		#print 'delim is', delim
		#if is_in:
		#	print "in"
		#else:
		#	print "out"
		if ch == ' ' or ch == '\n':
			nc += 1
			continue
			
		if ch in delims:
			if not delim and (nc == 0): #only set delim if it is first char on line
				delim = ch
			if delim and (delim == ch):
				nd += 1
				is_in = not is_in
				print "delim found", is_in
		
		elif ch in seps:
			if not sep:
				sep = ch
			
			if ch == sep and sep:
				ns += 1
				is_in = False
			
			#print "sep found"
		
		elif not is_in and False:
			print "in here..."
			is_in = True
			nf += 1
			#print "new field at ", ch, " char#", nc
			
		nc += 1
	print
	print "results: nc = %d, nd = %d, ns = %d, nf = %d" % (nc, nd, ns, nf)
	
if __name__ == '__main__':
	main()