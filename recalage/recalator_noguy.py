# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 11:19:48 2014

@author: florian
"""

import os
# sys.path.insert(0,"/home/florian/visit2_6_3.linux-x86_64/2.6.3/linux-x86_64/lib/site-packages/")
import numpy as np
# from scipy.optimize import minimize
from subprocess import call
import pandas
import os.path
from vmtk import pypes

# dirr = os.getcwd()
dirr = '/home/p0054421/Downloads/testDicom/recal/'


# refsurfname='20060124_7.stl'
# surfname='20120403_7.stl'
# print 'refsurfname', refsurfname
# print 'surfname', surfname

# print '''
#
#
# ██████╗ ███████╗ ██████╗ █████╗ ██╗      █████╗ ████████╗ ██████╗ ██████╗
# ██╔══██╗██╔════╝██╔════╝██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
# ██████╔╝█████╗  ██║     ███████║██║     ███████║   ██║   ██║   ██║██████╔╝
# ██╔══██╗██╔══╝  ██║     ██╔══██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
# ██║  ██║███████╗╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
# ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
#
#
# Registration only works with surface, vtp, stl etc. If a mesh (vtk) is to be registered:
# i)register a surface from the same case
# ii) at the end choose the good option
# iii) be nice to your mom
#
# mkay ?
# '''
# raw_input("Press Enter to continue...")

# initial dir


# Input: expects Nx3 matrix of points
# Returns R,t
# R = 3x3 rotation matrix
# t = 3x1 column vector
# http://nghiaho.com/?page_id=671
######
######
######
def scanator(dirr):
    # print 'scan dir to find *.stl correctly written i.e. patient-name_YYYY-MM-DD.stl'
    # print 'UN SEUL PATIENT A LA FOIS !'
    fs = [".vtkxml", ".vtk", ".stl", ".ply", ".tecplot", ".vtp"]
    flist = os.listdir(dirr)

    dt = np.dtype([('case', np.str_, 2000), ('date', pandas.tslib.Timestamp)])
    # print dt
    scans = np.zeros((30, 1), dtype=dt)

    j = 0
    for i in flist:
        for k in fs:
            if os.path.splitext(i)[1] == k:
                if os.path.splitext(i)[1] != '.vtp':
                    ifile = dirr + i
                    ofile = dirr + os.path.splitext(i)[0] + '.vtp'
                    cmmd = 'vmtksurfacewriter -ifile ' + ifile + ' -ofile ' + ofile
                    print cmmd
                    call(cmmd, shell=True)

                fname = dirr + os.path.splitext(i)[0]

                # print pandas.to_datetime(os.path.splitext(i)[0][-10:])
                scans[j, 0] = (fname, pandas.to_datetime(os.path.splitext(i)[0][-10:]))
                j += 1

    scans = scans[:j, :]
    s = np.sort(scans, axis=0)
    print s
    return s


def rigid_transform_3D(A, B, filename):
    assert len(A) == len(B)

    N = A.shape[0]  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    # centre the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

    # dot is matrix multiplication for array
    H = np.transpose(AA) * BB

    U, S, Vt = np.linalg.svd(H)

    R = Vt.T * U.T

    # special reflection case
    if np.linalg.det(R) < 0:
        print "Reflection detected"
        Vt[2, :] *= -1
        R = Vt.T * U.T

    t = -R * centroid_A.T + centroid_B.T
    t = np.array(t)
    R = np.array(R)

    #    print np.shape(t), np.shape(R)
    mat_trans = np.c_[R, np.zeros(3)]
    mat_trans = np.r_[mat_trans, [np.zeros(4)]]
    tt = np.r_[t, [[1]]]
    mat_trans[:, 3] = tt[:, 0]
    print 'mat tranformation'
    print mat_trans
    fname = filename + '_transformation-matrix.dat'
    np.savetxt(fname, mat_trans)
    return R, t


def centerlines(filename):
    command = "vmtkcenterlines  -seedselector openprofiles -ifile " + filename + \
              ".vtp -ofile " + filename + "_cl.vtp --pipe vmtkbranchextractor --pipe vmtkbifurcationreferencesystems --pipe vmtkbifurcationvectors -ofile " + \
              filename + ".dat"
    if not os.path.isfile(filename + '.dat'):
        call(command, shell=True)
    return


def displace(registered_file, R, t, rm=False):
    commandS = "vmtksurfacetransform -ifile " + registered_file + ".vtp -matrix " + str(R[0, 0]) + " " + str(
        R[0, 1]) + " " + str(R[0, 2]) + " " + str(t[0, 0]) + " " + str(R[1, 0]) + " " + str(
        R[1, 1]) + " " + str(R[1, 2]) + " " + str(t[1, 0]) + " " + str(R[2, 0]) + " " + str(R[2, 1]) + " " + str(
        R[2, 2]) + " " + str(t[2, 0]) + " 0 0 0 1 " + "-ofile " + registered_file + "_registered.vtp"

    pypes.PypeRun(commandS)
    print "VMTK command used for displacement: " + commandS
    if rm:
        os.remove(registered_file + '.vtp')

    return


def read_object(registered_file):
    #   print(registered_file)
    centerlines(registered_file)
    arr = []
    inp = open(registered_file + ".dat", "r")
    # read line into array
    for line in inp.readlines()[1:]:
        #         add a new sublist
        #        arr.append([])
        # loop over the elemets, split by whitespace
        lastel = line.split()[-1]
        if (float(lastel) >= 5) and (float(lastel) <= 7):
            arr.append([])
            for i in line.split():
                i = np.double(i)
                #                print 'i',line.split()[-1]
                arr[-1].append(i)

    arrlen = np.shape(arr)[0]
    print "number of bifurcation points: ", arrlen
    aa = np.array([arr[0][0:3]])
    for i in range(1, arrlen):
        aa = np.concatenate((aa, np.array([arr[i][0:3]])), axis=0)
        i += 1

    A = np.mat(aa)
    print 'File to be registered read'
    return A, registered_file


######
######
######
def recal(reference_file, registered_file):
    # calcul des points de recalage (A) du fichier a recaler .
    print "Reference surface:\n"
    print(reference_file)
    [A, registered_file] = read_object(registered_file)

    # calcul des points de recalage pour fichier de reference
    # if reference file not exist
    # if not os.path.isfile(reference_file + ".dat"):
    centerlines(reference_file)
    arrb = []
    inpb = open(reference_file + ".dat", "r")
    # read line into array

    for line in inpb.readlines()[1:]:
        # add a new sublist
        #            arrb.append([])
        # loop over the elemets, split by whitespace
        lastel = line.split()[-1]
        if (float(lastel) >= 5) and (float(lastel) <= 7):
            arrb.append([])
            for i in line.split():
                i = np.double(i)
                arrb[-1].append(i)

    arrlenb = np.shape(arrb)[0]
    bb = np.array([arrb[0][0:3]])
    for i in range(1, arrlenb):
        bb = np.concatenate((bb, np.array([arrb[i][0:3]])), axis=0)
        i += 1

    B = np.mat(bb)

    # calcul de la translation t et rotation B pour recaler
    [R, t] = rigid_transform_3D(A, B, registered_file)
    # deplacement de la surface

    displace(registered_file, R, t, True)
    displace(registered_file + '_cl', R, t, True)

    return R, t


def disp_results(refsurfname, surfname):
    dual_view = 'vmtksurfacereader -ifile ' + refsurfname + '.vtp \
    --pipe vmtkrenderer --pipe vmtksurfaceviewer -display 0 \
    --pipe vmtksurfaceviewer -ifile ' + surfname + '_registered.vtp -color 1 0 0 -display 1'

    #    surf_dist='vmtksurfacedistance -rfile '+ refsurfname +' -ifile '+surfname+' \
    #    -distancearray toto \
    #    --pipe vmtkrenderer --pipe vmtksurfaceviewer -array toto'
    pypes.PypeRun(dual_view)
    # vachement trop long


#    myPype0 = pypes.PypeRun(surf_dist)

#
def main():
    scans = scanator(dirr)
    for i in range(0, np.shape(scans)[0] - 1):
        # print scans


        refsurfname = scans[i, 0][0]
        surfname = scans[i + 1, 0][0]
        print surfname, ' will be registered on :', refsurfname
        print 'Are you ready kids?'
        print "Aye Aye Captain!!"
        # quit()
        recal(refsurfname, surfname)
        disp_results(refsurfname, surfname)


main()
# if len(sys.argv) == 1:
#     main()
# elif len(sys.argv) == 3:
#     fs=[".vtkxml",".vtk",".stl",".ply",".tecplot", ".vtp"]
#     k=0
#     for j in range(1,len(sys.argv)):
#         for i in fs:
#             if (((os.path.splitext(str(sys.argv[j]))[1]))==i):
#                 k+=1
# #    print k
#     if (k!=2):
#         print "wrong file format. Choose one in: vtkxml vtk stl ply tecplot"
#         print "p'tit con"
#
#         exit()
#     refsurfname = os.path.splitext(str(sys.argv[1]))[0]
#     surfname = os.path.splitext(str(sys.argv[2]))[0]
#     recal(refsurfname, surfname, False)
#     disp_results(refsurfname, surfname)
# else:
#     sys.exit('Usage: %s ref-file surface-file' % sys.argv[0])
#
# if not os.path.exists(sys.argv[1]):
#     sys.exit('ERROR: Database %s was not found!' % sys.argv[1])
