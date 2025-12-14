#!/bin/bash
# calc_delta.sh RUN_DIR

if [ -z "$1" ]; then
  echo "Please provide a directory as argument!"
  exit 0
fi
myresdir=$1

#SCRIPTS_DIR=/Users/torrentm/WORK/JTH-TABLE/ABINIT/RUN-TOPAZE/SCRIPTS

myroot=$PWD
SCRIPTS_DIR=${myroot}/SCRIPTS

cd ${myroot}

rm -rf ${myroot}/${myresdir}_eos.txt
rm -rf ${myroot}/${myresdir}_delta.txt

for ff in ${myroot}/${myresdir}/*; do
 
  sp=`basename ${ff}`
  cd ${myroot}/${myresdir}/${sp}

  ${SCRIPTS_DIR}/extract_abinit V etot_eV ${sp}.abo> ${sp}.fit
  ${SCRIPTS_DIR}/eosfit.py ${sp}.fit
  ${SCRIPTS_DIR}/build_delta.py ${sp}.fit.eosout ${myroot}/${myresdir}_eos.txt

done

${SCRIPTS_DIR}/calcDelta.py ${myroot}/${myresdir}_eos.txt ${SCRIPTS_DIR}/WIEN2k.txt --stdout > ${myroot}/${myresdir}_delta.txt
