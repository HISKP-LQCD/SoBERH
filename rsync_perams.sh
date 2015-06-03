#!/bin/bash
# Script to rsync perambulators from SRC to a specific folder TRG config-wise
# The script assumes a 4 digit configuration number 

# Paths
SRC=/hiskp2/helmes/A100.24/strange_225
TRG=/hiskp2/perambulators/A100/nev_120/strange_225

# Range of configurations
BGN=501
END=2997
DST=8
for (( CFG=${BGN}; CFG<=${END}; CFG+=${DST} )); do 
  C=`printf %04d ${CFG}`
  rsync -av ${SRC}/cnfg${CFG}/ ${TRG}/cnfg${C}/
done
