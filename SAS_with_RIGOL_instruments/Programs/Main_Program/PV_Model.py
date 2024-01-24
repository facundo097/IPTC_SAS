import math
import numpy as np
from scipy.optimize import root
from scipy.optimize import fsolve
import csv
import os

def find_V_and_I_given_R(V_oc, R, n, I_o_ref, I_ph_ref, R_s_ref, R_sh_ref, N_s_pv, T_c_ref):
    Rel_Error = 100
    V = 0.1
    I = 0
    R_calc = 0.001
    while Rel_Error > 4 and V < V_oc:
        I = Solve_for_Current(V, n, I_o_ref, I_ph_ref, R_s_ref, R_sh_ref, N_s_pv, T_c_ref)
        R_calc = V / I
        Rel_Error = 100 * abs(R - R_calc)/R
        #print("V: {:.2f} V    I: {:.2f} A    R_calc: {:.2f} Ω    Error: {:.2f} %".format(V, I, R_calc, Rel_Error))
        V += 0.001
    return V, I

def get_arrays_I_P_R_given_V(V_ref,n,I_o_ref,I_ph_ref,R_s_ref,R_sh_ref,N_s_pv,T_c_ref):
    I_o = I_o_ref
    I_ph = I_ph_ref
    R_s = R_s_ref
    R_sh = R_sh_ref
    N_s = N_s_pv
    len_dataset = len(V_ref)
    I_calc = []
    P_calc = []
    R_calc = []
    consecutive_negative_count = 0

    for i in range(len_dataset):
        V_i = V_ref[i]
        I_i = Solve_for_Current(V_i, n, I_o, I_ph, R_s, R_sh, N_s, T_c_ref)

        if I_i < 0:
            consecutive_negative_count += 1
        else:
            consecutive_negative_count = 0

        if consecutive_negative_count > 10:
            I_calc.extend([-1] * (len_dataset - i))
            P_calc.extend([-1] * (len_dataset - i))
            break

        P_i = V_i * I_i
        R_i = V_i / I_i
        I_calc.append(I_i)
        P_calc.append(P_i)
        R_calc.append(R_i)

    return I_calc, P_calc, R_calc


def Scale_Parameters(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g):
    T_c += 273.15
    T_c_ref += 273.15
    k = 1.38064852E-23  # Boltzmann's constant
    q = 1.60217662E-19  # Elementary charge
    delta_T = T_c - T_c_ref
    Ang_Rad = math.radians(Ang_Deg)
    G_new = G * math.cos(Ang_Rad)
    alpha_G = G_new / G_ref
    R_s = R_s_ref / alpha_G
    R_sh = R_sh_ref / alpha_G
    I_ph = alpha_G * (I_ph_ref + K_i * delta_T)
    I_o = I_o_ref * (T_c / T_c_ref) ** 3 * math.exp((E_g * q) / (n * k) * (1 / T_c_ref - 1 / T_c))
    #print(f"n: {n}, I_ph: {I_ph}, I_o: {I_o}, R_s: {R_s}, R_sh: {R_sh}")
    return n, I_ph, I_o, R_s, R_sh

def Solve_for_Current(V, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref):
    T_c_ref += 273.15
    k = 1.38064852E-23  # Boltzmann's constant
    q = 1.60217662E-19  # Elementary charge
    def eq(I, V, I_o, I_ph, R_s, R_sh, V_T):
        exponent = (V + I * R_s) / V_T
        clipped_exponent = np.clip(exponent, -700, 700)  # Clip exponent to avoid overflow
        return I_ph - I_o * (np.exp(clipped_exponent) - 1) - ((V + I * R_s) / R_sh) - I
    V_T = (N_s_pv * n * k * T_c_ref) / q
    result = root(eq, 0, args=(V, I_o, I_ph, R_s, R_sh, V_T))
    I = result.x[0]
    return I

def Solve_for_Voltage(I, n, I_o, I_ph, R_s, R_sh, N, T_c_ref):
    def eq(V, I, n, I_o, I_ph, R_s, R_sh, N):
        k = 1.38064852E-23
        q = 1.60217662E-19
        V_T = (N * n * k * T_c_ref) / q
        return V_T * np.log((I_ph + I_o - I * (1 + R_s / R_sh) - V / R_sh) / I_o) - I * R_s - V
    voltage = fsolve(eq, 0, args=(I, n, I_o, I_ph, R_s, R_sh, N))
    return voltage[0]


