import numpy as np
from globals import *

import matplotlib.pyplot as plt
from scipy.misc import derivative
from scipy.stats import linregress as linear
from scipy import interpolate
from excel_export import *

def calc_der(data_set, interpolated, Ts):
    odvodi = []
    for i in range(len(data_set)):
        odvodi.append(derivative(interpolated[i], Ts, dx=1e-4))
    return np.array(odvodi)

def baseline_calc(baseline_number_of_points):
    baseline = []
    for i in range(len(data_set)):
        k = 3
        rvalue = 1
        if baseline_number_of_points < 0:
            while k < 15 and rvalue >= 0.80:
                Kupper, Nupper, rvalue, _, stderr = linear(T[i][-k:], A[i][-k:])
                if i == 1: print(stderr, rvalue)
                k += 1
            k = 3
            rvalue = 1
            while k < 15 and rvalue >= 0.80:
                Klower, Nlower, _, rvalue, stderr = linear(T[i][:k], A[i][:k])  # the lower baseline
                if i == 1: print(stderr, rvalue)
                k += 1
        else:
            k = baseline_number_of_points
            Kupper, Nupper, rvalue, _, stderr = linear(T[i][-k:], A[i][-k:])
            Klower, Nlower, _, rvalue, stderr = linear(T[i][:k], A[i][:k])
        if T[i][0] >= T[i][len(T[i])-1]:
            tmp = [Kupper,Nupper]
            Kupper=Klower
            Nupper=Nlower
            Klower=tmp[0]
            Nlower=tmp[1]

        baseline.append([Klower, Nlower, Kupper, Nupper])

    return np.array(baseline)

def ff_calc(baseline):
    ff = []
    for i in range(len(data_set)):
        tmp=np.array(T[i])
        Klower=baseline[i][0]
        Nlower=baseline[i][1]
        Kupper = baseline[i][2]
        Nupper = baseline[i][3]
        tAf = Klower*tmp+Nlower
        tAu = Kupper*tmp+Nupper
        ff.append(((A[i]-tAu)/(tAf-tAu)))

    return np.array(ff)

def linear_fit(x1, x2, y1, y2, val=0.5):
    # Finds such x that y = val (0.5)
    k,n,_,_,_=linear([x1,x2],[y1,y2])
    return (val-n)/k

def getTmCorrection(h, s, c):
    return h/(-0.008314*(np.log(2/(c*1e-6))-s/8.314))-273.15

def quad(a,b,c):
    # finds 1 solution of the quadratic equation
    d=b*b-4*a*c
    return (-b - np.sqrt(d))/(2*a)

def getExtrapolatedAbsorbance(at_temperature, baseline, i):
    return baseline[i][0]*at_temperature+baseline[i][1]