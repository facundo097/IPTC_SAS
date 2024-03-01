import PV_Model as PVM
import csv
import random
import time


# Inputs sent by the MCU_S2
N_s = 2  # Number of rows in the solar array (Ns) || I03
N_p = 3  # Number of columns in the solar array (Np)|| I04
G = 0  # Irradiance || I05
T_c = 0  # Temperature of the cell || I06
Ang_Deg = 0  # Incidence angle || I07
CV = 0  # Control variable || I08
CVV = 0  # Control variable value || I09

# Outputs that will be stored in both the local and cloud databases
V_out_calc = 0  # Voltage output calculated
I_out_calc = 0  # Current output calculated

# Solar panel parameters at reference conditions sent by the MCU_S2
T_c_ref = 28  # Cell temperature at ref. conditions
G_ref = 1367  # Solar irradiance at ref. conditions
V_oc = 2.699  # Open Circuit Voltage
I_sc = 0.496  # Short Circuit Current
V_mp = 2.387  # MPP Voltage
I_mp = 0.487  # MPP Current
P_mp = 1.162  # MPP Power
N_s_pv = 2  # Number of cells in series (in a single solar panel)
K_v = -6.20E-03  # Voc temperature coefficient
K_i = 3.60E-04  # Isc temperature coefficient
E_g = 1.6  # Band gap
n = 1.23  # Diode ideality factor
I_ph = 0  # Photoelectric current
I_o = 0  # Diode inverse saturation current
R_s = 0  # Series resistance
R_sh = 0  # Shunt resistance
I_ph_ref = 0.496  # Photoelectric current
I_o_ref = 9.44E-38  # Diode inverse saturation current
R_s_ref = 0.3555  # Series resistance
R_sh_ref = 996.98  # Shunt resistance

def write_csv(exec_time, V_out_calc, I_out_calc, G, T_c, Ang_Deg):
    header = ["t", "V", "I", "G", "T", "Ang"]
    data = [exec_time, V_out_calc, I_out_calc, G, T_c, Ang_Deg]

    with open('TimeTest.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if file is empty
            writer.writerow(header)
        writer.writerow(data)

while True:
    while True:
        CVV = 2.0 + random.random() * 3.0  # Generates a random float between 2 and 5
        G = random.randint(200, 1375)  # Generates a random integer between 200 and 1375
        T_c = random.randint(-80, 80)  # Generates a random integer between -80 and 80
        Ang_Deg = random.randint(0, 85)  # Generates a random integer between 0 and 85
        start_time = time.perf_counter()  # start timer
        if N_s != 1 or N_p != 1:
            if CV == 0:
                CVV = CVV / N_s
            else:
                CVV = CVV / N_p
        n, I_ph, I_o, R_s, R_sh, V_out_calc, I_out_calc, P_out_calc, V_out_meas, I_out_meas, P_out_meas = PVM.Analytical_Model(
            G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, CV,
            CVV, N_s,
            N_p, N_s_pv)
        exec_time = time.perf_counter() - start_time  # calculate execution time
        print(f"{exec_time}, {V_out_calc}, {I_out_calc}, {G}, {T_c}, {Ang_Deg}")
        write_csv(exec_time, V_out_calc, I_out_calc, G, T_c, Ang_Deg)
        time.sleep(5)

