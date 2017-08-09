# 10.01.2017 Maximilian Oehm, Markus Werner
# This skript checks the existance and size of perambulators and random vectors
# generated with the sLapH method.
import argparse

import os, glob
import re

import numpy as np

################################################################################
# Argument parsing ############################################################# 

parser = argparse.ArgumentParser()

parser.add_argument("--first_config", type=int, 
                    help="Number of first gauge configuration", required=True)
parser.add_argument("--delta_config", type=int, 
                    help="Number of first gauge configuration", required=True)
parser.add_argument("--final_config", type=int, 
                    help="Number of first gauge configuration", required=True)

parser.add_argument("--nb_rnd_vec", type=int, 
                    help="Number of random vectors", required=True)

parser.add_argument("--T", type=int, 
                    help="Time extent of the lattice", required=True)
parser.add_argument("--dilution_scheme", 
                     help="Dilution scheme chosen for the lattice", 
                     required=True, choices=["20", "24", "32"])
parser.add_argument("--missing_config", type=int, nargs="*", default = [])

args = parser.parse_args()

srt_cnfg = args.first_config
del_cnfg = args.delta_config
end_cnfg = args.final_config

nb_rnd_vec = args.nb_rnd_vec

T = args.T
missing_cnfg = args.missing_config

nb_ev = {"20" : 66, "24" : 120, "32" :220}   # number of eigenvectors
nb_ev = nb_ev[args.dilution_scheme]
dil_T = {"20" : 24, "24" : 24, "32" : 32}    # number of diluted blocks in time
dil_T = dil_T[args.dilution_scheme]
dil_ev = {"20" : 6, "24" : 6, "32" : 4}       # number of diluted blocks in ev-space
dil_ev = dil_ev[args.dilution_scheme]

nb_I_T  = {"20" : 24, "24" : 24, "32" : 32}   # number of inversions in time
nb_I_T = nb_I_T[args.dilution_scheme]
nb_I_EV = {"20" : 6, "24" : 6, "32" : 4}      # number of inversions in eigenvector space
nb_I_EV = nb_I_EV[args.dilution_scheme]
nb_I_D  = 4                                   # number of inversions in Dirac space


################################################################################
peram_size = (T*nb_ev*4)*(dil_T*dil_ev*4)*(2*8) 
                                     # 4: Dirac, 2: complex, 8: double precision
rnd_vec_size = (T*nb_ev*4)*(2*8)     # 4: Dirac, 2: complex, 8: double precision
################################################################################

# function to print error message and simultaniously save it into a list.
def eprint(message, errors, cnfg, rnd):
  print message
  errors.append([cnfg, rnd, message])

# taken from http://stackoverflow.com/questions/8560440/
#                      removing-duplicate-columns-and-rows-from-a-numpy-2d-array
# function to remove duplicates in a 2d array. Will be used to recompute 
# missing configurations only once even if multiple error messages are thrown
def unique(a):
  a = np.array(a)
  order = np.lexsort(a.T)
  a = a[order]
  diff = np.diff(a, axis=0)
  ui = np.ones(len(a), 'bool')
  ui[1:] = (diff != 0).any(axis=1) 
  return a[ui]

################################################################################
errors = []
for i in range(srt_cnfg, end_cnfg+1, del_cnfg):
  if i in missing_cnfg:
    continue
  for j in range(nb_rnd_vec):
    path = './cnfg%04d' % i + '/rnd_vec_%02d' % j
    print 'check path: ' + path

    # checking the perambulator
    filename = path + '/perambulator.rndvecnb%02d.*' % j
    fi = glob.glob(filename)
    if(len(fi) == 0):
      eprint('\tNo perambulator file exists in ' + path, errors, i, j)
    for k in fi:
      size = os.path.getsize(k)
      if(peram_size != size):
        eprint('\tSize of perambulator in ' + path + ' is not correct', \
                                                                   errors, i, j)
        eprint('\tsize should be %d' % peram_size + ' but is %d' % size, 
                                                                   errors, i, j)

    # checking the random vector
    filename = path + '/randomvector.rndvecnb%02d.*' % j
    fi = glob.glob(filename)
    if(len(fi) == 0):
      eprint('\tNo randomvector file exists in ' + path, errors, i, j)
    for k in fi:
      size = os.path.getsize(k)
      if(rnd_vec_size != size):
        eprint('\tSize of randomvector in ' + path + ' is not correct', errors, i, j)
        eprint('\tsize should be %d' % rnd_vec_size + ' but is %d' % size, errors, i, j)

if len(errors) != 0:
  print ' ' 
  for e in errors:
    print e

  print ' ' 

  missing_cnfg = unique(zip([e[0] for e in errors], [e[1] for e in errors]))
  np.savetxt('missing_configs.txt', missing_cnfg, fmt='%d', header='cnfg\trnd_vec', delimiter=',')
else:
  print 'No errors'

