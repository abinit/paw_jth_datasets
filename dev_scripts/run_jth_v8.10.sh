#!/bin/bash

#MSUB -r jth           # Name of the job
#MSUB -n 384           # Number of MPI processes
##MSUB -N 1             # Number of nodes
#MSUB -c 1             # Number of threads
#MSUB -T 1800          # Max. time in seconds
#MSUB -q milan         # Partition: milan (cpu) or a100 (gpu)
#MSUB -Q test

#Dont touch this
#MSUB -A dam00000      # Project id 
#MSUB -o %I.o          # Standard output. %I is the job id
#MSUB -e %I.e          # Error output.    %I is the job id
#MSUB -m work,scratch  # List of used file systems

ABINIT_EXE=/ccc/scratch/cont002/dam/torrent/abinit-8.10.1/build/src/98_main/abinit

source /ccc/scratch/cont002/dam/torrent/abinit-8.10.1/build/v8.10_env.sh

myroot=$PWD

cd ${myroot}

for ff in ${myroot}/INPUT/*; do
 
  IFS='.' read -r -a parts <<< `basename ${ff}`
  sp=${parts[0]}
  
  mkdir -p ${myroot}/RUN/${sp}

  /usr/bin/cp -rf ${myroot}/INPUT/${sp}.in ${myroot}/RUN/${sp}
  echo -e "\nnp_slk 0" >> ${myroot}/RUN/${sp}/${sp}.in
  echo -e "wfoptalg 114" >> ${myroot}/RUN/${sp}/${sp}.in
  echo -e "npband 1" >> ${myroot}/RUN/${sp}/${sp}.in
  echo -e "npfft 1" >> ${myroot}/RUN/${sp}/${sp}.in
  echo -e "npkpt ${SLURM_NTASKS}\n" >> ${myroot}/RUN/${sp}/${sp}.in
  sed -i -e 's/chksymtnons 0//g' ${myroot}/RUN/${sp}/${sp}.in

  echo "${sp}.in" > ${myroot}/RUN/${sp}/${sp}.files
  echo "${sp}.abo" >> ${myroot}/RUN/${sp}/${sp}.files
  echo "${sp}i" >> ${myroot}/RUN/${sp}/${sp}.files
  echo "${sp}o" >> ${myroot}/RUN/${sp}/${sp}.files
  echo "${sp}p" >> ${myroot}/RUN/${sp}/${sp}.files
  echo -e "${myroot}/PSEUDOS/${sp}.GGA_PBE-JTH.xml" >> ${myroot}/RUN/${sp}/${sp}.files

  cd ${myroot}/RUN/${sp}
  
  ccc_mprun ${ABINIT_EXE} < ${sp}.files > ${sp}.log
  
  cd ${myroot}

done

