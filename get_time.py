import sys, os, math, random
import numpy as np
import re

arg = sys.argv[1]
# running over all subdirectories and searching for files starting with "Magne"
fi = open(arg, 'r')
time = []
check_string = '# Inversion done in [+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)? sec.'
i=0
for line in fi:
#  if check_string in line:
  if re.match(check_string, line):
    segments = line.split()
    time.append(float(segments[4]))
    print i, time[-1]
    i += 1
fi.close()
total_time = sum(time)/3600
nb_cnfg = 39
print '# total time %lf' % total_time + " h"
print '# time to build deflation space %lf' % sum(time[0:nb_cnfg])
print '# average time to build deflation space %lf' % (sum(time[0:nb_cnfg])/len(time[0:nb_cnfg]))
print '# average time inversion %lf' % (sum(time[nb_cnfg:-1])/len(time[nb_cnfg:-1]))


