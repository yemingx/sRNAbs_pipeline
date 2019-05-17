#!/bin/bash
set -e
set -u
set -o pipefail
#"""author = Yeming 04-30-2019"""

##pipeline settings
thread='4'
example_folder='example'
converted_index_folder='converted_index'
outputs_folder='outputs'
projects_dir=$PWD
index="${projects_dir}/${example_folder}/index.fa"

if [ ! -d "${projects_dir}/${converted_index_folder}" ] || [ ! -d "${projects_dir}/${outputs_folder}" ]; then
mkdir ${projects_dir}/${converted_index_folder} ${projects_dir}/${outputs_folder}
fi

echo -e "\n ***preparing converted reference*** \n"
python convert_C_to_T_fa.py $index ${projects_dir}/${converted_index_folder}
bowtie2-build -q ${projects_dir}/${converted_index_folder}/converted_index.fa \
			  ${projects_dir}/${converted_index_folder}/converted_index.fa
echo "python convert_C_to_T_fa.py $index ${projects_dir}/${converted_index_folder}"
echo "bowtie2-build -q ${projects_dir}/${converted_index_folder}/converted_index.fa \
			  ${projects_dir}/${converted_index_folder}/converted_index.fa"

echo -e "\n ***organize sample names*** \n"
seqfile=($(ls ${projects_dir}/${example_folder}/AA*_L*))
echo ${seqfile[@]}
samplename1=(${seqfile[@]%_L*})
samplename=(${samplename1[@]##*/})
samplename=($(printf "%q\n" "${samplename[@]}"|sort -u))
echo ${samplename[@]}


for i in ${samplename[@]}; do
	echo ${projects_dir}/${example_folder}/${i}

	echo -e "\n ***align converted sample to converted index*** \n"
	if [ ! -f "${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.sam" ]; then
	python convert_C_to_T_fastq.py ${projects_dir}/${example_folder}/${i}_L001_R1_trim.fastq ${projects_dir}/${outputs_folder}
	bowtie2 -L 16 -i S,0,0.2 -p ${thread} -x ${projects_dir}/converted_index/converted_index.fa \
			-U ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq \
			-S ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.sam
	echo "	python convert_C_to_T_fastq.py ${projects_dir}/${example_folder}/${i}_L001_R1_trim.fastq ${projects_dir}/${outputs_folder}"
	echo "	bowtie2 -L 16 -i S,0,0.2 -p ${thread} -x ${projects_dir}/converted_index/converted_index.fa \
			-U ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq \
			-S ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.sam"
	fi

	echo -e "\n ***sort sam file by seq ID*** \n"
	if [ ! -f "${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.bam" ]; then
	#convert to bam file
	samtools view -@ ${thread} -bS ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.sam > \
			 ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.bam
	#sort reads by names
	samtools sort -@ ${thread} -n ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.bam \
					 -o ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.bam  
	#convert sorted bam file to sam file
	samtools view -@ ${thread} -o ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.sam \
					 ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.bam
	echo "  samtools view -@ ${thread} -bS ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.sam > \
			 ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.bam  "
	echo "	samtools sort -@ ${thread} -n ${projects_dir}/${outputs_folder}/converted_${i}_L001_R1_trim.fastq.bam \
					 -o ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.bam  "
	echo "	samtools view -@ ${thread} -o ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.sam \
					 ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.bam  "
	fi

    #methylation table generated based on sorted sam file, sample fastq, and reference index
	echo -e "\n ***generating methylation table*** \n"
	if [ ! -f "${projects_dir}/${outputs_folder}/MethyTable_${i}_L001_R1_trim.fastq.txt" ]; then
	python methy_report.py \
	       ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.sam \
	       $index \
	       ${projects_dir}/${example_folder}/${i}_L001_R1_trim.fastq \
	       ${projects_dir}/${outputs_folder}
	echo "	python methy_report.py \
	       ${projects_dir}/${outputs_folder}/sorted_converted_${i}_L001_R1_trim.fastq.sam \
	       $index \
	       ${projects_dir}/${example_folder}/${i}_L001_R1_trim.fastq \
	       ${projects_dir}/${outputs_folder}"	       
	fi

done
##run with log file ./sRNAbs_pipeline.sh 2>&1 | tee make.log