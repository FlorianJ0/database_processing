import pydicom
import os

acquis_folder = os.getcwd()
# get image size
im = acquis_folder + '/' + \
     [f for f in os.listdir(acquis_folder) if os.path.isfile(os.path.join(acquis_folder, f))][0]

imm = pydicom.read_file(im)

e = 0.5 * imm.SliceThickness

print 'Slice thickness is ', e, 'mm'

dx = imm.PixelSpacing[0]

output_fname = os.path.split(im)[0] + '.nrrd'
dx = str(dx) + ' ' + str(dx) + ' ' + str(dx)

command = 'vmtkimagereslice -ifile ' + im + ' -ofile ' + output_fname + ' -spacing ' + dx + ' -interpolation cubic'

if e <= 1.5:
    print 'resliced file name will be', output_fname
    print 'reslicing'
    call(command, shell=True)
