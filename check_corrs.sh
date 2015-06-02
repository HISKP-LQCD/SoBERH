#Script for checking filesize and completness of perambulator generation
#!/bin/bash
for cnfg in {2608..2696..8}
#for cnfg in 1000
 do
# #Skip broken configurations
#   if [[ ${cnfg} == 1184 || ${cnfg} == 1200 || ${cnfg} == 1336 || ${cnfg} == 1440 || ${cnfg} == 1488 || ${cnfg} == 1720 || ${cnfg} == 1960 || ${cnfg} == 2032 || ${cnfg} == 2104 || ${cnfg} == 2152 || ${cnfg} == 2544 ]];then
#     continue
#   fi
 PER_FIN=0
 RND_FIN=0
   #for i in 0 1 2 3 4; do
     PER=$(ls cnfg${cnfg}/C2* | wc -l)
     PER_FIN=$(( $PER_FIN + $PER ))
     RND=$(ls cnfg${cnfg}/C4* | wc -l)
     RND_FIN=$(( $RND_FIN + $RND ))
  #done
  echo "config ${cnfg} has ${PER_FIN} 2pt- and ${RND_FIN} 4pt-functions"
 done

