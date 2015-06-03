#Python script checking size and numbers of eigensystems listing missing ones
#!/usr/bin/python
import subprocess
import os.path
START, END, DST = 787, 979 , 8
TS=96
fsize=3.3*1024*1024*1024
for cfg in range(START, END+DST, DST):
    miss = list()
    for t in range(0,TS):
        file = "eigenvectors.%04d"%cfg+".%03d"%t
        if os.path.exists(file):
            size = os.path.getsize(file)
            if os.path.getsize(file) == fsize:
              pass
        else:
            miss.append(t)
    if len(miss) > 0:
            print "Timeslices "+",".join(map(str, miss))+" missing on cfg %d"%cfg
    else:
        print "Config %d"%cfg+" complete"
