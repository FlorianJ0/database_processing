import multiprocessing
import os
import shutil
from shutil import ignore_patterns
import math
import vtk
import time
import subprocess
from vmtk import pypes

import PyFoam
import PyFoam.FoamInformation
print 'foam version', PyFoam.FoamInformation.foamVersion()

"""
file naming: AAA_ACAB_YYYYMMDD.stl      > segmentation file
file naming: AAA_ACAB_YYYYMMDD_0.stl    > cleaned segmentation file
file naming: AAA_ACAB_YYYYMMDD_1.stl    > cleaned segmentation file + taubin smoothing
file naming: AAA_ACAB_YYYYMMDD_2.stl    > cleaned + outlet extensions segmentation file
file naming: AAA_ACAB_YYYYMMDD_3.stl    > cleaned + outlet extensions + inlet extension segmentation file
"""

src = '/media/I/DataCRCHUM/Inter_Equipe/Kauffmann_Claude/AAA_Fluide_IE/Database_FLOW/patients_images/sorted/'
dest = '/home/p0054421/Downloads/test_import/'
network = '/home/p0054421/Downloads/test_import/AAA_FR/foo2.vtp'

mission = 'ctrl'
patient_path_list = []
for d in os.listdir(dest):
    patient_path_list.append(os.path.join(dest, d))

ncpus = 7
# print patient_path_list

patient_names_list = []
for d in os.listdir(dest):
    patient_names_list.append(d)

patient_names_list.sort()
# patient_names_list = patient_names_list[0:7]
patient_number = len(patient_names_list)

if mission == 'import':
    for dirname, dirnames, filenames in os.walk(src):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            a = os.path.join(dirname, subdirname)
            # print 'dirname', dirname
            # print 'subdirname', subdirname
            # print subdirname[:3]
            if subdirname[:3] == 'seg':
                toto = dest + '/' + os.path.split(dirname)[1]
                # print a
                # os.makedirs(toto)
                src = a + '/'
                dst = toto + '/'
                # print toto
                shutil.copytree(src, dst, ignore=ignore_patterns('*.mha', '*.nrrd'))

if mission == 'network':
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(network)
    reader.Update()
    idList = vtk.vtkIdList()
    polyDataOutput = reader.GetOutput()
    # a = polyDataOutput.GetPoints().GetData()
    # a = numpy_support.vtk_to_numpy(a)
    # print a
    # print polyDataOutput.GetPoints().Get

if mission == 'ctrl':

    cpus = []

    if ncpus > patient_number:
        ncpus = patient_number
        print 'trop de cpus, running on ' + str(ncpus)
    ncas = int(math.ceil(float(patient_number) / ncpus))
    # reste = patient_number % ncpus

    print '\n'
    print "patients repartition on", ncpus, 'cpus'
    print patient_number, ' = ', ncas, ' * ', ncpus
    print '\n'



    for i in xrange(ncpus):
        s = i * ncas
        f = i * ncas + ncas
        # print s, f
        if s != 0:
            s -= 0

        cpus.append([])
        cpus[i] = (patient_names_list[s:f])
        # print cpus[i], '\n'
    # print patient_names_list

    t=time.time()

    def worker(proc):
        print 'Worker:', proc
        pid =  'process id:', os.getpid()

        k = 0
        for i in cpus[proc]:
            dest_patient = dest + i + '/'
            flist = os.listdir(dest_patient)
            flist.sort()
            for j in flist:
                if j.endswith('_0.stl') or j.endswith('_1.stl') or j.endswith('_2.stl') or j.endswith('_3.stl'):
                    surf = dest_patient+j
                    # a = 'meshlabserver -i ' + surf + ' -o ' + surf
                    # print a
                    # os.system(a)
                    a = 'vmtksurfaceviewer -ifile '+ surf
                    myPype = pypes.PypeRun(a)




        return


    if __name__ == '__main__':
        jobs = []
        for i in range(ncpus):
            p = multiprocessing.Process(target=worker, args=(i,))
            jobs.append(p)
            p.start()

