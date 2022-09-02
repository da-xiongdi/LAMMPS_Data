import os.path

import numpy as np

import ReadFile
import LocateCL
import Fit
import Angle


def radium(input_file, frequency, rho, surface, base, equili=0, liquid_type=True):
    path = os.path.split(input_file)[0]
    file = os.path.split(input_file)[1]
    suffix = '.' + file.split('.')[-1]
    file = file.strip(suffix)
    keywords = file.split('-')

    index = path.split('/')[-1]
    if len(keywords) == 4:
        save_r_path = path + '/r.%s.%s.%s.%s.txt' % (index, keywords[3], surface, base)
    else:
        save_r_path = path + '/r.%s.%s.%s.%s.%s.txt' % (index, keywords[3], keywords[4], surface, base)

    data = ReadFile.ReadChunk(input_file, frequency)
    validdata = data.read3DChunk()[0][equili:]

    rho_s = rho * surface  # 1.28
    cl = LocateCL.Cl(validdata, rho_s, base, liquid_type)
    clCoord = cl.drop()

    np.savetxt(save_r_path, clCoord)


def ca(input_file, frequency, surface, base, equili=0):
    path = os.path.split(input_file)[0]
    file = os.path.split(input_file)[1]
    suffix = '.' + file.split('.')[-1]
    file = file.strip(suffix)

    strength = file.split('-')[3]
    index = path.split('/')[-1]

    save_a_path = path + '/ca.%s.%s.%s.%s.txt' % (index, strength, surface, base)
    save_c_path = path + '/contour.%s.%s.%s.%s.txt' % (index, strength, surface, base)
    save_f_path = path + '/fit.%s.%s.%s.%s.txt' % (index, strength, surface, base)

    data = ReadFile.ReadChunk(input_file, frequency)
    validdata = data.read3DChunk()[0][equili:]

    rho = 1.28 * surface
    cl = LocateCL.Cl(validdata, rho, base)
    contours = cl.contour()

    angle = np.zeros(frequency - equili)
    n = 0
    for contour in contours:
        contour = np.array(contour)
        zero = np.zeros((len(contour), 1))
        fitdata = np.hstack((contour, zero)).T

        fit = Fit.Fit(fitdata)
        fitpara = fit.circleFit()
        ca = Angle.CLAngle(fitpara, base)
        angle[n] = ca.circleAngle
        n += 1

    np.savetxt(save_c_path, contours[-4])
    np.savetxt(save_f_path, fitpara)
    np.savetxt(save_a_path, angle)
