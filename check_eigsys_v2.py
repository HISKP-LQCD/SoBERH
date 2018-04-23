#Python script checking size and numbers of eigensystems listing missing ones
#!/usr/bin/python
import subprocess
import os
PATH='/qbig2work/helmes/laph_eigsys/cA211a.30.32/data/'
START, END, DST = 0, 648, 4
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
            print "Timeslices "+",".join(map(str, miss))+" missing on cfg %d"%cfg
    else:
        print "Config %d"%cfg+" complete"
