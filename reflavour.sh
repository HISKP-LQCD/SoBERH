# Bash script for replacing the flavour Tag in the file name of a perambulator
# and its associated random vector
#!/bin/bash

# Old and new quark flavour name
flv_old="u"
flv_new="s"

# The script operates configuration-wise, need configs range
bgn=501
end=2004
dst=8

# Number of perambulators per config
per_cfg=5

# Flag for storage layout (rnd_vec subfolders yes or no?)
rnd_vec=true 
# loop over all configurations that need renaming
for (( cfg=$bgn; cfg<=$end; cfg+=$dst )); do
  cd cnfg${cfg}
  if [ "$rnd_vec" = true ]; then
    for (( r=0; r<$per_cfg; r+=1 )); do
      cd rnd_vec_$r/
      # Rename perambulator
      ls perambulator*
      # Rename randomvector
      ls randomvector*
      cd ../
    done
  else
    for (( r=0; r<$per_cfg; r+=1 )); do
      # Rename perambulator
      # Rename randomvector
    done
    fi
done
echo "Renamed $( ($end-$bgn)/$dst+1 ) configurations"
