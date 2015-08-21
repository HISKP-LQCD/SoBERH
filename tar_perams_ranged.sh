# Small bash script to tar perambulators in packages of configurations
#!/bin/bash

# Set the parameters
# Lattice name
ens=A40.24
flv_src=A40_charm_225
flv=charm_225
add=

# Config range
BGN=1914
END=2110
DST=4


# Setting target path for archive and rsync destination
WRK=/hiskp2/helmes/peram_vault # tar locally and then rsync to juelich archive
HOST=judac.fz-juelich.de
SNC=/arch/hch02/hch026/helmes/perambulators/A40.24/${flv}

# First create a list with the according configurations
PERM=/hiskp2/perambulators/${ens}/${flv_src}
cd $WRK
echo "-C$PERM" > perams_tared.txt
for (( cfg = $BGN; cfg <= $END; cfg += $DST )); do
  j=`printf %04d $cfg`
	echo "cnfg$j" >> perams_tared.txt
done
#cd /hiskp2/perambulators/${ens}/${flv}
# Now we want to tar everything in the range list into one specific tar archive
SRC=perams_${BGN}-${DST}-${END}.tar
tar cvf ${SRC} --files-from perams_tared.txt --exclude main 
# Rsync perambulator archive to destination
rsync  ${SRC} hch026@${HOST}:${SNC}
# After that we should delete peram_list to generate it anew each time
rm perams_tared.txt
