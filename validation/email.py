#!/usr/bin/env python
# encoding: utf-8
"""
email.py

Created by Robert McFadden on 2008-10-20.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import re

EMAIL_REGEX = email_regex = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}'
remove = '<', '>', '[', ']', ' ', ';', '"', '\'', ':', '/', '\\', ','
common_typos = ('@@', '@'), (',com', '.com')

def validate_email(email):
	global EMAIL_REGEX
	if re.search(EMAIL_REGEX, email):
		return True
	return False

def clean_email(email, **opts):
	clean_email = email
	clean_email = clean_email.strip()
	clean_email = clean_email.lower()

	for cm in common_typos:
		typo = cm[0]
		replace = cm[1]
		clean_email = clean_email.replace(typo, replace)

	for re in remove:
		clean_email = clean_email.replace(re, '')

	return clean_email