import os
import pydicom

from subprocess import call

acquis_folder = os.getcwd()
f= []
for (dirpath, dirnames, filenames) in os.walk(acquis_folder):
    f.extend(filenames)
    break
# ll = 0
for k in filenames:
    print k
    im = pydicom.read_file(k)
    print im.PatientID
    im.ImageOrientationPatient = ['1', '0', '0', '0', '1', '0']
    im.save_as(k)