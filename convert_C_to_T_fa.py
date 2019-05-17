##input: python convert_C_to_T_fa.py [path/indexFile] [optional output directory]
##example: python convert_C_to_T_fa.py ./example/index.fa ./converted_index
#"""author = Yeming 04-30-2019"""
import re
import sys
import os

with open(sys.argv[1]) as f:
	line = f.read().splitlines()

pathname = os.path.split(sys.argv[1])
outputID = 'converted_' + pathname[-1]

if len(sys.argv) == 3:
	if not os.path.exists(sys.argv[2]):
		os.system('mkdir {}'.format(sys.argv[2]))
	converted = open(os.path.join(sys.argv[2],outputID),'w')
else:
	converted = open(outputID,'w')

##take out every 2 lines that
##begin with ">" for the 1st line
a = 0

for line[a] in line:
	if line[a].startswith(">"):		##verifying format
		converted.write(line[a] + '\n')
	else:
		i = 0
		seq_str = line[a]
		seq_converted = []
		for i in range(0,len(line[a])):
			if seq_str[i] == 'C':
				seq_converted += "T"
			elif seq_str[i] == 'c':
				seq_converted += "t"
			else:
				seq_converted += seq_str[i]
			i += 1
		seq_join = ''.join(seq_converted)
                converted.write(seq_join + '\n')

	a += 1		
