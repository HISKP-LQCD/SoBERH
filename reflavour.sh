# Bash script for replacing the flavour Tag in the file name of a perambulator
# and its associated random vector
#!/bin/bash

# Perambulator Path
loc_peram=/hiskp2/perambulators/A100/nev_120/strange_185

# Replace flv_old in file name by flv_new in file name
flv_old="u"
flv_new="s"

# The script operates configuration-wise, need configs range
bgn=501
end=509
dst=8

# Number of perambulators per config
per_cfg=5

# Flag for storage layout (rnd_vec subfolders yes or no?)
rnd_vec=true
# go to perambulator location
cd $loc_peram
# loop over all configurations that need renaming
for (( cfg=$bgn; cfg<=$end; cfg+=$dst )); do
  cd cnfg${cfg}

  # Substructure present?
  if [ "$rnd_vec" = true ]; then
  # Yes
    for (( r=0; r<$per_cfg; r+=1 )); do
      cd rnd_vec_$r/
      # Rename perambulator
      per_old=$(ls perambulator*)
      per_new=${per_old//.${flv_old}./.${flv_new}.}
      cp $per_old $per_new

      # Rename randomvector
      rnd_old=$(ls perambulator*)
      rnd_new=${rnd_old//.${flv_old}./.${flv_new}.}
      cp $rnd_old $rnd_new
      cd ../
    done
  else
  # No
    for (( r=0; r<$per_cfg; r+=1 )); do
      # Rename perambulator
      per_old=$(ls perambulator.rndvecnb0${r}*)
      per_new=${per_old//.${flv_old}./.${flv_new}.}
      cp $per_old $per_new

      # Rename randomvector
      rnd_old=$(ls perambulator.rndvecnb0${r}*)
      rnd_new=${rnd_old//.${flv_old}./.${flv_new}.}
      cp $rnd_old $rnd_new
    done
  fi
done
nb_cfg=$(( ($end-$bgn)/$dst + 1 ))
echo "Renamed $nb_cfg configurations"
