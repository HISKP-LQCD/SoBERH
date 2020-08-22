import argparse
import sys
import os.path

def arg_parser():
    progname = os.path.basename(sys.argv[0])
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--source_path", help="Path to data locally", required=True)
    parser.add_argument("--first_config", type=int, help="Number of first gauge configuration", required=True)
    parser.add_argument("--delta_config", type=int, help="Number of  gauge configuration distance", required=True)
    parser.add_argument("--final_config", type=int, help="Number of last gauge configuration", required=True)

    parser.add_argument("--skip_configs", help=("Comma-separated list of configuration"
                                                "indices which should be skipped in the archival process"))

    parser.add_argument("--error_on_missing", 
                        help=("React to a missing configuration by aborting execution"
                              "otherwise just remove it from the target list and continue"),
                        dest="error_on_missing",
                        action="store_true",
                        default=True)
    
    # Setting the login information for Juelich. Please ensure access permission
    if progname == "archive_eigsys.py" or progname == "archive_perams.py":
        parser.add_argument("--remote_user", help="Name of user to log onto archive ", required=True)
        parser.add_argument("--remote_host", help="Name of host to log onto archive Default: %(default)s", default="judac")
        parser.add_argument("--chunksize",
                            type=int,
                            help="Number of gauge configurations per tar archive. Default: %(default)s",
                            default = 50)
        parser.add_argument("--ens", help="Name of ensemble", required=True)

    # some arguments depend on whether we are dealing with eigensystems,
    # perambulators or contracted diagrams
    if progname == "archive_perams.py":
        parser.add_argument("--otf", help="Perform rsync 'on the fly', deleting the .tar after rsync exit status 0",
                            dest="otf", 
                            action="store_true",
                            default=False)
        parser.add_argument("--flv", help="Name of flavour", required=True)
        parser.add_argument("--work_path", 
                            help=("Path in which the .tar files will be created locally, "
                                  "the ensemble and flavour names will be appended. Default: %(default)s"),
                            default="/hiskp4/peram_vault/")
        parser.add_argument("--remote_path", 
                            help="Remote archival path, the ensemble and flavour names will be appended. Default: %(default)s", 
                            default="/p/arch2/hbn28/project/sLapH_perambulators/")
        parser.add_argument("--rsync_opts", 
                            help="Optional arguments for rsync (e.g. --progress): %(default)s", 
                            default="")

    if progname == "archive_eigsys.py":
        parser.add_argument("--otf", help="Perform transfer 'on the fly', piping the output of the tar command directly to ssh.",
                            dest="otf", 
                            action="store_true",
                            default=False)
        parser.add_argument("--work_path", 
                            help=("Path in which the .tar files will be created locally, "
                                  "the ensemble name will be appended. Default: %(default)s"),
                            default="/hiskp4/eigsys_vault/")
        parser.add_argument("--remote_path", 
                            help="Remote archival path, the ensemble name will be appended. Default: %(default)s", 
                            default="/p/arch2/hbn28/project/eigensystems/")

    if progname == "archive_eigsys.py" or progname == "check_eigsys_v2.py":
        parser.add_argument("--Lt", type=int, help="Time extent of ensemble", required=True)
        parser.add_argument("--Ls", type=int, help="Spatial extent of ensemble", required=True)
        parser.add_argument("--Nev", type=int, help="Number of LapH eigenvectors per time slice", required=True)

    return parser

