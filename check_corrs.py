#!/usr/bin/python

# 10.01.2017 Maximilian Oehm, Markus Werner
# This skript checks the existance of correlation functions calculated with the
# cntr.v0.1 contraction code

import argparse

import h5py

import numpy as np

################################################################################
# Argument parsing ############################################################# 

parser = argparse.ArgumentParser()

parser.add_argument("first_config", type=int, 
                    help="Number of first gauge configuration")
parser.add_argument("final_config", type=int, 
                    help="Number of first gauge configuration")
parser.add_argument("delta_config", type=int, 
                    help="Number of first gauge configuration")

parser.add_argument("--missing_config", type=int, nargs="*", default = [])

parser.add_argument("--path", default="./", 
                   help="Path to diagrams. Default: (default)s")

parser.add_argument("--diagrams", nargs="+", 
                    default = ["C20", "C2c", "C3c", "C4cB", "C4cD"],
                    help="Name of the diagrams which where calculated")
parser.add_argument("--datasets_per_diagram", type=int, nargs="+", 
                    default = [1188, 132, 11640, 123120 ,123120],
                    help="Number of datasets which where calculated for each diagram")

################################################################################

args = parser.parse_args()

srt_cnfg = args.first_config
del_cnfg = args.delta_config
end_cnfg = args.final_config

missing_cnfg = args.missing_config

path = args.path

diagrams = args.diagrams
datasets_per_diagram = args.datasets_per_diagram

################################################################################

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

##########################################################################################
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class WrongSizeError(Error):
    """Exception raised if a h5file contains the wrong number of datasets.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

##########################################################################################
errors = np.empty([0,3], dtype=object)
for c in range(srt_cnfg, end_cnfg+1, del_cnfg):
  if c in missing_cnfg:
    continue
  for d,expected_size in zip(diagrams, datasets_per_diagram):

    filename = '/%s' % d + '_cnfg%04d' % c + '.h5'

    print('checking {}'.format(filename))

    # if error occurs, go to exception handling
    try:
      with h5py.File(path+filename, 'r') as file:
        size = len(file.keys())
        if(size != expected_size):
          raise WrongSizeError('\tNumber of correlators in ' + path + filename + ' is ' + str(size) + ' but expected ' + str(expected_size))
    except IOError:                                                                                                                                                                                            
      errors = np.append(errors, np.array([[c, d, '\tNo correlator file exists for ' + d]], dtype=object), axis=0)
      print(errors[-1,-1])
      continue
    except WrongSizeError as e:
      errors = np.append(errors, np.array([[c, d, e.message]], dtype=object), axis=0)
      print(errors[-1,-1])
      continue
    except:
      errors = np.append(errors, np.array([[c, d, '']], dtype=object), axis=0)
      print('Unexpected error in cnfg {}'.format(c))
      continue

if len(errors) != 0:
  print(' ')
  for e in errors:
    print(e)

  print(' ')

  # dtype = object necessary, because implicitely cnfg is casted to string otherwise
  missing_cnfg = np.unique(errors[:,:1])
  np.savetxt(path + '/missing_configs.txt', missing_cnfg, fmt='%d')
else:
  print('No errors')
