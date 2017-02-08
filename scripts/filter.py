# filter.py
# Input: file of indices, file with a table
# Output: filtered table

import sys

USAGE = "{0} filterfile tablefile outfile" .format(sys.argv[0])

def parse_args(argv):
	if len(argv) != 4:
		print USAGE
		exit(1)
	filter_file = argv[1]
	table_file = argv[2]
	outfile  = argv[3]
	return filter_file, table_file, outfile

def grab_header(filename):
	with open(filename, 'r') as f:
		header = f.readline()
	return header

def create_filter(filename):
	included = []
	with open(filename, 'r') as f:
		lines = f.readlines()
	for line in lines:
		included.append(line.strip())
	return included

def get_dlm(line):
	dlms = [',','\t',' ']
	for dlm in dlms:
		fields = line.strip().split(dlm)
		if len(fields) > 1:
			return dlm
	return ','

def filter_table(included, table_file):
	out = ""
	with open(table_file, 'r') as f:
		lines = f.readlines()[1:]
	dlm = get_dlm(lines[0])
	for line in lines:
		ID = line.strip().split(dlm)[0]
		if ID in included:
			out += line
	return out
		
def write_to_file(subset, outfile):
	with open(outfile, 'w') as f:
		f.write(subset)

# main
filter_file, table_file, outfile = parse_args(sys.argv)
header = grab_header(table_file)
included = create_filter(filter_file)	
subset = filter_table(included, table_file)
write_to_file(header + subset, outfile)
