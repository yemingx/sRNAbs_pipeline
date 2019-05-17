##input: python convert_C_to_T_fastq.py [path/indexFile] [optional output directory]
##example: python convert_C_to_T_fastq.py ./example/AAwt-FFsrna-TTspe-SS3_L001_R1_trim.fastq ./outputs
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
	if line[a].startswith("@") and line[a+2].startswith("+"):	##verifying format
		converted.write(line[a] + '\n')
		i = 0
		seq_str = line[a+1]
		seq_converted = []
		for i in range(0,len(line[a+1])):
			if seq_str[i] == 'C':
				seq_converted += "T"
			else:
				seq_converted += seq_str[i]
		seq_join = ''.join(seq_converted)
        	converted.write(seq_join + '\n' + line[a+2] + '\n' + line[a+3] + '\n')

	a += 1		
