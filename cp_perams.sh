#!/bin/bash
# Setting target path for archive
ARC=/hiskp2/perambulators/B85.24_L24_T48_beta195_mul0085_musig135_mudel170_kappa1612312
# Loop over all configurations to be packed
# for (( cfg=955; cfg<=1019; cfg+=8 ))
# Test for one config first
for cfg in 500
do
  NUM=`printf %04d ${cfg}`
  mkdir -p ${ARC}/light/cnfg${NUM}
  cd cnfg${cfg}
  for (( r=0; r <=4; r+=1 ))
  do
    mkdir -p ${ARC}/light/cnfg/rnd_vec_${r}
    cd rnd_vec_${r}
    cp  perambulator.*.0${NUM} randomvector.*.${NUM} infile.in invert.input job.sh
    ${ARC}/light/cnfg${NUM}/rnd_vec${r}/
    cd ../
  done
  cd ../
# mv since only tar archive is used
#  mv eigensys_${NUM}.tar ${ARC}/
done
