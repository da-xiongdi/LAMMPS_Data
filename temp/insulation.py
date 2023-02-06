import sys

import numpy as np
import scipy.integrate
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
from sympy import *


class Test:

    def __init__(self, T1, T2, pt, fluid, qmt, x):
        self.T2 = T2
        self.T1 = T1
        self.pt = pt
        self.mass = np.array([PropsSI('M', 'T', T1, 'P', pt, fluid[i]) for i in range(len(fluid))])  # kg/mol
        self.p_rs = pt * np.array([x / 4, x / 4, (1 - x) / 4, 3 * (1 - x) / 4])
        self.rho_rs = np.array([PropsSI('D', 'T', T1, 'P', self.p_rs[i], fluid[i]) for i in range(len(fluid))])
        self.q_mass_rs = qmt * self.rho_rs / np.sum(self.rho_rs)
        self.q_mol_rs = self.q_mass_rs / self.mass
        self.fluid = fluid
        # x_mol = q_mol_rs / sum(q_mol_rs)

    @staticmethod
    def ode(T1, T2, c1, c2, dl, u1):
        """
        ode for the concentration distribution along the channel
        the origin is located at the outside
        :param u1: inside velocity
        :param T1: inside temperature
        :param T2: outside temperature
        :param c1: inside concentration
        :param c2: outside concentration
        :param dl: length of the channel
        :return: slop of the concentration at the inside
        """

        # function
        def dydx(x, y):
            a = (T1 - T2) / dl
            b = T2
            c = u1 / (a * dl + b)
            dy0 = y[1]
            dy1 = y[1] * (a * x + b) * c
            return np.vstack((dy0, dy1))

        def bound(ya, yb):
            return np.array([ya[0] - c2, yb[0] - c1])

        xa, xb = 0, dl
        xini = np.linspace(xa, xb, 11)
        # print(xini)
        yini = np.zeros((2, xini.size))
        res = scipy.integrate.solve_bvp(dydx, bound, xini, yini)
        xsol = np.linspace(xa, xb, 100)
        ysol = res.sol(xsol)
        # plt.plot(xsol, ysol[0])
        # plt.show()
        # plt.plot(xsol, ysol[1])
        # plt.show()
        return ysol[1][-1]

    def vapor(self, i, j):
        """
        calculate the heat flux determined by the vapor diffusion
        :param i: condensable gas
        :param j: non-condensable gas, list
        :return:
        """
        Tm = (self.T1 + self.T2) / 2
        p_c_out = PropsSI('P', 'T', self.T2, 'Q', 1, self.fluid[i])
        p_nc_in, k_nc = 0, 0
        for m in j:
            p_nc_in += self.p_rs[m]
            k_nc += self.p_rs[m] * PropsSI('L', 'T', Tm, 'P', self.p_rs[m], self.fluid[m])
        k_nc = k_nc / p_nc_in
        k_c_in = PropsSI('L', 'T', self.T1, 'P', self.p_rs[i], self.fluid[i])
        k_c_out = PropsSI('L', 'T', self.T2, 'Q', 1, self.fluid[i])

        xc_mol_in = self.p_rs[i] / (self.p_rs[i] + p_nc_in)
        xc_mol_out = p_c_out / (self.p_rs[i] + p_nc_in)
        k_v = (k_c_in * xc_mol_in + k_nc * (2 - xc_mol_in - xc_mol_out) + k_c_out * xc_mol_out) / 2
        k_e = k_v * vof + ks * (1 - vof)

        c_in = (self.p_rs[i] + p_nc_in) / 8.314 / self.T1
        c_c_in = PropsSI('DMOLAR', 'T', self.T1, 'P', self.p_rs[i], self.fluid[i])
        c_c_out = PropsSI('DMOLAR', 'T', self.T2, 'Q', 1, self.fluid[i])

        r = PropsSI('Hmass', 'T', self.T2, 'Q', 1, self.fluid[i]) - PropsSI('Hmass', 'T', self.T2, 'Q', 0,
                                                                            self.fluid[i])
        gap = 1e10
        for height in np.linspace(0.1, 50, 100):
            u_in = self.q_mass_rs[i] / np.pi / dm / height / vof / self.rho_rs[i]
            u_in = -1e-4* self.ode(self.T1,self.T2,c_in-c_c_in, c_in-c_c_out,thick)

            na_mass_temp = -1 * 0.1e-4 * self.ode(self.T1, self.T2, c_c_in, c_c_out, thick, u_in) * self.mass[i] \
                           - u_in * c_c_in * self.mass[i]  # kg/m2 s
            qcd_temp = na_mass_temp * r * vof
            qcv_temp = (self.T2 - self.T1) * k_e / thick
            qt_temp = qcd_temp + qcv_temp

            h_valid = -self.q_mass_rs[i] * r / qt_temp / np.pi / dm
            temp = abs(h_valid - height)
            if temp < gap:
                gap = temp
                qt, qcv, qcd, na_mass = qt_temp, qcv_temp, qcd_temp, na_mass_temp
                h_design = height

        return qt, qcd, qcv, na_mass, h_design, gap


ks = 0.2  # W/m K
vof = 0.8
do, dc, dm = 5, 3, 3.04  # m
thick = (dm - dc) / 2

Ts = np.arange(313 + 1, 383, 1)
n = Ts.shape
q2, q2_cd, q2_cv, n2_mass = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
fluids = ['water', 'methanol', 'CO2', 'hydrogen']
q_mass_in = 2.25
x_conversion = 0.5
tes = Test(523, 314, 6e6, fluids, q_mass_in, x_conversion)

print(tes.vapor(0, [2, 3]))
