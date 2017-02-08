from random import random, randint
from sys import argv


if len(argv) < 3:
	print "Usage: {0} outfile n".format(argv[0])
	exit(1)

n = int(argv[2])
with open(argv[1], 'w') as f:
	f.write("ID,u-g,g-i,i-r,r-z,class\n")
	for i in range(n):
		f.write("{0},{1},{2},{3},{4},{5}\n".format(1000+i, random(), random(), random(), random(), randint(0, min(3,n))))
