#!/bin/bash

#MSUB -r jth           # Name of the job
#MSUB -n 384           # Number of MPI processes
#MSUB -c 1             # Number of threads
#MSUB -T 15000         # Max. time in seconds
#MSUB -q milan         # Partition: milan (cpu) or a100 (gpu)
##MSUB -Q test

#Dont touch this
#MSUB -A dam00000      # Project id 
#MSUB -o %I.o          # Standard output. %I is the job id
#MSUB -e %I.e          # Error output.    %I is the job id
#MSUB -m work,scratch  # List of used file systems

ABINIT_EXE=/ccc/scratch/cont002/dam/torrent/abinit-10.4.7/build/src/98_main/abinit

source /ccc/scratch/cont002/dam/torrent/abinit-10.4.7/build/topaze_env_nov25.sh

myroot=$PWD

cd ${myroot}

for ff in ${myroot}/INPUT/*; do
 
  IFS='.' read -r -a parts <<< `basename ${ff}`
  sp=${parts[0]}
  
  mkdir -p ${myroot}/RUN/${sp}

  /usr/bin/cp -rf ${myroot}/INPUT/${sp}.in ${myroot}/RUN/${sp}/${sp}.abi
  echo -e "\npseudos \"${myroot}/PSEUDOS/${sp}.GGA_PBE-JTH.xml\"\n" >> ${myroot}/RUN/${sp}/${sp}.abi
  echo -e "wfoptalg 114  npfft 1  npband 1" >> ${myroot}/RUN/${sp}/${sp}.abi
  echo -e "npkpt ${SLURM_NTASKS}\n" >> ${myroot}/RUN/${sp}/${sp}.abi

  cd ${myroot}/RUN/${sp}
  
  ccc_mprun ${ABINIT_EXE} ${sp}.abi > ${sp}.log
  
  cd ${myroot}

done

