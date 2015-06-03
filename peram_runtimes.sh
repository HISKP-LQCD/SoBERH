#!/bin/bash
for i in $(cat peram_folders.txt); do
  if [[ ${i:0:1} != "#" ]]; then
    echo "runtimes for $i"
    python get_time.py ${i}/run.out | tail -n4
    echo " ";
  fi
done
