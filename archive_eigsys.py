#!/hadron/knippsch/Enthought/Canopy_64bit/User/bin/python

# Small bash script to tar eigensystems
import argparse
import sys, os, tarfile, re, subprocess

def calc_arcsize(t, l, nev):
    evecs_ts = nev*l**3*3*2*8
    # phases have same size as evals
    evals_ts = nev*8
    return t*(2*evals_ts+evecs_ts)

def cmp_sizes(arcpath,size,push,pop):
    sync = None
    if os.path.getsize(arcpath) >= size:
        print("\nSuccessfully packed %d" %c)
        # make shure to only append filename
        push.append(arcpath.split('/')[-1])
    else:
        print("\nEigensystem %d has wrong size:"%c)
        print("Should be %d bytes" %arcsize)
        print("Instead is: %d bytes" %os.path.getsize(arcname))
        # make shure to only append filename
        pop.append(arcpath.split('/')[-1])

# Input parameters, can be changed later
# ensemblename
ens='B55.32'
# paths
src='/hiskp4/eigensystems/nf211/B55.32_L32_T64_beta195_mul0055_musig135_mudel170_kappa1612360/hyp_062_058_3/nev_220/'
vault='/hiskp4/helmes/eigsys_vault'
dest='/arch/hch02/hch026/helmes/eigensystems/'+ens+'/'
host='judac'
user='hch026'
# configuration numbers
bgn=504
end=1288
dst=16
# Lattice parameters
time=64
length=32
nev=220

sync=True

# calculate size of archive of one configuration
arcsize=calc_arcsize(time,length,nev)
# Change to sourcefolder
os.chdir(src)
print(os.getcwd())
# First look at available eigensystems with check_eigsys
# WORKAROUND: specify configurations directly
configs=range(bgn,end+1,dst)
    
# tar configurations to eigsys_vault
# per configuration open one tar archive
include=[]
exclude=[]
for c in configs:
    arcname=vault+'/eigsys_%04d'%c+'.tar'
# create filenames for that configuration
    filenames=[]
    if os.path.lexists('eigenvectors.%04d.%03d' %(c,time-1)):
        for t in range(time):
        # TODO: there has to be something more elegant
            filenames.append('eigenvectors.%04d.%03d' %(c,t))
            filenames.append('eigenvalues.%04d.%03d' %(c,t))
            filenames.append('phases.%04d.%03d' %(c,t))
        with tarfile.open(arcname,"w",dereference=True) as tar:
            for name in filenames:
                tar.add(name)
    else:
        print('Configuration %d not existing.' %c)
# check expected filesize vs actual one and decide whether to sync or not
# TODO: refine that
    #sync=cmp_sizes(arcname,arcsize)
    cmp_sizes(arcname,arcsize,include,exclude)

# generate a list of eigensystems in vault
os.chdir(vault)
transfer=os.listdir(os.getcwd())
# save transfer file for rsync
with open('include.txt',"a") as inc:
    inc.write("\n".join(map(lambda x: str(x),include)))
with open('exclude.txt',"a") as exc:
    exc.write("\n".join(map(lambda x: str(x),exclude)))
#TODO:adapt tar command    
# rsync configurations to archive destination with --from-file
#rsync_args=['rsync','--files-from=include.txt' ,'./', user+'@'+host+':'+dest]
print("Archiving complete. To transfer archive files change to eigsys_vault and run:")
print("ls | grep tar > transfer.txt")
print("and afterwards:")
print("rsync -v --files-from=include.txt ./ %s@%s:%s > transfer.log " %(user,host,dest))
#subprocess.call(rsync_args)
# delete transfer file
