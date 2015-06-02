#!/bin/bash
# Script that deletes all eigensystems in the execution folder specified by arguments BGN, END, DST
BGN=327
END=799
DST=8
PRD=$(( ($END - $BGN) / DST + 1))
echo "About to delete $PRD eigensystems rangeing from $BGN to $END"
read -p "Are you sure? (y|n): " dec
if [[ $dec = "y" ]]; then
	for (( cnfg=${BGN}; cnfg<=${END}; cnfg+=${DST} )); do
		c=`printf %04d ${cnfg}`
		rm eigenv*.$c.* 
		rm phases.$c.*
		echo "deleted eigensystem $c"
	done
	echo "$PRD eigensystems deleted"
elif [[ $dec = "n" ]]; then 
	echo "No harm done"
else
	echo "invalid choice"
fi
