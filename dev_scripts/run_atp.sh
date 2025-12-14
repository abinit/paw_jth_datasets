#!/bin/bash

# ===================================
# Variables to be adjusted

#XC="PBE" ; XC_TYPE="GGA" ; NPT="2000"
 XC="PBE" ; XC_TYPE="GGA" ; NPT="500"
#XC="PW"  ; XC_TYPE="LDA" ; NPT="2000"
#XC="PW"  ; XC_TYPE="LDA" ; NPT="500"

WITH_UPF="yes"
#WITH_UPF="no"

WITH_COREWF="yes"
#WITH_COREWF="no"

ATOMPAW_EXE=/opt/homebrew/bin/atompaw

# ===================================

if [ "${XC}" == "PW" ]; then
  XC_NAME="LDA"
else
  XC_NAME=${XC}
fi

INPUT_DIR="INPUT-"${XC_NAME}
PSEUDO_DIR="PSEUDOS-"${XC_NAME}"_"${NPT}
COREWF_DIR="COREWF-"${XC_NAME}"_"${NPT}
RUN_DIR="RUN-"${XC_NAME}"_"${NPT}

myroot=$PWD
cd ${myroot}

for ff in ${myroot}/${INPUT_DIR}/*/*; do
 
  fname=`basename ${ff}`
  IFS='.' read -r -a parts <<< `basename ${ff}`
  sp=${parts[0]}
  if [[ "${fname}" == *"JTH_sp."* ]]; then
    SUF1="-SP" ; SUF2="_sp"
  else
    SUF1="" ; SUF2=""
  fi

  PSEUDO_DIR_SP=${myroot}/${PSEUDO_DIR}${SUF1}
  COREWF_DIR_SP=${myroot}/${COREWF_DIR}${SUF1}
  RUN_DIR_SP=${myroot}/${RUN_DIR}/${sp}${SUF2}

  mkdir -p ${RUN_DIR_SP}
  rm -rf ${RUN_DIR_SP}/*

  /bin/cp -rf ${ff} ${RUN_DIR_SP}/${sp}.input
  if [ "${WITH_COREWF}" == "yes" ]; then
    sed -i -e 's/default/default prtcorewf/' ${RUN_DIR_SP}/${sp}.input
  fi
  sed -i -e 's/ withsplgrid 500//g' ${RUN_DIR_SP}/${sp}.input
  if [ "${NPT}" == "500" ]; then
    sed -i -e 's/default/default withsplgrid 500/g' ${RUN_DIR_SP}/${sp}.input
  fi
  cd ${RUN_DIR_SP}
  ${ATOMPAW_EXE} < ${sp}.input > ${sp}.log
  
  mkdir -p ${PSEUDO_DIR_SP}
  /bin/cp -rf ${RUN_DIR_SP}/${sp}*-paw.xml \
              ${PSEUDO_DIR_SP}/${sp}.${XC_TYPE}_${XC}-JTH${SUF2}.xml

  if [ "${WITH_UPF}" == "yes" ]; then
    /bin/cp -rf ${RUN_DIR_SP}/${sp}*-paw.UPF \
                ${PSEUDO_DIR_SP}/${sp}.${XC_TYPE}_${XC}-JTH${SUF2}.UPF
  fi

  if [ "${WITH_COREWF}" == "yes" ]; then
    mkdir -p ${COREWF_DIR_SP}
    /bin/cp -rf ${RUN_DIR_SP}/${sp}*-paw.corewf.xml \
                ${COREWF_DIR_SP}/${sp}.${XC_TYPE}_${XC}-JTH${SUF2}.corewf.xml
  fi

  cd ${myroot}

done
