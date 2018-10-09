#!/usr/bin/python
#Python script checking size and numbers of eigensystems listing missing ones
import argument_parsing as ap
import conf_utils
import sys, os, tarfile, re, subprocess
def main():
    parser = ap.arg_parser()
    args = parser.parse_args()
    ens = args.ens

    source_path = args.source_path
    # configuration numbers
    bgn=args.first_config
    end=args.final_config
    dst=args.delta_config
    
    # Lattice parameters
    time=args.Lt
    length=args.Ls
    nev=args.Nev
    fsize=2*8*nev*3*(length**3)
    # loop over configurations
    for cfg in range(bgn, end+1, dst):
        # empty list for missing timeslices
        miss = list()
        for t in range(0,time):
            file = "%s/eigenvectors.%04d"%(source_path,cfg)+".%03d"%t
            if os.path.exists(file):
                if os.path.getsize(file) == fsize:
                  pass
                else:
                  #print(os.path.getsize(file))
                  miss.append(t)
            else:
                miss.append(t)
        if len(miss) > 0:
            if len(miss) > time/2:
                print("More than half of the timeslices missing on cfg %d"%cfg)
            else:
                print("Timeslices "+",".join(map(str, miss))+" missing on cfg %d"%cfg)
        else:
            print "Config %d"%cfg+" complete"
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
