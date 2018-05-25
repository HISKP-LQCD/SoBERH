#!/hadron/knippsch/Enthought/Canopy_64bit/User/bin/python

# Small bash script to tar eigensystems
import argument_parsing as ap
import sys, os, tarfile, re, subprocess

def calc_arcsize(t, l, nev,bgn=None,end=None,dst=None):
    evecs_ts = nev*l**3*3*2*8
    # phases have same size as evals
    evals_ts = nev*8
    size = t*(2*evals_ts+evecs_ts)
    if dst is not None:
        size *= ((end-bgn)/dst+1)
    return size

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

def main():
    parser = ap.arg_parser()
    args = parser.parse_args()
    ens = args.ens
    flv = args.flv

    otf = args.otf

    d = args.delta_config
    size = args.chunksize

    USER = args.USER
    HOST = args.HOST

    SRC = args.SRC
    WRK = args.WRK
    SNC = args.SNC

    # Set default for WRK and SNC depending on ens and flv
    if WRK is None:
      WRK='/hiskp2/werner/eigsys_vault/'+ens+'/'+flv+'/'
    try:
       if not os.path.exists(os.path.dirname(WRK)):
           os.makedirs(os.path.dirname(WRK))
    except OSError as err:
       print(err)
    if SNC is None:
      SNC='/arch/hch02/hch026/helmes/eigensystems/'+ens+'/'
    # configuration numbers
    bgn=args.first_config
    end=args.last_config
    dst=args.delta_config
    # Lattice parameters
    time=64
    length=32
    nev=220

    sync=True

    # calculate size of archive of one configuration
    arcsize=calc_arcsize(time,length,nev,bgn,end,dst)
    # Change to sourcefolder
    os.chdir(SRC)
    print(os.getcwd())
    # First look at available eigensystems with check_eigsys
    # WORKAROUND: specify configurations directly
    configs=range(bgn,end+1,dst)
        
    # tar configurations to eigsys_vault
    # per configuration open one tar archive
    include=[]
    exclude=[]
    arcname=WRK+'/eigsys_%04d-%d-%04d'%(bgn,dst,end)+'.tar'
    filenames=[]
    for c in configs:
    # create filenames for configs in range
        if os.path.lexists('eigenvectors.%04d.%03d' %(c,time-1)):
            for t in range(time):
            # TODO: there has to be something more elegant
                filenames.append('eigenvectors.%04d.%03d' %(c,t))
                filenames.append('eigenvalues.%04d.%03d' %(c,t))
                filenames.append('phases.%04d.%03d' %(c,t))
        else:
            print('Configuration %d not existing.' %c)
    with tarfile.open(arcname,"w",dereference=True) as tar:
        for name in filenames:
            tar.add(name)
    # check expected filesize vs actual one and decide whether to sync or not
    # TODO: refine that
    #sync=cmp_sizes(arcname,arcsize)
    cmp_sizes(arcname,arcsize,include,exclude)

    # generate a list of eigensystems in vault
    os.chdir(WRK)
    transfer=os.listdir(os.getcwd())
    # save transfer file for rsync
    with open('include.txt',"a") as inc:
        inc.write("\n".join(map(lambda x: str(x),include)))
    with open('exclude.txt',"a") as exc:
        exc.write("\n".join(map(lambda x: str(x),exclude)))
    #TODO:adapt tar command    
    # rsync configurations to archive destination with --from-file
    #rsync_args=['rsync','--files-from=include.txt' ,'./', USER+'@'+HOST+':'+SNC]
    print("Archiving complete. To transfer archive files change to eigsys_vault and run:")
    print("ls | grep tar > transfer.txt")
    print("and afterwards:")
    print("rsync -v --files-from=include.txt ./ %s@%s:%s > transfer.log " %(USER,HOST,SNC))
    #subprocess.call(rsync_args)
    # delete transfer file
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
