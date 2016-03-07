# Small bash script to tar perambulators in packages of configurations
#!/usr/bin/python
##!/hadron/knippsch/Enthought/Canopy_64bit/User/bin/python

import sys, os, tarfile, re, subprocess, glob


# Function sorting by digits independent from length
def natural_sort(l): 
      convert = lambda text: int(text) if text.isdigit() else text.lower() 
      alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
      return sorted(l, key = alphanum_key)

# cut a list of configuration based on indices
def cut_range(lst, rnge):
  # the indices pointing to first and last index
  #TODO: think about list comprehension
  #e = [i for i,s in enumerate(lst) if]
  b, e = 0, 0
  for i, s in enumerate(lst):
  # s is padded with cnfg, exclude from comparison for identity checking
    if rnge[0] == s[4:]:
      b = i
    if rnge[1] == s[4:]:
      e = i
  res = lst[b:e+2]
  #return res[0::int(rnge[2])]
  return res[0::2]

# Set the parameters
# Lattice name
ens_src='A40.32/'
ens='A40.32/'
flv_src='light/'
flv='light/'
# is backup local?
local=True

# Setting target path for archive and tar locally 
# and then rsync to juelich archive rsync destination
SRC='/work/hbn28/hbn284/'+ens_src+flv_src
WRK='/work/hbn28/hbn284/peram_vault/'
HOST='juqueen'
SNC='/arch2/hbn28/hbn284/perambulators/'+ens+flv


# create a list of configs to tar and check existence
cfg_want = ['cnfg%d' % c for c in range(200,1201,4)]
# get names
cfg_have = os.listdir(SRC)
# test and sort list
# regular expression containing "cnfg" followed by 3 or 4 ints
reg = re.compile(r'cnfg[0-9]{1,}')
cfgs_reg = filter(reg.match, cfg_have)
cfgs_new = natural_sort(cfgs_reg)
# compare lists
cfgs_cut = set(cfg_want).intersection(cfg_have)
# sort intersection
cfgs_tar = natural_sort(cfgs_cut)
print cfgs_tar

size = 50
# chunks for taring
chunks = [cfgs_tar[i:i+size] for i  in range(0, len(cfgs_tar), size)]
for c in chunks:
    b=c[0]
    e=c[-1]
    # distance in filename from interval
    d='4'
    # First create a list with the according configurations
    
    os.chdir(SRC)
    # Now we want to tar everything in the range list into one specific tar archive
    arcname=WRK+'perams_' +b[4:] + '-' + d + '-' +e[4:]+ '.tar'
    #if os.path.isfile(arcname) is False:
    tar = tarfile.open(arcname,"w")
    for name in c:
        files=os.listdir(name)
        EXCLUDE_FILES=['main', 'slice1', 'slice2']
        EXCLUDE_FILES=[ name+'/'+f for f in EXCLUDE_FILES]
        print(EXCLUDE_FILES)
        tar.add(name, exclude=lambda x: True if x in EXCLUDE_FILES else False)
    tar.close()
    # Rsync perambulator archive to destination
    if local:
        rsync_args=['rsync', arcname, SNC]
    else:
        rsync_args=['rsync', arcname, 'hbn284@'+HOST+':'+SNC]
    subprocess.call(rsync_args)

