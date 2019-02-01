#!/usr/bin/python

import os
import glob
import re
import logging
import datetime

# global definitions
global_path = "/hiskp4/perambulators/nf211/"
lat = "A40.24"
verbose = 1
# enable log file
now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
logging.basicConfig(filename='qbigmove_%s_%s.log'% (lat, now),level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s")


# regular expressions for matching
rdirmatch = re.compile("rnd_vec_(\d+)")
permatch = re.compile("perambulator.rndvecnb(\d+).([usc]).TsoB(\d*).VsoI(\d*).DsoF(\d*).TsiF(\d*).SsiF(\d*).DsiF(\d*).CsiF(\d*).smeared(\d).(\d*)")
ranmatch = re.compile("randomvector.rndvecnb(\d+).([usc]).nbev(\d*).(\d*)")

def get_info_per(fname):
    m = permatch.match(fname)
    if m:
        return (int(m.group(1)), m.group(2), int(m.group(10)), int(m.group(11)))
    else:
        return None
    
def get_info_ran(fname):
    m = ranmatch.match(fname)
    if m:
        return (int(m.group(1)), m.group(2), int(m.group(4)))
    else:
        return None

def move_files_nosubdir(srcdir, dstdir, eflavor, move_nonmatched):
    data = sorted(os.listdir(srcdir))
    print(srcdir)
    # move all content in directory
    for d in data:
        # build source path
        src = os.path.join(srcdir, d)
        # if it is a symlink, continue
        if os.path.islink(src):
            #print("skipping symlink %s" % src)
            logging.info("skipping symlink %s" % src)
            continue
        m1 = get_info_per(d)
        m2 = get_info_ran(d)
        cnum=-1
        rnum=-1
        # move if perambulator
        if m1 is not None:
            rnum, flavor, smeared, cnum = m1
            # create destination file name
            fname = d
            # The Quda_4_GPU peram_gen always names the perambulators 
            # rndvecnb00 to avoid disambiguities always replace the random
            # number with the one from the directory
            # TODO: This works for randomvectors but not for perambulators
            # and I have no idea why
            if re.search("/rnd_vec_(\d+)", srcdir):
                erandom = int(re.search("/rnd_vec_(\d+)", srcdir).group(1))
                fname = fname.replace("rndvecnb%2d" % rnum, "rndvecnb%02d" % erandom)
                rnum = erandom
            if ".%s." % eflavor not in flavor:
                fname = fname.replace(".%s." % flavor, ".%s." % eflavor)
            if smeared != 0:
                fname = fname.replace("smeared%d" % smeared, "smeared0")
        # move if randomvector
        elif m2 is not None:
            rnum, flavor, cnum = m2
            # create destination file name
            fname = d
            # The Quda_4_GPU peram_gen always names the perambulators 
            # rndvecnb00 to avoid disambiguities always replace the random
            # number with the one from the directory
            if re.search("/rnd_vec_(\d+)", srcdir):
                erandom = int(re.search("/rnd_vec_(\d+)", srcdir).group(1))
                fname = fname.replace("rndvecnb%02d" % rnum, "rndvecnb%02d" % erandom)
                rnum = erandom
            if ".%s." % eflavor not in flavor:
                fname = fname.replace(".%s." % flavor, ".%s." % eflavor)
        else:
            if move_nonmatched:
                fname = d
                #print(srcdir)
                #print(re.search("/(cnfg|conf)(\d+)/", srcdir))
                cnum = int(re.search("/(cnfg|conf)(\d+)", srcdir).group(2))
                if re.search("/rnd_vec_(\d+)", srcdir):
                    rnum = int(re.search("/rnd_vec_(\d+)", srcdir).group(1))
            else:
                continue
        # build destination path
        if rnum > -1:
            dst = os.path.join(dstdir, "cnfg%04d" % cnum, "rnd_vec_%02d" % rnum, fname)
        else:
            dst = os.path.join(dstdir, "cnfg%04d" % cnum, fname)
        #print("moving\n%s\nto\n%s\n\n" % (src, dst))
        logging.info("moving %s to %s" % (src, dst))
        if os.path.exists(dst):
            logging.warn("file %s exists" % dst)
            continue
        # TODO move
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        os.rename(src, dst)

def flavor_moving(newpath, matches, flavor, eflavor):
    """Do the flavor matching and destination path construction."""
    def light_match(fname):
        # create path to move to
        tmp = md.split("/")[-1].split("_")
        if len(tmp) == 1:
            tmp = "light"
        elif len(tmp) >= 2 and "quark" in tmp[1]:
            tmp = "_".join(["light"] + tmp[2:])
        else:
            tmp = "_".join(["light"] + tmp[1:])
        return tmp
    def other_match(fname, flavor):
        # create path to move to
        tmp = md.split("/")[-1].split("_")
        if len(tmp) == 1:
            tmp = flavor
        else:
            tmp = "_".join([flavor, tmp[1].ljust(4, "0")] + tmp[2:])
        return tmp
    for md in matches:
        if flavor == "light":
            tmp = light_match(md)
        else:
            tmp = other_match(md, flavor)
        # create path to move to
        destpath = os.path.join(newpath, tmp)
        if not os.path.exists(destpath):
            logging.info("created %s" % destpath)
            os.makedirs(destpath)
        print("moving %s quarks from %r" % (flavor, md))
        print("to %r" % destpath)
        logging.info("moving %s quarks from %r to %r" % (flavor, md, destpath))

        # get all configs
        no_config_subdirs = False
        conf_search = os.path.join(md, "cnfg*")
        configs = sorted(glob.glob(conf_search))
        if not configs:
            conf_search = os.path.join(md, "conf*")
            configs = sorted(glob.glob(conf_search))
        # sometimes there are no subfolders
        if not configs:
            configs = md
            no_config_subdirs = True
            if not os.listdir(configs):
                print("Could not find data\nExiting...")
                os.sys.exit(-3)

        if verbose > 0:
            #print("found configs:\n%r" % configs)
            #print("No config subdirs: %r" % no_config_subdirs)
            logging.debug("No config subdirs: %r" % no_config_subdirs)

        #print(configs)
        move_files(configs, destpath, no_config_subdirs, eflavor)


def move_files(srcdirs, dstdir, no_config_subdirs, eflavor):
    """move data files"""

    # subdirs for each config exist
    if not no_config_subdirs:
        logging.debug("subdir branch")
        for sd in srcdirs:
            # get data
            data = sorted(os.listdir(sd))
            # check if contents is only rnd_vec dirs
            # TODO assumes either rnd_vec dirs or no subdirs exist
            tmpr = [x for x in data if rdirmatch.match(x)]
            if not tmpr:
                move_files_nosubdir(sd, dstdir, eflavor, True)
            else:
                for rnddir in tmpr:
                    tmp_src = os.path.join(sd, rnddir)
                    move_files_nosubdir(tmp_src, dstdir, eflavor, True)

    # no subdirs for each config exist
    else:
        #print("no subdir branch")
        logging.debug("no subdir branch")
        move_files_nosubdir(srcdirs, dstdir, eflavor, False)

def main():
    # build new path
    npath = os.path.join(global_path, lat + "_sorted")
    print("moving data to to %s" % npath)
    # discover all paths containing the lat identifier
    path = os.path.join(global_path, lat.split(".")[0] + "*")
    found_paths = glob.glob(path)
    if verbose > 0:
        print("search path %s" % path)
        print("found paths:\n %r" % found_paths)
    if len(found_paths) > 1:
        print("found more than one path:")
        for i, p in enumerate(found_paths):
            print("%d) %s" % (i, p))
        print("Which one to take?")
        n=int(raw_input())
        try:
            fpath=found_paths[n]
        except IndexError:
            print("Could not use %d as index!\nExiting..." % n)
            os.sys.exit(0)
        print("chose %s\n" % fpath)
        logging.info("chose %s\n" % fpath)
        print("Continue? (Y/n)")
        ans = raw_input()
        if ans not in ["Y", "y", ""]:
            print("exiting...")
            os.sys.exit(-1)
    elif len(found_paths) == 1:
        fpath=found_paths[0]
    else:
        print("Could not find anything for %s\nExiting..." % path)
        os.sys.exit(-1)

    ####################
    # get all folders inside directory
    ####################
    search_dirs = os.path.join(fpath,"*")
    found_dirs = glob.glob(search_dirs)
    # sometimes the number of eigenvectors is in the path
    if len(found_dirs) and "nev" in found_dirs[0].split("/")[-1]:
        search_dirs = os.path.join(search_dirs, "*")
        found_dirs = glob.glob(search_dirs)
    # sometimes the dilution scheme is in the path
    dilmatch = re.compile("T[IBNF]*(\d*)_S[IBNF]*(\d*)_L[IBNF]*(\d*)")
    if len(found_dirs) and dilmatch.match(found_dirs[0].split("/")[-1]):
        search_dirs = os.path.join(search_dirs, "*")
        found_dirs = glob.glob(search_dirs)
    if not len(search_dirs):
        print("Could not find anything for %s\nExiting..." % search_dirs)
        os.sys.exit(-2)
    if verbose > 0:
        print("searching for dirs: %s" % search_dirs)
        print("found dirs: %r" % found_dirs)
    logging.info("searching for dirs: %s" % search_dirs)
    logging.info("found dirs: %r" % found_dirs)

    print("###################################")
    # loop over folders
    matchlight = [x for x in found_dirs if "light" in x or "up" in x or "u_quark" in x]
    matchstrange = [x for x in found_dirs if "strange" in x]
    matchcharm = [x for x in found_dirs if "charm" in x]
    others = [x for x in found_dirs if x not in matchlight and x not in matchstrange and x not in matchcharm]
    if not matchlight and not matchstrange and not matchcharm and others:
        test = [x for x in found_dirs if "cnfg" in x]
        # if there are now entries in test, there are no subfolders for quarks
        # assume these are light quarks, in other cases matchlight has to be replaced
        # two lines under this line
        if test:
            matchlight = [ search_dirs ]
        print("no subdirs!")
    logging.info("light folders %r" % matchlight)
    logging.info("strange folders %r" % matchstrange)
    logging.info("charm folders %r" % matchcharm)
    if others:
        print("other directories not moved to new location:\n%r" % others)
        logging.info("other directories not moved to new location:\n%r" % others)
    if not matchlight and not matchstrange and not matchcharm:
        print("nothing to move, all matches empty")
        os.sys.exit(-3)
    print("###################################")

    ## light quarks
    flavor_moving(npath, matchlight, "light", "u")

    print("###################################")
    ## strange quarks
    flavor_moving(npath, matchstrange, "strange", "s")

    print("###################################")
    ## charm quarks
    flavor_moving(npath, matchcharm, "charm", "c")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
