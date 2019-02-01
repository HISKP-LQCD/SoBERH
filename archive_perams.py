#!/usr/bin/python3

# Small bash script to tar perambulators in packages of configurations
import conf_utils
import argument_parsing as ap
import sys, os, tarfile, re, subprocess

def main():
    parser = ap.arg_parser()
    args = parser.parse_args()

    ens = args.ens
    flv = args.flv

    otf = args.otf

    d = args.delta_config
    chunksize = args.chunksize

    remote_user = args.remote_user
    remote_host = args.remote_host

    source_path = args.source_path
    work_path = args.work_path
    remote_path = args.remote_path

    rsync_opts = args.rsync_opts

    # Set default for work_path and remote_path depending on ens and flv
    work_path=work_path+'/'+ens+'/'+flv+'/'
    try:
       if not os.path.exists(os.path.dirname(work_path)):
           os.makedirs(os.path.dirname(work_path))
    except OSError as err:
       print(err)
    
    remote_path=remote_path+'/'+ens+'/'+flv+'/'

    ################################################################################

    # create a list of configs to tar, add one config in the end because python
    cfg_want = ['cnfg%04d' % c for c in range(args.first_config, args.final_config+1,int(d))]

    # check wether all configurations are there
    # get names
    cfg_have = os.listdir(source_path)
    # test and sort list
    # regular expression containing "cnfg" followed by at least one int
    reg = re.compile(r'cnfg\d+')
    cfgs_reg = filter(reg.match, cfg_have)
    cfgs_new = conf_utils.natural_sort(cfgs_reg)

    # Restrict cfgs_want to the subset we have and print all configurations in 
    # cfg_want but not in cfg_have
    for c in conf_utils.natural_sort(set(cfg_want) - set(cfg_have)):
      print('Skipping configuration ', c)
    cfgs_cut = set(cfg_want).intersection(cfg_have)

    # sort intersection
    cfgs_tar = conf_utils.natural_sort(cfgs_cut)
    print('Archiving: ', cfgs_tar)

    # chunks for taring
    chunks = [cfgs_tar[i:i+chunksize] for i  in range(0, len(cfgs_tar), chunksize)]
    EXCLUDE_FILES=['main']
    arclist = []
    for c in chunks:
      b=c[0]
      e=c[-1]
      # distance in filename from interval
      # First create a list with the according configurations
      
      os.chdir(source_path)
      # Now we want to tar everything in the range list into one specific tar archive
      arcname=work_path+'perams_' +b[4:] + '-' + str(d) + '-' +e[4:]+ '.tar'
      if os.path.isfile(arcname) is False:
        with tarfile.open(arcname,"w",dereference=True) as tar:
          for name in c:
            tar.add(name,filter=lambda x: None if x.name in EXCLUDE_FILES
                else x)
      else:
        print('Archive already exists. Did not write!')
      
      # if "on the fly archival" is disabled, we will transfer all
      # files in one big sweep later and not delete them 
      if otf is False:
        arclist.append(arcname)
      else:  
      # on the fly archival to save space
        rsync_args=['rsync',rsync_opts, arcname, remote_user+'@'+remote_host+':'+remote_path]
        rval=subprocess.call(rsync_args)
        # delete file if rsync was successful
        if rval == 0:
          os.remove(arcname)

    ## Rsync perambulator archive to destination
    if otf is False:
      for name in arclist:
        rsync_args=['rsync',rsync_opts, name, remote_user+'@'+remote_host+':'+remote_path]
        subprocess.call(rsync_args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
