import argparse

def arg_parser():
    parser = argparse.ArgumentParser()
# Se    t the lattice parameters
    parser.add_argument("--ens", help="Name of ensemble", required=True)
    parser.add_argument("--flv", help="Name of flavor", required=True)

    parser.add_argument("--otf", help="Perform rsync 'on the fly', deleting the .tar after rsync exit status 0", dest="otf", action="store_true", default=False)
    
    parser.add_argument("--first_config", type=int, help="Number of first gauge configuration", required=True)
    parser.add_argument("--delta_config", type=int, help="Number of  gauge configuration distance", required=True)
    parser.add_argument("--final_config", type=int, help="Number of last gauge configuration", required=True)
    
    parser.add_argument("--chunksize", type=int, help="Number of gauge configurations per tar archive (default: %(default)s)", default = 50) 
    # Setting the login information for Jueich. Please ensure access permission
    parser.add_argument("--USER", help="Name of user to log onto archive (default: %(default)s)", default="hch026")
    parser.add_argument("--HOST", help="Name of host to log onto archive (default: %(default)s)", default="judac")
    
    # Setting target path for archive and tar locally 
    # and then rsync to juelich archive rsync destination
    parser.add_argument("--SRC", help="Path to data locally", required=True)
    parser.add_argument("--WRK", help="Path to archive locally (default: /hiskp2/werner/peram_vault/)")
    parser.add_argument("--SNC", help="Path to archive remote default: /arch/hch02/hch026/LapH_perambulators/)")
    return parser 

