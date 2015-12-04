__author__ = 'p0054421'
import numpy as np
import os
import os.path
import re
import shutil
import time
from os.path import expanduser
import pydicom
from anonymisator import anonymize

folder = '/media/I/DataCRCHUM/Inter_Equipe/Kauffmann_Claude/AAA_Fluide_IE/Database_FLOW/patients_images/recup_initial_simon/'
# folder = "/home/p0054421/Downloads/testDicom/test/"

def contained_dirs(dir):
    return filter(os.path.isdir,
                  [os.path.join(dir, f) for f in os.listdir(dir)])



aquis_list = contained_dirs(folder)


for i in aquis_list:
    if not os.listdir(i):
        print i, "is empty"
        continue

    else:
        series_list = contained_dirs(i)

        patient_folder = os.path.split(i)[1]
        if patient_folder[:6] == 'AAA_VC':
            # for j in series_list:
            #     sub = contained_dirs(j)
            print patient_folder
            for k in series_list:
                acquis_folder = k
                im = acquis_folder + '/' + \
                             [f for f in os.listdir(acquis_folder) if os.path.isfile(os.path.join(acquis_folder, f))][0]
                imm = pydicom.read_file(im)
                date = imm.StudyDate
                new_name = i+'/'+patient_folder+'_'+date
                print 'old name'
                print k
                print 'new name'
                print new_name
                if os.path.exists(new_name):
                    new_name +=  '_doublon-' + str(int(np.array([time.clock()])[0] * 10000))

                os.rename(k, new_name)
                print ''
