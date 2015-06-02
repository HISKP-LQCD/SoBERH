#!/bin/bash
# Setting target path
TGT=./
# Loop over all configurations to be packed
# for (( cfg=955; cfg<=1019; cfg+=8 ))
# Test for one config first
for cfg in 500
do
  NUM=`printf %04d ${cfg}`
  mkdir -p ${TGT}/cnfg${NUM}
  cd cnfg${cfg}
  for (( r=0; r <=4; r+=1 ))
  do
    mkdir -p ${TGT}/cnfg/rnd_vec_${r}
    cd rnd_vec_${r}
    old_peram = `ls peram*`  
    old_rando = `ls random*` 
    new_peram = echo ${old_peram}| sed 's/\.c\./\.s\./g'
    new_rando = echo ${old_rando}| sed 's/\.c\./\.s\./g' 
    mv $old_peram $new_peram
    mv $old_rando $new_rando
    #cp  perambulator.*.0${NUM} randomvector.*.${NUM} infile.in invert.input job.sh
    #${ARC}/light/cnfg${NUM}/rnd_vec${r}/
    cd ../
  done
  cd ../
# mv since only tar archive is used
#  mv eigensys_${NUM}.tar ${ARC}/
done

