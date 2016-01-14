import os
import pydicom

from subprocess import call

fname = '/media/backup/patients_article0/patient4/DOIRE^JEAN-LOUIS/DOIRE^JEAN_LOUIS_20100617/LCS/lum.mha'

im = pydicom.read_file(k)