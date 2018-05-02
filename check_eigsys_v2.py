#!/usr/bin/python
#Python script checking size and numbers of eigensystems listing missing ones
import subprocess
import os
#PATH='/hiskp4/eigensystems/nf211/B55.32-3/hyp_062_058_3/nev_220'
PATH='/hiskp4/eigensystems/nf211/D45.32_L32_T64_beta210_mul0045_musig0937_mudel1077_kappa1563150/hyp_062_058_3/nev_220'
START, END, DST = 2, 1198, 4
TS=64
L=32
NEV=220
fsize=2*8*NEV*3*(L**3)
# loop over configurations
for cfg in range(START, END+DST, DST):
    # empty list for missing timeslices
    miss = list()
    for t in range(0,TS):
        file = "%s/eigenvectors.%04d"%(PATH,cfg)+".%03d"%t
        if os.path.exists(file):
            if os.path.getsize(file) == fsize:
              pass
            else:
              #print(os.path.getsize(file))
              miss.append(t)
        else:
            miss.append(t)
    if len(miss) > 0:
        if len(miss) > TS/2:
            print("More than half of the timeslices missing on cfg %d"%cfg)
        else:
            print("Timeslices "+",".join(map(str, miss))+" missing on cfg %d"%cfg)
    else:
        print "Config %d"%cfg+" complete"
