#!/usr/bin/env python
import re
import csv
import operator
import sys
import os
#"""author = Yeming 04-30-2019"""
##input: python methy_report.py [path/sorted_converted_sam_file] [path/index] [path/sample fastq] [optional output directory]
##example: python methy_report.py ./outputs/sorted_converted_AAwt-FFsrna-TTspe-SS3_L001_R1_trim.fastq.sam ./example/index.fa ./example/AAwt-FFsrna-TTspe-SS3_L001_R1_trim.fastq ./outputs

##open sorted_converted_SAM_file, input sample name
sam = open(sys.argv[1],'r')
csv1 = csv.reader(sam, delimiter='\t')	

##read reference index
with open(sys.argv[2] , 'r') as f1:
	index = f1.read().splitlines()

##build length index for each sRNA
a = 0
dict_index = {}
for index[a] in index:
	if index[a].startswith('>'):
		dict_index[index[a]] = len(index[a+1])
	a += 1

#open original fastq/fasta file
with open(sys.argv[3],'r') as f2:
	sample = f2.read().splitlines()

a = 0
dict_sample = {}
if sample[a].startswith("@") and sample[a+2].startswith("+") and a < 1:
	print ('\nInput sample is a fastq file. \n')
	for sample[a] in sample:
		if sample[a].startswith('@'):
			seqID_total = sample[a].split()
			seqID_head = seqID_total[0]
			seqID = seqID_head[1:]
			i = 0
			seq_str = sample[a+1]
			seq_converted = []
			for i in range(0,len(sample[a+1])):
				if seq_str[i] == 'C':
					seq_converted += '1'
				else:
					seq_converted += '0'
			seq_join = ''.join(seq_converted)
			dict_sample[seqID] = seq_join
		a += 1
elif sample[a].startswith(">") and a < 1:
	print ('\nInput sample is a fasta file.\n')
	for sample[a] in sample:
		if sample[a].startswith('>'):
			seqID_head = sample[a]
			seqID = seqID_head[1:]
			i = 0
			seq_str = sample[a+1]
			seq_converted = []
			for i in range(0,len(sample[a+1])):
				if seq_str[i] == 'C':
					seq_converted += '1'
				else:
					seq_converted += '0'
			seq_join = ''.join(seq_converted)
			dict_sample[seqID] = seq_join
		a += 1


##generate methylation report, row[0] seqID, row[2] geneID, row[3] pos, row[5] cigar
outputID = 'MethyTable_' + os.path.split(sys.argv[3])[-1] + '.txt'

if len(sys.argv) == 5:
	if not os.path.exists(sys.argv[4]):
		os.system('mkdir {}'.format(sys.argv[4]))
	report_txt = open(os.path.join(sys.argv[4],outputID),'w')
else:
	report_txt = open(outputID,'w')
report_txt.write('seqID\tgeneID\tcigar\tmapping_start_pos\tread_length\tindex_length\tsplit_site_report\n')
for row in csv1:
	if row[2] == '*' or row[5] == '*':
		''
	else:
		raw_seq = dict_sample[row[0]]
		methy_array = re.findall(r'\d',raw_seq)
		methy_str = raw_seq
		cigar_str = row[5]
		cigar_array = []
		deletion = '0000000000000000000000000000000000'
		real_site = []


		if "I" not in cigar_str and "D" not in cigar_str:
			real_site = methy_str
			site = ''.join(real_site)

		else:
			cigar_array = re.findall(r'(\d+)(\w)', row[5])
			i = 0
			for i in range(0,len(cigar_array)):
				cigar_split = cigar_array[i]
				cigar_tuple = int(cigar_split[0])

				if 'M' == cigar_split[1]:
					real_site += methy_str[:cigar_tuple]
					methy_str = methy_str[cigar_tuple:]

				if 'D' == cigar_split[1]:
					real_site += deletion[:cigar_tuple]

				if 'I' == cigar_split[1]:
					methy_str = methy_str[cigar_tuple:]
						
			site = ''.join(real_site)	

		pos_sam = row[3]
		i = int(row[3]) - 1
		zeros1 = i * '0'
		zeros2 = 200 * '0'
		if i > 0:
			POS_site = zeros1 + site + zeros2
		else:
			POS_site = site + zeros2
		k = 0
		final_site_array = []
		for k in range(0,200):  ##break str into array
			final_site_array += POS_site[k]
			k += 1
		final_site = '\t'.join(final_site_array)
		##final report: seqID, geneID, cigar, mapping_start_pos, read_length, index_length, split_site_report
		report_txt.write(row[0] +'\t' + row[2] + '\t' + row[5] + '\t' + row[3] + '\t' + str(len(site)) + '\t' + str(dict_index['>' + row[2]]) + '\t' + final_site +'\n')

report_txt.close
sam.close
