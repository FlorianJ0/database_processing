import scipy as sp
from scipy.misc import imread, imsave
from scipy.signal.signaltools import correlate2d as c2d
from scipy import ndimage

import time

dirr = '/home/p0054421/MEGA/calcul/CFD_MRI_VALID/'


def get(i, gauss):
    # get JPG image as Scipy array, RGB (3 layer)
    data = imread(i)

    print 'image', i, 'read'

    # convert to grey-scale using W3C luminance calc
    data = sp.inner(data, [299, 587, 114]) / 1000.0

    print 'image converted to grey-scale'

    if gauss:
        data = ndimage.gaussian_filter(data, 4)
        print 'image smoothed'
        imsave(i + '_gauss.png', data)
    # normalize per http://en.wikipedia.org/wiki/Cross-correlation
    return (data - data.mean()) / data.std()



ttot = time.time()

im1 = get(dirr + 'cfd2.png', 0)
im2 = get(dirr + 'mri2.png', 1)

print ''
print ''
print ''
print '-----------------------------------------------------'
print ''
print 'ref image shape:', im1.shape
print ''
print '------------%%%%%%%%%%%%%%%%%%%%%%%------------------'
print ''
print 'moving image shape:', im2.shape
print ''
print '-----------------------------------------------------'

c11 = c2d(im1, im1, mode='same', boundary='symm')  # baseline
imsave(dirr + 'c11.png', c11)
c12 = c2d(im1, im2, mode='same', boundary='symm')
imsave(dirr + 'c12.png', c12)

# c13 = c2d(im1, im3, mode='same')
# c23 = c2d(im2, im3, mode='same')
print c11.max()
print c12.max()  # , c13.max(), c23.max()
print ''
print ''
print ''
perf = c12.max() * 100 / c11.max()
print '-----------------------------------------------------'
print ''
print "perf", perf, "%"
print ''
print '------------%%%%%%%%%%%%%%%%%%%%%%%------------------'
print ''
print 'full total time  in %f s ' % (time.time() - ttot)
print ''
print '-----------------------------------------------------'
