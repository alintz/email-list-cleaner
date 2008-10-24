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

class line_object:
	def __init__(self):
		self.fields = []
		self.field_count = 0
		self.sep_count = 0
		self.delim_count = 0