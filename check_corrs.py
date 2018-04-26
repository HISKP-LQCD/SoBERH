# 10.01.2017 Maximilian Oehm, Markus Werner
# This skript checks the existance of correlation functions calculated with the
# cntr.v0.1 contraction code

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
parser.add_argument("--missing_config", type=int, nargs="*", default = [])

parser.add_argument("--path", default="./", 
                   help="Path to diagrams. Default: (default)s")

parser.add_argument("--diagrams", nargs="+", 
                    help="Name of the diagrams which where calculated", 
                    required=True)

################################################################################

args = parser.parse_args()

srt_cnfg = args.first_config
del_cnfg = args.delta_config
end_cnfg = args.final_config

missing_cnfg = args.missing_config

path = args.path

diagrams = args.diagrams

## necessary diagrams for rho calculation
#diagrams = ["C20", "C2+", "C3+", "C4+B", "C4+D"]

################################################################################

# function to print error message and simultaniously save it into a list.
def eprint(message, errors, cnfg, diagram):
  print(message)
  errors.append([cnfg, diagram, message])

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
  for j in diagrams:

    filename = '/%s' % j + '_cnfg%04d' % i + '.h5'

    print('checking {}'.format(filename))

    # checking for existence
    fi = glob.glob(path + filename)
    if(len(fi) == 0):
      eprint('\tNo correlator file exists for ' + j, errors, i, j)

# TODO: check for correct size as well
#    size = os.path.getsize(k)
#    if(peram_size != size):
#      eprint('\tSize of perambulator in ' + path + ' is not correct', \
#                                                                 errors, i, j)
#      eprint('\tsize should be %d' % peram_size + ' but is %d' % size, 
#                                                                 errors, i, j)

if len(errors) != 0:
  print(' ')
  for e in errors:
    print(e)

  print(' ')

  # TODO: repair unique function for strings in diagrams
# missing_cnfg = unique(zip([e[0] for e in errors], [e[1] for e in errors]))
#  missing_cnfg = np.asarray(zip([e[0] for e in errors], [e[1] for e in errors]), dtype=object)
  # dtype = object necessary, because implicitely cnfg is casted to string otherwise
  missing_cnfg = np.array(errors, dtype=object)[:,:2]
  np.savetxt(path + '/missing_configs.txt', missing_cnfg, fmt='%d\t%s', header='cnfg\tdiagram')
