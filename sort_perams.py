#!/usr/bin/python
# Used to sort perambulators into a cnfg*/rnd_vec*/ folder structure
import os
import glob
import fnmatch

def create_struct(prefix,confs):
  """ create a bunch of folders

  Parameters
  ----------
  confs : 
  prefix : 
  """
  confs[1] += 1
  print confs
  for i in range(confs[0],confs[1],confs[2]):
    print("creating path %d" %i)
    os.mkdir(prefix+str(i))

def sort_data_to_struct(prefix, confs, randoms=None):
  """Sort data classified by prefix, configuration number and random vector
  number into created struct

  Parameters
  ----------
  """
  #onlyfiles = [f for f in os.path.listdir('./') if os.path.isfile(join('./', f))]
  sort=glob.glob(prefix+'*')
  for c in range(confs[0],confs[1]+1,confs[2]):
    per_rand = fnmatch.filter(sort,'*'+str(c))
    print("moving "+prefix+"s to cnfg %d" %c )
    fld_name ='cnfg'+str(c)+'/' 
    for p in per_rand:
      print("moving "+p+" to "+fld_name+p)
      os.rename(p,fld_name+p)

def replace_name_part(name, prepend, confs, randoms=None):
  """Sort data classified by prefix, configuration number and random vector
  number into created struct

  Parameters
  ----------
  """
  #onlyfiles = [f for f in os.path.listdir('./') if os.path.isfile(join('./', f))]
  sort=glob.glob(name+'*')
  for c in range(confs[0],confs[1]+1,confs[2]):
    os.chdir('cnfg'+str(c))
    filenames = glob.glob(name+'*')
    newnames = []
    for i,v in enumerate(filenames):
      newname = prepend+v
      print("replacing "+v+" by "+newname)
      os.rename(v,newname)
    os.chdir('../')    

def main():
  configs=[2128,2992,8]
  r=range(5)
  #create_struct("./cnfg",configs
  #replace_name_part('ator','perambul',configs)
  #sort_data_to_struct("perambulator",configs)
  sort_data_to_struct("randomvector",configs)

if __name__ == '__main__':
  try:
    print("starting")
    main()
  except KeyboardInterrupt:
    pass
                                    
