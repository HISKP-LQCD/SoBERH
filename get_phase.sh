#get phases from eigensystems for every configuration into subfolder
#The eigensystems are only read in for fixation but remain untouched
#!/bin/bash
#copy correct binary to folder
cp /hiskp2/helmes/projects/lap_shell_imp_comm/save_phase/bins/save_phase_${1}_${2}_${3} .
#if nonexistent create folder phases
mkdir -p phases
#get a list of all available eigensystems of one ensemble in terms of configs
ls -lh *values* | awk '{if($5!=0) print $9}' | cut -c 13-16 | sort -u > conf_list.txt
#loop over this list
while read CONF
do
  #execute programm, this creates for every timeslice of each config a file
  #phases.$config.$ts holding the phase of the first entry of each eigenvector
  #naming scheme of programm is save_phase_LT_LS_NEV
  ./save_phase_${1}_${2}_${3} ${CONF};
  mv phases.${CONF}.* phases/
done < conf_list.txt
#modify so that phases can be read by everyone in the group
chmod -R g+rw phases/
rm save_phase*
rm conf_list.txt
