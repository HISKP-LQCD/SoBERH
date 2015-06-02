#!/usr/bin/python
# Script to sum up all 4 diagrams of 4pt-correlation functions for same meson
# types

import numpy as np 

def _open_single(_name,first=False):
  """ Opens a correlation function file containing an informative header and
  correlation functions of the same diagram for different configurations.

  Args:
      _name: string representing the filename to be opened
      first: Boolean determining if it is the first file to be read in,
             if false the metadata as 3 tuple is returned as well
  Returns:
      A list of three tuples with each tuple consisting of time index, real
      and imaginary part of the correlation function (if first,the metadata as 3
      tuple is returned
  """
  _f = open(_name,'r')
  _dg = []
  _head = _f.readline()
  nbcfg = int(_head.split()[0])
  T=int(_head.split()[1])
  L=int(_head.split()[3])
  metadata=[nbcfg,T,L]
  for _cfg in range(0, nbcfg):
    for _t in range(0, T):   
      c_ent = _f.readline()
      arr = [float(x) for x in c_ent.split()]
      _dg.append(arr)
  _f.close()
  if not first:
    return _dg
  else:
    return _dg,metadata

#------------------------------------------------------------------------------

def corr_subtr(data1, data2):
  """ function to subtract two diagrams columnwise 
  
  Subtracts two correlation functions like data1 -data2

  Args:
      data1, data2: List of three tuples of one or more correlation functions

  Returns:
      A list of three tuples containing the difference C_1(t) - C_2(t)
  """
  _dif=[]

  for l1 in zip(data1, data2):
    t = int(l1[0][0])
    re = l1[0][1]-l1[1][1]
    im = l1[0][2]-l1[1][2]
    _dif.append([t, re, im])
  return _dif

#------------------------------------------------------------------------------

def corr_add(data1, data2):
  """ function to add two diagrams columnwise 
  
  Subtracts two correlation functions like data1 -data2

  Args:
      data1, data2: List of three tuples of one or more correlation functions

  Returns:
      A list of three tuples containing the difference C_1(t) + C_2(t)
  """
  _sum=[]
  for l1 in zip(data1, data2):
    t = int(l1[0][0])
    re = l1[0][1]+l1[1][1]
    im = l1[0][2]+l1[1][2]
    _sum.append([t, re, im])
  return _sum

#------------------------------------------------------------------------------

def corr_multi_scalar(data, scl=-1.):
  """ Multiplying Im(C(t)) with a scalar
  
  Args: 
      data1: List of three tuples of one or more correlation functions
      scl: the scalar to multiply with (defaults to -1)

  Returns: List of 3 tuples: t, Re(C(t)), scl*Im(C(t))
  """
  _prd=[] 
  for l1 in data:
    t = int(l1[0])
    re = l1[1]
    im = l1[2]*scl
    _prd.append([t, re, im])
  return _prd

###############################################################################
############################### Start Main ####################################
###############################################################################

def main():

  # define filenames
  save_name="kk_test"
  diag_list=['C4_1','C4_2','C4_3',]
  diag_sfx='.dat'
  diag_names=[]
  for dg in diag_list:
    diag_names.append(dg+diag_sfx)

  # open files and get metadata and correlation functions of diagrams
  diag1, meta = _open_single(diag_names[0],True) 
  diag2 = _open_single(diag_names[1])
  diag3 = _open_single(diag_names[2])
  # Add two diagrams for the direct propagating contribution
  direct = corr_add(diag1, diag2)

  # Obtain the last diagram by adjoining of the first cross diagram
  dg_4 = corr_multi_scalar(diag3)

  # Add these two up for the total cross propagating contribution
  crossed = corr_add(diag3, dg_4)

  # Finally subtract the crossed from the direct contribution to get the full
  # correlation function
  kk = corr_subtr(direct, crossed)
  # Save what was just calculated in save_name, conformant to liumings data
  # format
  with open(save_name, 'w') as fo:
    fo.write("%d %d 1 %d 1\n" %(meta[0], meta[1], meta[2]))
    for l in kk:
      out_str = "%d %.6e %.6e\n" %(l[0], l[1], l[2]) 
      fo.write(out_str)
  return

if __name__ == "__main__":
    main()
