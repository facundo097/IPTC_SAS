import math
import numpy as np
from scipy.optimize import root
from scipy.optimize import fsolve
import time
import PV_CSV
import os


# Functions to calculate current and voltage using the Single-Diode equations.
def Solve_for_Current(V, n, I_o, I_ph, R_s, R_sh, N, T_c_ref):
    def eq(I, V, I_o, I_ph, R_s, R_sh, V_T):
        exponent = (V + I * R_s) / V_T
        clipped_exponent = np.clip(exponent, -700, 700)  # Clip exponent to avoid overflow
        return I_ph - I_o * (np.exp(clipped_exponent) - 1) - ((V + I * R_s) / R_sh) - I
    k = 1.38064852E-23
    q = 1.60217662E-19
    V_T = (N * n * k * T_c_ref) / q
    result = root(eq, 0, args=(V, I_o, I_ph, R_s, R_sh, V_T))
    I = result.x[0]
    return I


def Solve_for_Voltage(I, n, I_o, I_ph, R_s, R_sh, N, T_c_ref):
    def eq(V, I, n, I_o, I_ph, R_s, R_sh, N):
        k = 1.38064852E-23
        q = 1.60217662E-19
        V_T = (N * n * k * T_c_ref) / q
        return V_T * np.log((I_ph + I_o - I * (1 + R_s / R_sh) - V / R_sh) / I_o) - I * R_s - V
    initial_guess = 0.0  # Provide an initial guess for the voltage value
    voltage = fsolve(eq, initial_guess, args=(I, n, I_o, I_ph, R_s, R_sh, N))
    return voltage[0]


# The following functions are used to calculate the unknown parameters in the Single-Diode model
# Based on the paper from A. Hussein, "A simple approach to extract the unknown parameters of PV modules", 2017
def f(V_oc, I_sc, V_mp, I_mp, V_T, A, B, C): # Equation 17
    return V_mp * (C + 1) * (I_sc * V_oc - I_sc * V_mp - I_mp * V_oc) - I_sc * V_mp * V_T * (A - C) + I_mp * V_oc * V_T * (B - C) + 2 * I_mp * V_mp * V_T * (A - B)


def dfdR(V_oc, I_sc, V_mp, I_mp, V_T, B, C): # Equation 19
    return ((V_oc * V_mp * (C + 1)) / V_T) * (I_sc - I_mp) + I_sc * (B + 1) * (V_oc - 2 * V_mp) + (C + 1) * (I_sc * V_mp - I_mp * V_oc - (I_sc * (V_mp ** 2)) / V_T)


def Calc_MAPE_RMSE_nRMSE_R2(I_array_ref, I_array_calc):
    Sum_I_ref = 0
    Sum_ARPE = 0
    SS_res = 0 # AKA sum of squared errors or Sum_SE
    SS_tot = 0
    index = 0
    while index <= len(I_array_ref)-2:
        Sum_I_ref += I_array_ref[index]
        SS_res += (I_array_calc[index] - I_array_ref[index]) ** 2
        Sum_ARPE += 100 * abs(I_array_ref[index] - I_array_calc[index]) / I_array_ref[index]
        index += 1
    Mean_I_ref = Sum_I_ref / len(I_array_ref)
    index = 0
    while index <= len(I_array_ref)-2:
        SS_tot += (I_array_ref[index] - Mean_I_ref) ** 2
        index += 1

    MAPE = Sum_ARPE / len(I_array_ref)
    RMSE = math.sqrt(SS_res / len(I_array_ref))
    nRMSE = RMSE / (max(I_array_ref) - min(I_array_ref))
    R2 = 1 - SS_res / SS_tot
    return MAPE, RMSE, nRMSE, R2


