#!/usr/bin/python3

# Small bash script to tar eigensystems
import argument_parsing as ap
import conf_utils
import sys, os, tarfile, re, subprocess

def calc_arcsize(t, l, nev, nconf=None):
    evecs_ts = nev*l**3*3*2*8
    # phases have same size as evals
    evals_ts = nev*8
    size = t*(2*evals_ts+evecs_ts)
    if nconf is not None:
        size *= nconf
    return size

def cmp_sizes(arcpath,size,push,pop):
    sync = None
    if os.path.getsize(arcpath) >= size:
        print("\nSuccessfully packed %s" %arcpath)
        # make shure to only append filename
        push.append(arcpath.split('/')[-1])
    else:
        print("\nEigensystem archive %s has wrong size:" %arcpath)
        print("Should be %d bytes" %size)
        print("Instead is: %d bytes" %os.path.getsize(arcpath))
        # make shure to only append filename
        pop.append(arcpath.split('/')[-1])

def main():
    parser = ap.arg_parser()
    args = parser.parse_args()
    ens = args.ens

    chunksize = args.chunksize

    remote_user = args.remote_user
    remote_host = args.remote_host

    source_path = args.source_path
    work_path = args.work_path
    remote_path = args.remote_path

    # user may provide list of configs to be skipped which we parse here
    skip_configs = []
    if args.skip_configs:
      skip_configs = [int(e) for e in ((args.skip_configs).split(","))]

    # set the work and remote path, adding the ensemble name
    work_path=work_path + '/' + ens + '/'
    try:
       if not os.path.exists(os.path.dirname(work_path)):
           os.makedirs(os.path.dirname(work_path))
    except OSError as err:
       print(err)
    
    remote_path=remote_path+'/'+ens+'/'
    
    # configuration numbers
    bgn=args.first_config
    end=args.final_config
    dst=args.delta_config
    
    # Lattice parameters
    time=args.Lt
    length=args.Ls
    nev=args.Nev

    sync=True

    # Change to sourcefolder
    os.chdir(source_path)
    print(os.getcwd())
    # First look at available eigensystems with check_eigsys
    # WORKAROUND: specify configurations directly
    configs=range(bgn,end+1,dst)
    
    # remove any of the skipped configs 
    configs = sorted(set(configs).difference(skip_configs))
    
    for conf_idx in configs:
        if not os.path.lexists('eigenvectors.%04d.%03d' %(conf_idx,time-1)):
            if args.error_on_missing:
                sys.exit("Files for configuration %d could not be found! Aborting!" %conf_idx)
            else:
                print('Files for configuration %d do not seem to exist!' %conf_idx)
                print('Removing from set of configs to be archived!')
                configs = sorted(set(configs).difference(conf_idx))

    if len(configs) == 0:
        sys.exit("No configurations left in target set! Aborting!")

    # we are going to build a list of archives that are ready to be synched (include)
    # and a list of archives where some kind of error occured (exclude), at least
    # judging from the file size 
    include=[]
    exclude=[]

    chunks = [configs[i:(i+chunksize)] for i in range(0, len(configs), chunksize)]
    for chunk in chunks:
        print('Packing chunk %s' %chunk)
        chunk_start = chunk[0]
        chunk_end = chunk[-1]
    
        arcsize=calc_arcsize(time,length,nev, len(range(chunk_start,chunk_end+1,dst)) )

        arcname=work_path+'/eigsys_%04d-%d-%04d'%(chunk_start,dst,chunk_end)+'.tar'
        if chunksize == 1:
            arcname=work_path+'/eigsys_%04d'%(chunk_start)+'.tar'

        filenames=[]
        for conf_idx in range(chunk_start,chunk_end+1,dst):
            for ts in range(time):
                filenames.append('eigenvectors.%04d.%03d' %(conf_idx,ts))
                filenames.append('eigenvalues.%04d.%03d' %(conf_idx,ts))
                filenames.append('phases.%04d.%03d' %(conf_idx,ts))

        with tarfile.open(arcname, "w", dereference=True) as tar:
            for name in filenames:
                tar.add(name)

        cmp_sizes(arcname, arcsize, include, exclude)

    # generate a list of eigensystems in vault
    os.chdir(work_path)
    transfer=os.listdir(os.getcwd())
    # save transfer file for rsync
    with open('include.txt',"a") as inc:
        inc.write("\n".join(map(lambda x: str(x),include)))
    with open('exclude.txt',"a") as exc:
        exc.write("\n".join(map(lambda x: str(x),exclude)))
    
    print("Archiving complete. To transfer archive files change to %s and run:" %(work_path))
    print("ls | grep tar > transfer.txt")
    print("and afterwards:")
    print("rsync -v --files-from=include.txt ./ %s@%s:%s > transfer.log " %(remote_user,remote_host,remote_path))
    #subprocess.call(rsync_args)
    # delete transfer file
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
