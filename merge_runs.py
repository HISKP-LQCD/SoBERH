#!/usr/bin/python

###############################################################################
# 
# Merge subsequent calculations of perambulators
#
# Python script to merge different runs on the same quark mass, e.g. when the
# number of random vectors is increased. This program takes care of the renaming
# of the perambulator and randomvector files. It also adds the new seeds to the
# old input file. For the script to work the configurations to merge with have
# to be unpacked. 
#
# Copyright: Christopher Helmes,  March 2016
#
################################################################################

import glob, os, shutil, re

# Purge unwanted elements el_del from a list origin
def purge_list( origin, el_del ):
  origin[:] = [item for i, item in enumerate(origin) if i not in el_del]
  return

# Replace names in a list 
def replace_names( origin ):
  result = []
  for i in origin:
    # find index with peram
    if 'perambulator' in i:
      if 'rndvecnb00' in i:
        new = i.replace('rndvecnb00', 'rndvecnb05')
        result.append(new)
      if 'rndvecnb01' in i:
        new = i.replace('rndvecnb01', 'rndvecnb06')
        result.append(new)
    if 'randomvector' in i: 
      if 'rndvecnb00' in i:
        new = i.replace('rndvecnb00', 'rndvecnb05')
        result.append(new)
      if 'rndvecnb01' in i:
        new = i.replace('rndvecnb01', 'rndvecnb06')
        result.append(new)
  return result

# Merge the two infiles into one infile appending the random seeds and change
# number of random vectors
def merge_infiles(in_1, in_2):
  # seed strings
  seeds = []
  # open in_1 and in_2 (in_2 is supposed to contain 2 rnd seeds)
  with open(in_2, 'r') as f2:
  # get lines containing rnd seeds in in_2
    for line in f2:
      if 'seed' in line:
        if 'id 0' in line:
	  tmp = line.replace('id 0', 'id 5')
          seeds.append(tmp)
        if 'id 1' in line:
          tmp = line.replace('id 1', 'id 6')
          seeds.append(tmp)
  print seeds
  with open(in_1, 'r+') as f1:
    lines = f1.readlines()
    for i, line in enumerate(lines):
      if 'nb_rnd' in line:
         del lines[i]
         lines.insert(i, 'nb_rnd = 7\n') 
      if 'id 4' in line:
        lines.insert(i+1, seeds[0])  # inserts "somedata" above the current line
        lines.insert(i+2, seeds[1])  # inserts "somedata" above the current line
    f1.truncate()         # truncates the file
    f1.seek(0)             # moves the pointer to the start of the file
    f1.writelines(lines)   # write the new data to the file
  # change number of random vectors in in_1
  # copy to appropriate lines in in_1
  # close files
  # remove infile in_2


bgn, end, dst = 200, 200, 4
fold = ['/work/hbn28/hbn284/A40.32/merge_test/up',
'/work/hbn28/hbn284/A40.32/merge_test/light']
entry = os.getcwd()
unwanted = ['main','get_time.py','invert.input','job.sh','job.sh2',
            'tmLQCD_parameters.out']
checkre = re.compile("^random|peram*")

for c in range(bgn, end+1, dst):
  cnfg = "cnfg" + str(c)
  outfiles=0
  # get a list of the files in the two folders
  files_orig = sorted(os.listdir(fold[0]+"/"+cnfg),key=str.lower)
  files_dest = sorted(os.listdir(fold[1]+"/"+cnfg),key= str.lower)
  # remove unwanted files from list
  purge = [i for i, item in enumerate(files_orig) if item in unwanted]
  purge_list(files_orig, purge)

  print(files_orig)

  # rename perambulators and randomvectors and move them
  dests = replace_names(files_orig)
  per_rnd = [item for item in files_orig if checkre.match(item)]
  if len(per_rnd) == len(dests):
    for i in range(0, len(per_rnd)):
      src = fold[0] + "/" +cnfg + "/" + per_rnd[i]
      dst = fold[1] + "/" +cnfg + "/" + dests[i]
      shutil.copy(src, dst)
  else:
    print("lists have different length! ")
    print len(dests), len(per_rnd)
    print dests
    print per_rnd
  files=[item for item in files_orig if not checkre.match(item)]
  # rename log files and input files
  for i in files:
    if '.0.out' in i:
      src = fold[0] + "/" + cnfg + "/" + i
      dst = fold[1] + "/" + cnfg + "/" + i.replace('.0.', '.'+str(outfiles)+'.')
      shutil.copy(src, dst)
      outfiles += 1
    elif 'infile.in' in i:
      src = fold[0] + "/" + cnfg +  "/" + i
      dst = fold[1] + "/" + cnfg +  "/" + i + "2"
      shutil.copy(src, dst)
   
  merge_infiles(fold[1]+"/"+cnfg+"/infile.in",fold[1]+"/"+cnfg+"/infile.in2")
  os.remove(fold[1]+"/"+cnfg+"/infile.in2")
