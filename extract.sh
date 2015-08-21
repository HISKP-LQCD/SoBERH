#!/bin/bash

T=48
L=24

for ((c=500; c<=2900; c+=8)); do
	cfg=`printf %04d $c`
	lime_extract_record C2_k_conf${cfg}.dat 2 3 tmp.dat
	echo "1 1 $T 0 $L 1" > pi_corr_pre
	od -vt fD tmp.dat >> pi_corr_pre
	cut -s -d" "  -f 2- pi_corr_pre > C2_k_c${cfg}.dat
	
	for p4 in 1 2 3 4; do
		lime_extract_record C4_${p4}_conf${cfg}.dat 2 3 tmp.dat
		echo "1 1 $T 0 $L 1" > pi_corr_pre
		od -vt fD tmp.dat >> pi_corr_pre
		cut -s -d" "  -f 2- pi_corr_pre > C4_${p4}_c${cfg}.dat
	done
done