def Analytical_Model(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, CV, CVV, N_s, N_p, N_s_pv):
    n, I_ph, I_o, R_s, R_sh = Scale_Parameters(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g)
    print(f"Scaled parameters: n: {n}, I_ph: {I_ph}, I_o: {I_o}, R_s: {R_s}, R_sh: {R_sh}")
    if CV == 1:
        print("Current provided, finding voltage...")
        V_out_calc = Solve_for_Voltage(CVV, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref)
        V_out_calc = V_out_calc * N_s
        I_out_calc = CVV * N_p
    else:
        print("Voltage provided, finding current...")
        I_out_calc = Solve_for_Current(CVV, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref)
        I_out_calc = I_out_calc * N_p
        V_out_calc = CVV * N_s
    P_out_calc = V_out_calc * I_out_calc
    R_out_calc = V_out_calc / I_out_calc
    V_out_meas = V_out_calc
    I_out_meas = I_out_calc
    P_out_meas = P_out_calc
    print(f"Ouputs: V_out_calc: {round(V_out_calc,3)}, I_out_calc: {round(I_out_calc,3)}, P_out_calc: {round(P_out_calc,3)}, R_out_calc: {round(R_out_calc,3)}")

    return n, I_ph, I_o, R_s, R_sh, V_out_calc, I_out_calc, P_out_calc, V_out_meas, I_out_meas, P_out_meas

def calculate_curve_arrays(V_start, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref, N_s, N_p):
    V_arr = []
    I_arr = []
    P_arr = []
    R_arr = []
    V_calc = V_start / N_s
    I_calc = 0
    while I_calc >= 0:
        I_calc = Solve_for_Current(V_calc, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref)
        #print(f"V = {V_calc}     I = {I_calc}")
        V_arr.append(V_calc * N_s)
        I_arr.append(I_calc * N_p)
        P_arr.append(V_arr[-1] * I_arr[-1])  # Calculate power using the last elements
        R_arr.append(V_arr[-1] / I_arr[-1])
        V_calc += 0.01
    V_arr = V_arr[:-1]
    I_arr = I_arr[:-1]
    P_arr = P_arr[:-1]
    R_arr = R_arr[:-1]
    return V_arr, I_arr, P_arr, R_arr


def find_MPP(V_arr, I_arr, P_arr):
    MPP_index = np.argmax(P_arr)
    P_mp = P_arr[MPP_index]
    V_mp = V_arr[MPP_index]
    I_mp = I_arr[MPP_index]
    R_mp = V_mp / I_mp
    return V_mp, I_mp, P_mp, R_mp, MPP_index


def write_MPP_in_csv(file_name, variable, variable_value, V_mp, I_mp, P_mp, R_mp):
    # Check if the file already exists
    file_exists = os.path.isfile(file_name)

    with open(file_name, 'a', newline='') as csvfile:
        fieldnames = [variable, 'V_mp', 'I_mp', 'P_mp', 'R_mp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file doesn't exist, write the header row
        if not file_exists:
            writer.writeheader()

        # Round float values to 4 decimal places
        V_mp = round(V_mp, 4) if isinstance(V_mp, float) else V_mp
        I_mp = round(I_mp, 4) if isinstance(I_mp, float) else I_mp
        P_mp = round(P_mp, 4) if isinstance(P_mp, float) else P_mp
        R_mp = round(R_mp, 4) if isinstance(R_mp, float) else R_mp

        # Write the data to the CSV file
        writer.writerow({variable: variable_value, 'V_mp': V_mp, 'I_mp': I_mp, 'P_mp': P_mp, 'R_mp': R_mp})


def write_array_dataset_in_csv(file_name, V_arr, I_arr, P_arr, R_arr):
    # Create a list of rows to write to the CSV file
    rows = zip(V_arr, I_arr, P_arr, R_arr)

    # Open the CSV file in write mode
    with open(file_name, 'w', newline='') as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        # Write the header row
        csv_writer.writerow(["Voltage", "Current", "Power", "Resistance"])

        # Write the data rows with float values rounded to 4 decimal places
        for row in rows:
            rounded_row = [round(val, 4) if isinstance(val, float) else val for val in row]
            csv_writer.writerow(rounded_row)


def find_nearest_index(arr, value):
    nearest_index = 0
    nearest_difference = abs(arr[0] - value)

    for i in range(1, len(arr)):
        difference = abs(arr[i] - value)
        if difference < nearest_difference:
            nearest_difference = difference
            nearest_index = i

    return nearest_index


def reduce_points_in_curve(V_arr, I_arr, P_arr, R_arr, MPP_index):
    V_mp = V_arr[MPP_index]
    V_target = V_mp - V_mp * 0.1
    #print("V_target: ", V_target)
    V_target_index = find_nearest_index(V_arr, V_target)
    #print("V_closest_target: ", V_arr[V_target_index])

    # Calculate the increment value
    increment = (V_target_index - 10) // 9

    # Create new arrays with reduced points
    reduced_V_arr = [V_arr[0]] + [V_arr[increment * i] for i in range(1, 11)] + V_arr[increment * 10 + 1:]
    reduced_I_arr = [I_arr[0]] + [I_arr[increment * i] for i in range(1, 11)] + I_arr[increment * 10 + 1:]
    reduced_P_arr = [P_arr[0]] + [P_arr[increment * i] for i in range(1, 11)] + P_arr[increment * 10 + 1:]
    reduced_R_arr = [R_arr[0]] + [R_arr[increment * i] for i in range(1, 11)] + R_arr[increment * 10 + 1:]

    return reduced_V_arr, reduced_I_arr, reduced_P_arr, reduced_R_arr

