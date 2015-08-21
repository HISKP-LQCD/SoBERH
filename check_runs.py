import os, glob

################################################################################
# parameters which need to be set ##############################################
srt_cnfg = 714
end_cnfg = 2330
del_cnfg = 4

nb_rnd_vec = 6

T = 48        # number of timeslices
nb_ev = 120   # number of eigenvectore
I = 24**2     # number of inversions

nb_I_T  = 24  # number of inversions in time
nb_I_EV = 6   # number of inversions in eigenvector space
nb_I_D  = 4   # number of inversions in Dirac space

peram_size = T*nb_ev*4*I*2*8 # 4: Dirac, 2: complex, 8: double precision
rnd_vec_size = T*nb_ev*4*2*8 # 4: Dirac, 2: complex, 8: double precision
################################################################################


for i in range(srt_cnfg, end_cnfg+1, del_cnfg):
  for j in range(nb_rnd_vec):
    path = './cnfg%d' % i + '/rnd_vec_%d' % j
    print 'check path: ' + path

    # checking the perambulator
    filename = path + '/perambulator*'
    fi = glob.glob(filename)
    if(len(fi) == 0):
      print '\tNo perambulator file exists in ' + path
    for k in fi:
      size = os.path.getsize(k)
      if(peram_size != size):
        print '\tSize of perambulator is not correct'
        print '\tsize should be %d' % peram_size + ' but is %d' % size

    # checking the random vector
    filename = path + '/randomvector*'
    fi = glob.glob(filename)
    if(len(fi) == 0):
      print '\tNo randomvector file exists in ' + path
    for k in fi:
      size = os.path.getsize(k)
      if(rnd_vec_size != size):
        print '\tSize of randomvector is not correct'
        print '\tsize should be %d' % rnd_vec_size + ' but is %d' % size

    # check run.out if all inversions are performed
    filename = path + '/run.out'
    check_string = '%d' % (nb_I_T-1) + '\t%d' % (nb_I_EV-1)
    #print check_string 
    try:
      if not check_string in open(filename).read():
         print '\tIt seems that not all Inversions are performed'
    except IOError:
      print "\tCANNOT open", filename