def hussein2017(V_oc, I_sc, V_mp, I_mp, N_s, R_s, n_step, V_array_ref, I_array_ref, tolerance, T_c_ref, panel_manuf, panel_model, folder_path):
    start_time = time.time()
    file_name = f"{panel_manuf}_{panel_model}_Hussein_Parameters_Iterations.csv"
    file_path = os.path.join(folder_path, file_name)
    k = 1.38064852e-23  # boltzmann constant
    q = 1.60217662e-19  # electron charge
    n = 1
    V_T = (n * N_s * k * T_c_ref) / q
    A = (math.exp(V_oc / V_T) - 1)
    B = (math.exp(I_sc * R_s / V_T) - 1)
    C = (math.exp((V_mp + I_mp * R_s) / V_T) - 1)

    # Variables to calculate RMSE for a given iteration
    I_array_calc = []
    iteration_data = []
    i = 0
    i_max = len(V_array_ref) - 1
    iter = 0

    while (n <= 2):
        V_T = (n * N_s * k * T_c_ref) / q
        x = f(V_oc, I_sc, V_mp, I_mp, V_T, A, B, C)
        y = dfdR(V_oc, I_sc, V_mp, I_mp, V_T, B, C)

        while (abs(x/y)) > tolerance:
            A = (math.exp(V_oc / V_T) - 1)
            B = (math.exp(I_sc * R_s / V_T) - 1)
            C = (math.exp((V_mp + I_mp * R_s) / V_T) - 1)
            x = f(V_oc, I_sc, V_mp, I_mp, V_T, A, B, C)
            y = dfdR(V_oc, I_sc, V_mp, I_mp, V_T, B, C)
            R_s = R_s - x / y  # Equation 18

        R_sh = (V_oc * (C - B) - V_mp * (A - B)) / (I_mp * (A - B) - I_sc * (A - C)) - R_s  # Equation 14
        I_ph = (I_sc * (1 + R_s / R_sh) * A - V_oc / R_sh) / (A - B)                        # Equation 12
        I_o = (I_ph / A) - (V_oc / (A * R_sh))                                              # Equation 5
        while i <= i_max:
            V = V_array_ref[i]
            I_calc = Solve_for_Current(V, n, I_o, I_ph, R_s, R_sh, N_s, T_c_ref)
            I_array_calc.append(I_calc)
            i += 1
        i = 0
        MAPE, RMSE, nRMSE, R2 = Calc_MAPE_RMSE_nRMSE_R2(I_array_ref, I_array_calc)
        I_array_calc.clear()
        Iter_info = {'i': iter, 'n': n, 'I_o': I_o, 'I_ph': I_ph, 'R_s': R_s, 'R_sh': R_sh,'RMSE': RMSE, 'nRMSE': nRMSE, 'R2': R2, 'MAPE': MAPE}
        iteration_data.append(Iter_info)
        PV_CSV.log_iteration_data_in_CSV(Iter_info, file_path)
        iter += 1
        n += n_step

    min_RMSE_iteration = min(iteration_data, key=lambda x: x['RMSE'])
    best_n = min_RMSE_iteration['n']
    best_I_o = min_RMSE_iteration['I_o']
    best_I_ph = min_RMSE_iteration['I_ph']
    best_R_s = min_RMSE_iteration['R_s']
    best_R_sh = min_RMSE_iteration['R_sh']
    best_RMSE = min_RMSE_iteration['RMSE']
    best_nRMSE = min_RMSE_iteration['nRMSE']
    best_MAPE = min_RMSE_iteration['MAPE']
    best_R2 = min_RMSE_iteration['R2']
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"'hussein2017' Execution time: {elapsed_time:.6f} seconds")
    return best_n, best_I_o, best_I_ph, best_R_s, best_R_sh, best_RMSE, best_nRMSE, best_R2, best_MAPE


# This function scale the firve paramters to other conditions of irradiance, temperature and incidence angle
# Equations taken from various sources
def Scale_Parameters(G, T_c, incidence_angle_deg, G_ref, T_c_ref, V_oc, I_sc, TK_V_oc, TK_I_sc, n, I_ph, I_o, R_s, R_sh, E_g):
    start_time = time.time()
    k = 1.38064852e-23  # boltzmann constant
    q = 1.60217662e-19  # electron charge
    #I_sc = I_sc * alpha_G + TK_I_sc * delta_T
    #V_oc = V_oc + n * T_c * np.log(alpha_G) + TK_V_oc * delta_T
    incidence_angle_rad = np.deg2rad(incidence_angle_deg)
    G = G * np.cos(incidence_angle_rad) # LK03
    delta_T = (T_c - T_c_ref)
    alpha_G = G / G_ref
    R_s = R_s / alpha_G # PV09
    R_sh = R_sh / alpha_G # PV04, PV09
    I_ph = alpha_G * (I_ph + TK_I_sc * delta_T) # PV04, PV03
    I_o = I_o * ((T_c / T_c_ref) ** 3) * np.exp((E_g * q) / (n * k) * (1 / T_c_ref - 1 / T_c)) # PV11
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"'Scale_Parameters' Execution time: {elapsed_time:.10f} seconds")

    return n, I_ph, I_o, R_s, R_sh




