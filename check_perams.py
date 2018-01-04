#!/usr/bin/python

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
parser.add_argument("--nb_ev", type=int,
                     help="Number of LapH Eigenvectors", 
                     required=True)
parser.add_argument("--dil_T", type=int,
                    help="Extent of time dilution index",
                    required=True)
parser.add_argument("--dil_ev", type=int,
                    help="Extent of LapH EV dilution index",
                    required=True)

parser.add_argument("--missing_config", type=int, nargs="*", default = [])

args = parser.parse_args()

srt_cnfg = args.first_config
del_cnfg = args.delta_config
end_cnfg = args.final_config

nb_rnd_vec = args.nb_rnd_vec

T = args.T
missing_cnfg = args.missing_config

nb_ev = args.nb_ev
dil_T = args.dil_T
dil_ev = args.dil_ev
dil_D = 4

################################################################################
peram_size = (T*nb_ev*4)*(dil_T*dil_ev*dil_D)*(2*8) 
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
peram_errors = []
rndvec_errors = []
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
      eprint('\tNo perambulator file exists in ' + path, peram_errors, i, j)
    for k in fi:
      size = os.path.getsize(k)
      if(peram_size != size):
        eprint('\tSize of perambulator in ' + path + ' is not correct', \
                                                                   peram_errors, i, j)
        eprint('\tsize should be %d' % peram_size + ' but is %d' % size, 
                                                                   peram_errors, i, j)

    # checking the random vector
    filename = path + '/randomvector.rndvecnb%02d.*' % j
    fi = glob.glob(filename)
    if(len(fi) == 0):
      eprint('\tNo randomvector file exists in ' + path, rndvec_errors, i, j)
    for k in fi:
      size = os.path.getsize(k)
      if(rnd_vec_size != size):
        eprint('\tSize of randomvector in ' + path + ' is not correct', rndvec_errors, i, j)
        eprint('\tsize should be %d' % rnd_vec_size + ' but is %d' % size, rndvec_errors, i, j)

if len(peram_errors) != 0:
  print ' ' 
  for e in peram_errors:
    print e
  print ' '

if len(rndvec_errors) != 0:
  for e in rndvec_errors:
    print e
  print ' ' 

  missing_cnfg = unique(zip([e[0] for e in peram_errors], [e[1] for e in peram_errors]))
  np.savetxt('missing_configs.txt', missing_cnfg, fmt='%d', header='cnfg\trnd_vec', delimiter=',')
else:
  print 'No errors'

