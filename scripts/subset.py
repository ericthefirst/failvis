# generate_subset_indices.py

from sys import argv
from random import shuffle

USAGE = "{0} infile class_size idxfile".format(argv[0])

def process_args(args):
	if len(args) != len(USAGE.split(" ")):
		print "Usage: {0}".format(USAGE)
		exit(1)
	infile = args[1]
	class_size = int(args[2])
	outfile = args[3]
	return infile, class_size, outfile


def get_dlm(line):
	dlms = [',','\t',' ']
	for dlm in dlms:
		fields = line.strip().split(dlm)
		if len(fields) > 1:
			return dlm
	return ','

# in case we want to switch to using a percentage at some point
def get_class_counts(lines):
	class_counts = {}
	dlm = get_dlm(lines[0])
	for line in lines:
		fields = line.strip().split(dlm)
		cls = int(fields[-1])
		if not cls in class_counts:
			class_counts[cls] = 1
		else:
			class_counts[cls] += 1
	return class_counts



def generate_IDs(infile, class_size):
	with open(infile, 'r') as f:
		lines = f.readlines()
	dlm = get_dlm(lines[0])
	lines = lines[1:]
	IDs = []
	class_counts = get_class_counts(lines)   # note that we
	classes = [[] for _ in range(len(class_counts))]
	for line in lines:
		fields = line.strip().split(dlm)
		ID = int(fields[0])
		classes[int(fields[-1])].append(ID)
	for i, cls in enumerate(classes):
		shuffle(cls)
		print "Class {0} has {1} elements in its subset out of {2}".format(i, min(class_size, class_counts[i]), class_counts[i])
		classes[i] = cls[:min(class_size, class_counts[i])]
	for cls in classes:
		for ID in cls:
			IDs.append(ID)
	return IDs


			
def write_IDs_to_file(IDs, outfile):
	with open(outfile, 'w') as f:
		for ID in IDs:
			f.write("{0}\n".format(ID))


# MAIN 
infile, class_size, outfile = process_args(argv)
IDs = generate_IDs(infile, class_size)
write_IDs_to_file(IDs, outfile)
