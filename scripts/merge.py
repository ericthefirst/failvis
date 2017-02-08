# merge.py
# 
# Input: list of files stored as simple tables (CSV/TSV/SSV agnostic), outfile name
# Output: file with all fields from all files
# Warning: if the same feature appears in multiple files, the value from the first file is kept
# 
# Eric Welch
# February 2017

import sys
from os.path import isfile

stars = {}    # key is ID, contains all fields, in the order of fields
fields = []   # list of all star fields in order so we can print them in a reasonable way
DLM = ','



def parse_args(argv):
	if len(argv) < 3:
		print "Usage: {0} infiles... outfile".format(argv[0])
		exit(1)
	infiles = argv[1:-1]
	outfile = argv[-1]
	return infiles, outfile



def process_input(infiles):
	for infile in infiles:
		with open(infile, 'r') as f:
			lines = f.readlines()
		dlm = get_dlm(lines[0])
		skip = add_fields(lines[0], dlm)
		add_data(lines[1:], dlm, skip)

def get_dlm(line):
	dlms = [',','\t',' ']
	for dlm in dlms:
		fields = line.strip().split(dlm)
		if len(fields) > 1:
			return dlm
	return ','

def add_fields(line, dlm):
	skip = []
	field_names = line.strip().split(dlm)
	for i, field_name in enumerate(field_names):
		if field_name in fields:
			skip.append(i)
			continue
		fields.append(field_name)
	return skip
			
def add_data(lines, dlm, skip):
	for line in lines:
		fields = line.strip().split(dlm)
		ID = fields[0]
		for i, value in enumerate(fields):
			if i in skip:
				continue
			if not ID in stars:
				stars[ID] = []
			stars[ID].append(value)




# all data for all stars combined into a string
def merge_data():
	data = ""
	for star in stars:
		data += ','.join(stars[star]) + '\n'
	return data
				
			

def write_to_outfile(data, outfile):
	with open(outfile, 'w') as f:
		f.write(','.join(fields) + '\n')
		f.write(data)


infiles, outfile = parse_args(sys.argv)
if isfile(outfile):
	print "Output file {0} already exists, renaming as {0}-prime".format(outfile)
	outfile = "{0}-prime".format(outfile)
print "Using input files {0} and output file {1}".format(infiles, outfile)
process_input(infiles)
data = merge_data()
write_to_outfile(data, outfile)
