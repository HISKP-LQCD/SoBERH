#!/usr/bin/python

import glob, os, shutil

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
        new = i.replace('rndvecnb00', 'rndvecnb03')
        result.append(new)
      if 'rndvecnb01' in i:
        new = i.replace('rndvecnb01', 'rndvecnb04')
        result.append(new)
    if 'randomvector' in i: 
      if 'rndvecnb00' in i:
        new = i.replace('rndvecnb00', 'rndvecnb03')
        result.append(new)
      if 'rndvecnb01' in i:
        new = i.replace('rndvecnb01', 'rndvecnb04')
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
	  tmp = line.replace('id 0', 'id 3')
          seeds.append(tmp)
        if 'id 1' in line:
          tmp = line.replace('id 1', 'id 4')
          seeds.append(tmp)
  print seeds
  with open(in_1, 'r+') as f1:
    lines = f1.readlines()
    for i, line in enumerate(lines):
      if 'nb_rnd' in line:
         del lines[i]
         lines.insert(i, 'nb_rnd = 5\n') 
      if 'id 2' in line:
        lines.insert(i+1, seeds[0])  # inserts "somedata" above the current line
        lines.insert(i+2, seeds[1])  # inserts "somedata" above the current line
    f1.truncate()         # truncates the file
    f1.seek(0)             # moves the pointer to the start of the file
    f1.writelines(lines)   # write the new data to the file
  # change number of random vectors in in_1
  # copy to appropriate lines in in_1
  # close files
  # remove infile in_2

bgn, end, dis = 1331, 1339, 8 
subfold = ['slice1', 'slice2']
entry = os.getcwd()

for c in range(bgn, end, dis):
  cfg_fold = os.getcwd() + "/" + "cnfg" + str(c)
  print "Merging " + cfg_fold
  for s in subfold:
    os.chdir("cnfg"+str(c)+"/"+s)
    files = sorted(os.listdir(os.getcwd()), key=str.lower)
    if s == 'slice1':
      print "Moving slice1"
      # Purge main and get_time.py from list
      purge = [1,5]
      purge_list(files, purge)
      # Move everything up one folder
      for i in files:
	src = os.getcwd() + "/" + i
	dst = cfg_fold + "/" + i
        shutil.copy(src, dst)
      
     # for name in files:
    else:
      print "\nMoving slice2"
      purge = [1,3,4,5]
      purge_list( files, purge )
      dests = replace_names(files)
      per_rnd = files[2:6]
      if len(per_rnd) == len(dests):
        for i in 0,1,2,3:
          src = os.getcwd() + "/" + per_rnd[i]
          dst = cfg_fold + "/" + dests[i]
          shutil.copy(src, dst)
      else:
        print("lists have different length! ")
        print len(dests), len(per_rnd)
      del files[2:6]
      
      src = os.getcwd() + "/" + files[0]
      dst = cfg_fold + "/" + files[0].replace('.0.','.1.')
      shutil.copy(src, dst)
      src = os.getcwd() + "/" + files[1]
      dst = cfg_fold + "/" + files[1] + "2"
      shutil.copy(src, dst)
      # rename rndvec and peramb files, also rename infile.in and move things up
    os.chdir(entry)
  os.chdir(cfg_fold)
  merge_infiles("infile.in", "infile.in2")
  # Clean up
  slice1 = cfg_fold + "/" + "slice1/*"
  slice2 = cfg_fold + "/" + "slice2/*"
  for file in glob.glob(slice1):
    os.remove(file)
  for file in glob.glob(slice2):
    os.remove(file)
  os.removedirs('slice1/')
  os.removedirs('slice2/')
  os.remove('infile.in2')

    
