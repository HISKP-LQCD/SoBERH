#!/bin/bash/
  
for i in $(seq 2 4 698); do
	echo $i
	printf -v line0 "%04d" "$i"
	#echo C4cC_cnfg$line0.h5
	if [ ! -f "C2c_cnfg$line0.h5" -a $(stat -c%s "C2c_cnfg$line0.h5") -ne "65024" ]; then
	    echo "C2c_cnfg$line0.h5 does not exist."
        fi
	if [ ! -f "C4cC_cnfg$line0.h5" -a $(stat -c%s "C4cC_cnfg$line0.h5") -ne "7661824" ]; then
            echo "C4cC_cnfg$line0.h5 does not exist."
	fi
	if [ ! -f "C4cD_cnfg$line0.h5" -a $(stat -c%s "C4cC_cnfg$line0.h5") -ne "7607736" ]; then
            echo "C4cD_cnfg$line0.h5 does not exist."
	fi
	if [ ! -f "C6cC_cnfg$line0.h5" -a $(stat -c%s "C6cC_cnfg$line0.h5") -ne "139084720" ]; then
	    echo "C6cC_cnfg$line0.h5 does not exist."
	fi
	if [ ! -f "C6cD_cnfg$line0.h5" -a $(stat -c%s "C6cD_cnfg$line0.h5") -ne "69653152" ]; then
	    echo "C6cD_cnfg$line0.h5 does not exist."
	fi
	if [ ! -f "C6cCD_cnfg$line0.h5" -a $(stat -c%s "C6cCD_cnfg$line0.h5") -ne "200961968" ]; then
	    echo "C6cCD_cnfg$line0.h5 does not exist."
	fi
				    
done
