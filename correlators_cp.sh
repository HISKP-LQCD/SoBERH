#!/bin/bash
# Simple script to copy and rename correlators
# Config range
BGN=600
END=3104
DST=8

# define name prefixes
twopt_old="C2_pi+-_conf"
twopt_new="C2_k_conf"
twopt_xtrct="C2_k_c"

# Lattice stuff
T=48
L=24
# Copy everything over to the respective name
for (( c=$BGN; c<=$END; c+=$DST ));do 
  j=`printf %04d $c`
  cp ../cnfg$c/${twopt_old}${j}.dat ${twopt_new}${j}.dat
  cp ../cnfg$c/C4_*_conf$j.dat .
done
# Extract the correlation functions from binary format (needs lime tools
# installed), only one Correlation function per file regarded
for ((c=$BGN; c<=$END; c+=$DST)); do
	cfg=`printf %04d $c`
	lime_extract_record ${twopt_new}${cfg}.dat 2 3 tmp.dat
	echo "1 1 $T 0 $L 1" > pi_corr_pre
	od -vt fD tmp.dat >> pi_corr_pre
	cut -s -d" "  -f 2- pi_corr_pre > ${twopt_xtrct}${cfg}.dat
	
	for p4 in 1 2 3 4; do
		lime_extract_record C4_${p4}_conf${cfg}.dat 2 3 tmp.dat
		echo "1 1 $T 0 $L 1" > pi_corr_pre
		od -vt fD tmp.dat >> pi_corr_pre
		cut -s -d" "  -f 2- pi_corr_pre > C4_${p4}_c${cfg}.dat
	done
done
