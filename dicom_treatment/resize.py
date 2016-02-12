import os
import pydicom
from vmtk import pypes

from subprocess import call
from medpy.io import load

fold = '/media/backup/patients_article0/patient4/DOIRE^JEAN-LOUIS/DOIRE^JEAN_LOUIS_20110620/LCS/test/'
lum = 'lum.dcm'
lcs = fold + 'DIZ.dcm'
ftle = fold + '2010.mha'
im = pydicom.read_file(lcs)
print im
data = im.pixel_array
print data
#transform mha>dcm to recorver 180 deg transformation
#comm = 'vmtkimagewriter -ifile ' + lcs + ' -ofile '+ fold + 'lcs.dcm'
# print comm
#pypes.PypeRun(comm)

image_data, image_header = load(fold+'DIZ.mha')
