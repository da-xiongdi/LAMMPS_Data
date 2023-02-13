import sys

import numpy as np
import scipy.integrate
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
from sympy import *

para_ad = [[7.05e-7,61700],[6.37e-9,84000],[2.16e-5,46800]] # 1/bar
para_eq = [[5139,12.621],[3066,10.592],[-2073,-2.029]]
para_rate = [[4.89e7,-63000],[9.64e11,-152900],[1.09e5,-87500]] # mol/s/kg/bar**0.5
def react1(p1,p2,p3,p4,p5,T):
    rate =0