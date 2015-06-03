#!/bin/bash
# Setting target path for archive
ARC=/arch2/hbn28/hbn284/perambulators/B35.48
# Loop over all configurations to be packed
 for (( cfg=1059; cfg<=1219; cfg+=8 ))
# Test for one config first
#for cfg in 1000
do
  NUM=`printf %04d ${cfg}`
  cd cnfg${cfg}
  tar cvf ${ARC}/perams_${NUM}.tar perambulator.*.0${NUM} randomvector.*.${NUM} infile.in invert.input *.out job.sh
  cd ../
# mv since only tar archive is used
#  mv eigensys_${NUM}.tar ${ARC}/
done
