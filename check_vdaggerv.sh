## NOTE that this script is lacking some funtionality as it's not quite
## clear which momenta will be generated during a run of sLapH-contractions
## as P = -P^\dagger is used in the code
## ideally this script would read the input file and then build a list
## of files that should be present (and their sizes, based on the dilution
## subspace dimensions)

checkdir=/p/scratch/chbn28/project/vdaggerv/nf2/cA2b.30.48

conf_start=1
conf_step=2
conf_end=701

size_expected=6969600
nfiles_expected=1536

echo > incomplete_files.txt
echo > incomplete_confs.txt

for cid in $(seq $conf_start $conf_step $conf_end); do
  cid4=$(printf %04d $cid)
  
  echo checking $cid4 / $(printf %04d $conf_end)

  error=0
  nfiles=0
  for f in $(ls ${checkdir}/cnfg${cid4}/operators.${cid4}.*); do
    size=$(stat --printf="%s" ${f})
    if [ $size -ne $size_expected ]; then
      echo ${f} >> incomplete_files.txt
      error=1
    fi
    nfiles=$(( $nfiles + 1 ))
  done
  if [ $nfiles -ne $nfiles_expected ]; then
    echo $cid4 >> incomplete_confs.txt
    error=1
  fi
  if [ $error -ne 0 ]; then
    echo Problem with $cid4
  else
    echo $nfiles files of size $size
  fi
done

