# Bash script concatenating all configurations of a single diagram
# Script first lists all abvailable configurations in a file then extracts every
# correlation function to a common file
#!/bin/bash

# Lattice input parameters, needed for header and extract_corrs
T=48
L=20

# number of correlators, needed for extract_corrs
ncorr=1
n_pt=$1


if [ $n_pt == '2' ]; then
  for pt in 'k'; do
    # Filenames  
    # Input prefix
    iprefix=C${n_pt}_${pt}_conf
    # Output filename
    oname=C${n_pt}_${pt}.dat

    # total number of configurations
    tot_conf=$(ls| grep $iprefix | wc -l)
    # get list of conf numbers in one file
    # cut 10-13 for 4pt, 13-16 for 2pt
    ls | grep $iprefix | cut -c10-13 > tmp_conf.dat 
    echo "$tot_conf $T 1 $L 1" > $oname
    for c in $(cat tmp_conf.dat) 
    do
      filename=$(echo "${iprefix}${c}.dat")
      echo -ne "extracting $filename\r"
      ./extract_corrs $filename $ncorr $T  | tail -n $T >> $oname 
    done
    rm tmp_conf.dat
  done
elif [ $n_pt == '4' ]; then
  for pt in 1 2 3 4; do
    # Filenames  
    # Input prefix
    iprefix=C${n_pt}_${pt}_conf
    # Output filename
    oname=C${n_pt}_${pt}.dat

    # total number of configurations
    tot_conf=$(ls| grep $iprefix | wc -l)
    # get list of conf numbers in one file
    # cut 10-13 for 4pt, 13-16 for 2pt
    ls | grep $iprefix | cut -c10-13 > tmp_conf.dat 
    echo "$tot_conf $T 1 $L 1" > $oname
    for c in $(cat tmp_conf.dat) 
    do
      filename=$(echo "${iprefix}${c}.dat")
      echo -ne "extracting $filename\r"
      ./extract_corrs $filename $ncorr $T  | tail -n $T >> $oname 
    done
    rm tmp_conf.dat
  done
else
  echo "No correlators summarized (need arg 2/4)"
fi

