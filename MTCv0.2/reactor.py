import json
import numpy as np
import scipy
from CoolProp.CoolProp import PropsSI
import pandas as pd
from matplotlib import pyplot as plt

R = 8.314  # J/mol/K


class Reactor:
    def __init__(self, kn_model='BU'):
        self.kn_model = kn_model
        if kn_model == 'GR':
            chem_path = 'in_chem_GR.json'
        elif kn_model == 'BU':
            chem_path = 'in_chem_BU.json'
        in_path = {'chem': chem_path, 'reactor': 'in_reactor.json', 'feed': 'in_feed.json'}
        in_data = dict()
        for key, values in in_path.items():
            with open(values) as f:
                in_data[key] = json.load(f)

        # reactor parameters
        self.L, self.Dt = in_data['reactor']["reactor"]['L'], in_data['reactor']["reactor"]['Dt']  # length, m
        self.nrt = in_data['reactor']["reactor"]['nt']  # number of the reaction tube
        self.phi = in_data['reactor']["reactor"]["phi"]  # void of fraction
        self.rhoc = in_data['reactor']["reactor"]["rhoc"]  # density of catalyst, kg/m3
        insulator_para = in_data['reactor']["insulator"]  # reaction occurring in the inside or outside of insulator
        self.nit = insulator_para["nt"]  # tube number of the insulator

        # feed gas parameter
        self.F0 = np.zeros(6)  # component of feed gas, mol/s; ndarray
        self.P0, self.T0 = in_data['feed']["condition"]["P"], in_data['feed']["condition"]["T"]  # P0 bar, T0 K
        self.v0 = in_data['feed']["condition"]["Sv"] / self.nrt  # volumetric flux per tube, m3/s

        self.Ft0 = self.P0 * 1e5 * self.v0 / R / self.T0  # total flux of feed,mol/s
        if in_data['feed']["condition"]["recycle"] == "off":  # fresh stream
            self.F0[0] = self.Ft0 / (in_data['feed']["condition"]["H2/CO2"] + 1)
            self.F0[1] = self.Ft0 - self.F0[0]
        elif in_data['feed']["condition"]["recycle"] == "on":  # recycled stream
            self.F0 = np.array([float(i) for i in in_data['feed']["feed"].split('\t')])

        # prescribed chem data of reaction
        self.chem_data = in_data['chem']
        self.comp_list = in_data['chem']["comp_list"]
        self.react_num = len(in_data['chem']["kr"])
        self.react_sto = np.empty((self.react_num, 5))
        self.react_dH = np.empty(self.react_num)
        for i in range(self.react_num):
            key = str(i + 1)
            self.react_sto[i] = in_data['chem']["stoichiometry"][key]
            self.react_dH[i] = in_data['chem']["heat_reaction"][key]

    @staticmethod
    def kad(T, in_dict):
        """
        calculate the equilibrium constant of adsorption
        :param T: operating temperature
        :param in_dict: prescribed chemical parameter
        :return: equilibrium constant of adsorption, 1/bar
        """
        adsorption_eq_constant = dict()
        for key, value in in_dict["kad"].items():
            adsorption_eq_constant[key] = value[0] * np.exp(value[1] / T / R)
        return adsorption_eq_constant

    @staticmethod
    def keq(T, in_dict):
        """
        calculate the equilibrium constant
        :param T: operating temperature
        :param in_dict: prescribed chemical parameter
        :return: equilibrium constant
        """
        react_eq_constant = dict()
        for key, value in in_dict["keq"].items():
            react_eq_constant[key] = 10 ** (value[0] / T + value[1])
        return react_eq_constant

    @staticmethod
    def kr(T, in_dict):
        """
        calculate the reaction rate constant
        :param T: operating temperature, K
        :param in_dict: prescribed chemical parameter
        :return: the reaction rate constant, mol kg−1 s−1 bar-1/2
        """
        react_rate_constant = dict()
        for key, value in in_dict["kr"].items():
            react_rate_constant[key] = value[0] * np.exp(value[1] / T / R)
        return react_rate_constant

    def rate_bu(self, T, Pi):
        """
        calculate the reaction rate
        :param T: operating temperature, K
        :param Pi: partial pressure of each component, bar
        :return: reaction rate of each component for each and all reaction; mol/s/kg_cat
        """
        # convert the partial pressure from ndarray to pd.Series
        Pi = pd.Series(Pi / 1e5, index=self.comp_list)
        # print(Pi)

        # calculate the reaction constant
        rate_const = self.kr(T, self.chem_data)
        ad_const = self.kad(T, self.chem_data)
        eq_const = self.keq(T, self.chem_data)
        # eq_const['3'] = eq_const['1'] / eq_const['2']

        # calculate the rate of each reaction
        react_rate = np.zeros(self.react_num)
        driving = rate_const['1'] * Pi['CO2'] * Pi['H2'] * (
                1 - Pi['H2O'] * Pi["Methanol"] / Pi["H2"] ** 3 / Pi['CO2'] / eq_const['1'])
        inhibiting = (1 + ad_const["H2O/H2"] * Pi['H2O'] / Pi['H2'] +
                      ad_const["H2"] * Pi["H2"] ** 0.5 + ad_const["H2O"] * Pi["H2O"])
        react_rate[0] = driving / inhibiting ** 3

        driving = rate_const['2'] * Pi['CO2'] * (1 - Pi['H2O'] * Pi["CO"] / Pi["H2"] / Pi['CO2'] / eq_const['2'])
        react_rate[1] = driving / inhibiting

        # compute the reaction rate for each component in every reaction
        react_comp_rate = self.react_sto * np.repeat(react_rate, 5).reshape(self.react_num, 5)
        react_comp_rate = np.vstack((react_comp_rate, np.sum(react_comp_rate, axis=0).T))
        react_comp_rate = np.hstack((react_comp_rate, np.array([0, 0, 0]).reshape(3, 1)))

        return react_comp_rate

    def rate_gr(self, T, Pi):
        """
        calculate the reaction rate
        :param T: operating temperature, K
        :param Pi: partial pressure of each component, bar
        :return: reaction rate of each component for each and all reaction; mol/s/kg_cat
        """

        # convert the partial pressure from ndarray to pd.Series
        Pi = pd.Series(Pi / 1e5, index=self.comp_list)

        # calculate the reaction constant
        rate_const = self.kr(T, self.chem_data)
        ad_const = self.kad(T, self.chem_data)
        eq_const = self.keq(T, self.chem_data)

        # eq_const['3'] = eq_const['1'] / eq_const['2']

        # calculate the rate of each reaction
        react_rate = np.zeros(self.react_num)
        driving = rate_const['1'] * ad_const['CO2'] * (
                Pi['CO2'] * Pi['H2'] ** 1.5 - Pi['H2O'] * Pi["Methanol"] / Pi["H2"] ** 1.5 / eq_const['1'])
        inhibiting = (1 + ad_const["CO"] * Pi['CO'] + ad_const["CO2"] * Pi['CO2']) * \
                     (Pi["H2"] ** 0.5 + ad_const["H2O/H2"] * Pi["H2O"])
        react_rate[0] = driving / inhibiting

        driving = rate_const['2'] * ad_const['CO2'] * (Pi['CO2'] * Pi["H2"] - Pi['H2O'] * Pi["CO"] / eq_const['2'])
        react_rate[1] = driving / inhibiting

        driving = rate_const['3'] * ad_const['CO'] * (
                Pi['CO'] * Pi["H2"] ** 1.5 - Pi['Methanol'] / Pi["H2"] ** 0.5 / eq_const['3'])
        react_rate[2] = driving / inhibiting

        # compute the reaction rate for each component in every reaction
        react_comp_rate = self.react_sto * np.repeat(react_rate, 5).reshape(self.react_num, 5)
        react_comp_rate = np.vstack((react_comp_rate, np.sum(react_comp_rate, axis=0).T))
        react_comp_rate = np.hstack((react_comp_rate, np.array([0, 0, 0, 0]).reshape(4, 1)))

        return react_comp_rate

    def balance(self, T, P, F_dict):
        """
        energy and material balance in the reactor
        :param T: operating temperature, K
        :param P: operating pressure, bar
        :param F_dict: molar flow rate of each component, mol/s; ndarray
        :return: temperature and molar flux variation of gas
        """
        Ft = F_dict.sum()  # total volumetric flow rate

        # calculate the partial pressure
        # calculate the correction to volumetric flow rate (m3/s)
        v = self.v0 * (self.P0 / P) * (T / self.T0) * (Ft / self.Ft0)
        Pi = F_dict * R * T / v  # Pa

        # calculate the change of the molar flow rate due to reactions, mol/s/kg_cat
        dF_react = self.rate_gr(T, Pi) if self.kn_model == 'GR' else self.rate_bu(T, Pi)

        # calculate the change of enthalpy due to reaction, kJ/(kg_cat s)
        dH = np.matmul(dF_react[:-1, 0], self.react_dH.T)

        # calculate the heat capacity of each component, cp*n, J/(s K)
        heat_capacity = 0
        for i in range(5):
            # read the heat capacity for each component, J/(mol K)
            cp = PropsSI('CPMOLAR', 'T', T, 'P', Pi[i], self.comp_list[i]) if Pi[i] > 0 else 0
            heat_capacity += cp * F_dict[i]
        dT = dH * 1e3 / heat_capacity  # K/kg_cat

        return dT, dF_react[-1]

    def simulator(self):
        """
        ode for the concentration distribution along the channel
        radial distribution
        the origin is located at the center of the circle
        :param inner_cond: temperature, molar fraction, and radius at inside;list
        :param outer_cond: temperature, molar fraction, and radius at outside; list
        :param P: pressure of mixture
        :param properties: heat capacity, diffusion coefficient, thermal conductivity of mixture; list
        :return: concentration and its slop
        """

        # model for ode solver
        P = self.P0

        def model(z, y):
            # y= [F_CO2, F_H2, F_CH3OH, F_H2O, F_CO, F_N2, T]
            F_in = np.array(y[:-1])
            temp = self.balance(y[-1], P, F_in)
            dl2dw = np.pi * self.Dt ** 2 / 4 * self.rhoc * self.phi
            dF_dz = temp[1] * dl2dw
            dT_dz = temp[0] * dl2dw
            return np.append(dF_dz, [dT_dz])

        z_span = [0, self.L]
        ic = np.append(self.F0, [self.T0])
        ode_method = 'RK45' if self.kn_model == 'GR' else 'BDF'
        res = scipy.integrate.solve_ivp(model, z_span, ic, method='BDF', t_eval=np.linspace(0, self.L, 100))
        t = res.t
        data = res.y
        for i in range(3):
            plt.plot(t, data[i + 2, :])

        plt.legend(['CH3OH', 'H2O', 'CO'])
        plt.show()
        plt.plot(t, data[-1, :])
        plt.show()
        r = (data[0, -1] - data[0, 0]) / data[0, 0]
        print(r)
        save_data = pd.DataFrame(data.T, columns=self.comp_list + ['T'])
        save_data.to_excel('result/result_test.xlsx')


reactor = Reactor(kn_model='BU')
reactor.simulator()

# cProfile.run("reactor.simulator(30)")
