Test sample:

AAwt-FFsrna-TTspe-SS3_L001_R1_trim.fastq
First 100000 reads of the trimmed WT mouse sperm sRNA bs fastq


Environment:

ubuntu 18.04
macOS Mojave 10.14.4 (18E226)

Bowtie 2 version 2.3.4.3

Python 2.7.15rc1 (default, Nov 12 2018, 14:31:15) 
[GCC 7.3.0] on linux2

Program: samtools (Tools for alignments in the SAM format)
Version: 1.9 (using htslib 1.9)



Get started:
1. Put sRNA fastq sample and fasta reference index in the same folder (example folder).

2. Put the scripts in the same directory with the example folder.
   Should have the following four scripts: 

   convert_C_to_T_fa.py
   convert_C_to_T_fastq.py
   methy_report.py
   sRNAbs_pipeline.sh

3. Make the sRNAbs_pipeline.sh executable and run the script.

   Sudo chmod 755 sRNAbs_pipeline.sh

4. Two folders will be generated. 
   The "converted_index" folder contains the C to T converted bowtie2 index.
   The "outputs" folder contains the methylation table (MethyTable_SampleFastq.txt) and other intermediate files.
