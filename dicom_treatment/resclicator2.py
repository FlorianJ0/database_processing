#!/usr/bin/env python

import sys
import itk

# if len(sys.argv) != 4:
#     print("Usage: " + sys.argv[0] + " <inputImage> <outputImage> <scale>")
#     sys.exit(1)


acquis_folder = os.getcwd()
# get image size
im = acquis_folder + '/' + \
     [f for f in os.listdir(acquis_folder) if os.path.isfile(os.path.join(acquis_folder, f))][0]




imm = pydicom.read_file(im)
# inputImage = sys.argv[1]
inputImage = im
# outputImage = sys.argv[2]
outputImage = os.path.split(im)[0] + '.nrrd'

# scale = float(sys.argv[3])
scale = 2.0

PixelType = itk.UC
ScalarType = itk.D
Dimension = 2

ImageType = itk.Image[PixelType, Dimension]

ReaderType = itk.ImageFileReader[ImageType]
reader = ReaderType.New()
reader.SetFileName(inputImage)
reader.Update()

inputImage = reader.GetOutput()

size = inputImage.GetLargestPossibleRegion().GetSize()
spacing = inputImage.GetSpacing()

centralPixel = itk.Index[Dimension]()
centralPixel[0] = size[0] / 2
centralPixel[1] = size[1] / 2
centralPoint = itk.Point[ScalarType, Dimension]()
centralPoint[0] = centralPixel[0]
centralPoint[1] = centralPixel[1]

scaleTransform = itk.ScaleTransform[ScalarType, Dimension].New()

parameters = scaleTransform.GetParameters()
parameters[0] = scale
parameters[1] = scale

scaleTransform.SetParameters(parameters)
scaleTransform.SetCenter(centralPoint)

interpolatorType = itk.LinearInterpolateImageFunction[ImageType, ScalarType]
interpolator = interpolatorType.New()

resamplerType = itk.ResampleImageFilter[ImageType, ImageType]
resampleFilter = resamplerType.New()

resampleFilter.SetInput(inputImage)
resampleFilter.SetTransform(scaleTransform)
resampleFilter.SetInterpolator(interpolator)
resampleFilter.SetSize(size)
resampleFilter.SetOutputSpacing(spacing)

WriterType = itk.ImageFileWriter[ImageType]
writer = WriterType.New()
writer.SetFileName(outputImage)
writer.SetInput(resampleFilter.GetOutput())

writer.Update()