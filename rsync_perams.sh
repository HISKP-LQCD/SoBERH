#!/bin/bash
# Script to rsync perambulators from SRC to a specific folder TRG config-wise

# Paths
SRC=/hiskp2/helmes/B85.24/up
TRG=/hiskp2/perambulators/B85.24_L24_T48_beta195_mul0085_musig135_mudel170_kappa1612312/light

# Range of configurations
BGN=500
END=3004i
DST=8
for (( CFG=${BGN}; CFG<=${END}; CFG+=${DST} )); do 
  C=${CFG}
  rsync -av ${SRC}/cnfg${CFG}/ ${TRG}/cnfg${C}/
done
