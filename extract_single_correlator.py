import numpy as np
import os
import sys
import pandas as pd
from pandas import Series, DataFrame
import h5py

# Taken from chjost:analysis-code/analysis2/in_out.py
def check_write(filename, verbose=False):
    """Do some checks before writing a file.

    Checks if the folder containing the file exists and create it if
    if does not.

    Parameters
    ----------
    filename : str
        The name of the file
    verbose : bool
        Toggle info output
    """
    # check if path exists, if not then create it
    _dir = os.path.dirname(filename)
    if (_dir != '') and not os.path.exists(_dir):
        os.mkdir(_dir)
    # check whether file exists
    if os.path.isfile(filename):
        if verbose:
            print(filename + " already exists, overwritting...")

# Taken from chjost:analysis-code/analysis2/in_out.py
def write_data_ascii(data, filename, verbose=False):
    """Writes the data into a file.

    The file is written to have L. Liu's data format so that the first line
    has information about the number of samples and the length of each sample.

    Args:
        filename: The filename of the file.
        data: The numpy array with data. Shape must be (samples, time)
        verbose: The amount of info shown.
    """
    # check file
    check_write(filename)
    if verbose:
        print("saving to file " + str(filename))

    # in case the dimension is 1, treat the data as one sample
    # to make the rest easier we add an extra axis
    if len(data.shape) == 1:
        data = data.reshape(1, -1)
    # init variables
    nsamples = data.shape[0]
    T = data.shape[1]
    L = int(T/2)
    # write header
    head = "%i %i %i %i %i" % (nsamples, T, 0, L, 0)
    # prepare data and counter
    #_data = data.flatten()
    _data = data.reshape((T*nsamples), -1)
    _counter = np.fromfunction(lambda i, *j: i%T,
                               (_data.shape[0],) + (1,)*(len(_data.shape)-1),
                               dtype=int)
    _fdata = np.concatenate((_counter,_data), axis=1)
    # generate format string
    fmt = ('%.0f',) + ('%.14f',) * _data[0].size
    # write data to file
    np.savetxt(filename, _fdata, header=head, comments='', fmt=fmt)

# Taken from maowerner:sLapH-projection/src/raw_data.py
def read_configuration(filename, groupname, use_imim = True):
    comb = True if diagram == 'C4cD' else False

    try:
        fh = h5py.File(filename, "r")#, driver='core')
    except IOError:
        print 'file %s not found' % filename
        raise

    # read data from file as numpy array and interpret as complex
    # numbers for easier treatment
    try:
        ret = fh[groupname][('re_full', 'im_full')].view(complex)
    except KeyError:
        print("could not read %s from %s" % (groupname, filename))
        exit(1)

    return ret

##########################################################################################

ensemble_configs = {'A40.24' : [i for i in range(714, 2750+1, 2) if i != 1282],
                 'A40.32' : range(200, 1200+1, 2)}

for ensemble in ['A40.24', 'A40.32']:
    path = os.path.join(*['/hiskp4', 'ueding', 'three-pion', 'contractions', ensemble, 'correlators'])
    configs = ensemble_configs[ensemble]

    data = {}
    for diagram in ['C2c', 'C4cD', 'C4cC']:
        groupname = 'C2c_uu_p000.d000.g5_p000.d000.g5' if diagram is 'C2c' else '{}_uuuu_p000.d000.g5_p000.d000.g5_p000.d000.g5_p000.d000.g5'.format(diagram)
    
        data[diagram] = np.array([read_configuration(os.path.join(path , '{}_cnfg{:04}.h5'.format(diagram, cnfg)), groupname) for cnfg in configs])
      
    write_data_ascii(np.real(data['C2c']), os.path.join('I2', '{}_pi-charged.txt'.format(ensemble)))
    write_data_ascii(np.real(2 * data['C4cD']), os.path.join('I2', '{}_D.txt'.format(ensemble)))
    write_data_ascii(np.real(data['C4cC']), os.path.join('I2', '{}_X.txt'.format(ensemble)))

