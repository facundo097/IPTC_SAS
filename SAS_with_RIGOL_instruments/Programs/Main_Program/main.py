import Google_Sheets as gs
import PV_Model as PVM
import RIGOL_lib as RIGOL
import pyvisa
import time
import csv
from datetime import datetime
from Secrets import GAS_ID_DATA_BASE, GAS_ID_CONTROL_PANEL

channels = 2

def write_in_csv(PV, N_s, N_p, G, T_c, Ang_Deg, CV, V_out_calc, V_out_meas, I_out_calc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas, Err_V, Err_I, Err_P, Err_R, n, I_ph, I_o, R_s, R_sh, supply_mode, correction_time):
    # Get the current date and time
    current_date = datetime.now().strftime('%d/%m/%y') # '%DD/%MM/%YY'
    current_time = datetime.now().strftime('%H:%M:%S')

    # Create or open the CSV file
    with open('datalogs.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        # Check if the file is empty and write header if needed
        if file.tell() == 0:
            header = ["Date", "Time", "PV", "N_s", "N_p", "G", "T_c", "Ang_Deg", "CV", "V_calc", "V_meas",
                      "I_calc", "I_meas", "P_calc", "P_meas", "R_calc", "R_meas", "Err_V",
                      "Err_I", "Err_P", "Err_R", "n", "I_ph", "I_o", "R_s", "R_sh", "Mode", "Set Time"]
            writer.writerow(header)

        # Write the current date, time, and input parameters
        data_row = [current_date, current_time, PV, N_s, N_p, G, T_c, Ang_Deg, CV, V_out_calc, V_out_meas, I_out_calc,
                    I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas, Err_V, Err_I, Err_P, Err_R, n,
                    I_ph, I_o, R_s, R_sh, supply_mode, correction_time]
        writer.writerow(data_row)

def log_in_corrections_database(correc_cycle, total_time, loop_time, loop_type, loop_iter, V_out_calc, V_out_correc, V_out_meas, I_out_calc, I_out_correc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas, Err_V, Err_I, Err_P, Err_R, supply_mode):
    # Create a list of the variables to be logged
    data = [correc_cycle, total_time, loop_time, loop_type, loop_iter, V_out_calc, V_out_correc, V_out_meas, I_out_calc, I_out_correc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas, Err_V, Err_I, Err_P, Err_R, supply_mode]

    # Define the CSV file name
    filename = "corrections_database.csv"

    # Check if the file already exists, and create it with a header row if it doesn't
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            # Check if the file is empty
            if not any(row for row in reader):
                # File is empty, so write the header row
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    header = ["correc_cycle", "total_time", "loop_time", "loop_type", "loop_iter", "V_calc", "V_correc", "V_meas", "I_calc", "I_correc", "I_meas", "P_calc", "P_meas", "R_calc", "R_meas", "Err_V", "Err_I", "Err_P", "Err_R", "supply_mode"]
                    writer.writerow(header)
    except FileNotFoundError:
        # File doesn't exist, so create it with the header row
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            header = ["correc_cycle", "total_time", "loop_time", "loop_type", "loop_iter", "V_calc", "V_correc", "V_meas", "I_calc", "I_correc", "I_meas", "P_calc", "P_meas", "R_calc", "R_meas", "Err_V", "Err_I", "Err_P", "Err_R", "supply_mode"]
            writer.writerow(header)

    # Append the data to the CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def turn_on_equipment(channels):
    dc_load.turn_on_load()
    if channels == 2:
        dc_power.turn_on_channel(1)
        dc_power.turn_on_channel(2)
    elif channels == 1:
        dc_power.turn_on_channel(3)

def turn_off_equipment(channels, RES_range):
    dc_load.turn_off_load()
    if channels == 2:
        dc_power.turn_off_channel(1)
        dc_power.turn_off_channel(2)
        dc_power.set_voltage_current(1, 0, 0)
        dc_power.set_voltage_current(2, 0, 0)
    elif channels == 1:
        dc_power.turn_off_channel(3)
        dc_power.set_voltage_current(3, 0, 0)
    dc_load.set_function("RES")
    dc_load.set_resistance_range(RES_range)

def set_supply_outputs(V, I, channels):
    if channels == 2:
        dc_power.set_voltage_current(1, round(V , 3), round((I) / channels, 3))
        dc_power.set_voltage_current(2, round(V, 3), round((I) / channels, 3))
    elif channels == 1:
        dc_power.set_voltage_current(1, round(V, 3), round(I, 3))

def set_equipment_values(V_out_calc, I_out_calc, R_out_calc):
    global RES_range, values_set, channels, supply_ON
    if R_out_calc >= 15 and RES_range == "min":
        print("Switching load to 15 kΩ range...")
        RES_range = "max"
        turn_off_equipment(channels, RES_range)
        time.sleep(1)
        print(f"Setting resistance to {round(R_out_calc, 4)} Ω...")
        dc_load.set_resistance(round(R_out_calc, 4))
        set_supply_outputs(V_out_calc, I_out_calc, channels)
        turn_on_equipment(channels)
        values_set = 1

    if V_out_calc > 10 and RES_range == "min":
        print("Switching load to 15 kΩ range...")
        RES_range = "max"
        turn_off_equipment(channels, RES_range)
        time.sleep(1)
        print(f"Setting resistance to {round(R_out_calc, 4)} Ω...")
        dc_load.set_resistance(round(R_out_calc, 4))
        set_supply_outputs(V_out_calc, I_out_calc, channels)
        turn_on_equipment(channels)
        values_set = 1

    if R_out_calc < 15 and RES_range == "max" and V_out_calc < 10:
        print("Switching load to 15 Ω range...")
        RES_range = "min"
        turn_off_equipment(channels, RES_range)
        time.sleep(1)
        print(f"Setting resistance to {round(R_out_calc, 4)} Ω...")
        dc_load.set_resistance(round(R_out_calc, 4))
        set_supply_outputs(V_out_calc, I_out_calc, channels)
        turn_on_equipment(channels)
        values_set = 1

    if values_set == 0:
        dc_load.set_resistance(round(R_out_calc, 3))
        set_supply_outputs(V_out_calc, I_out_calc, channels)
        values_set = 1

    if supply_ON == 0:
        turn_on_equipment(channels)
        supply_ON = 1

def correct_outputs(V_out_calc, I_out_calc, P_out_calc, R_out_calc, V_out_meas, I_out_meas, P_out_meas, R_out_meas,
                    Err_V, Err_I, Err_P, Err_R, V_correc_factor, I_correc_factor, V_max_iter, I_max_iter):
    start_time = time.time()
    time.sleep(1.5)
    sleep_delay = 1.5
    global correc_cycle
    V_out_correc = V_out_calc
    I_out_correc = I_out_calc
    supply_mode = supply.query(":OUTP:CVCC? CH1").strip()
    log_in_corrections_database(correc_cycle, time.time() - start_time, "", "", "", V_out_calc, V_out_correc,
                                V_out_meas, I_out_calc, I_out_correc, I_out_meas, P_out_calc, P_out_meas, R_out_calc,
                                R_out_meas, Err_V, Err_I, Err_P, Err_R, str(supply_mode))
    if Err_V > 0.5 and Err_P > 1.5:
        print("Attempting to stabilize the outputs by increasing supply voltage...")
        loop_type = "V"
        loop_iter = 0
        V_initial_loop_time = time.time()
        while Err_V >= 0.5 and Err_P > 1.5 and loop_iter <= V_max_iter:##########################################################
            V_out_correc = V_out_calc * V_correc_factor
            #print(f"Voltage set to: {V_out_correc}")
            dc_power.set_voltage_current(1, round(V_out_correc, 3), round(I_out_calc / channels, 3))
            dc_power.set_voltage_current(2, round(V_out_correc, 3), round(I_out_calc / channels, 3))
            time.sleep(sleep_delay)
            V_out_meas, I_out_meas, R_out_meas = dc_load.measure_all()
            P_out_meas = V_out_meas * I_out_meas
            if V_out_calc > 0 and I_out_calc > 0 and P_out_calc > 0 and R_out_calc > 0:
                Err_V = 100 * abs(V_out_calc - V_out_meas) / V_out_calc
                Err_I = 100 * abs(I_out_calc - I_out_meas) / I_out_calc
                Err_R = 100 * abs(R_out_calc - R_out_meas) / R_out_calc
                Err_P = 100 * abs(P_out_calc - P_out_meas) / P_out_calc
            supply_mode = supply.query(":OUTP:CVCC? CH1").strip()
            #print(f"Meas. Voltage: {V_out_meas}")
            #print(f"Voltage error: {Err_V}")
            log_in_corrections_database(correc_cycle, time.time() - start_time, time.time() - V_initial_loop_time,
                                        loop_type, loop_iter, V_out_calc, V_out_correc, V_out_meas, I_out_calc,
                                        I_out_correc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas,
                                        Err_V, Err_I, Err_P, Err_R, str(supply_mode))
            V_correc_factor += 0.05
            loop_iter += 1

    loop_iter = 0
    if Err_P >= 0.5:
        print("Attempting to stabilize the outputs by increasing supply current...")
        loop_type = "I"
        I_out_correc = I_out_calc + I_correc_factor
        I_initial_loop_time = time.time()
        while Err_P >= 1 and loop_iter <= I_max_iter: #########################################################################
            #print(f"Current set from {I_out_calc} to: {I_out_correc}")
            dc_power.set_voltage_current(1, round(V_out_correc, 3), round(I_out_correc / channels, 3))
            dc_power.set_voltage_current(2, round(V_out_correc, 3), round(I_out_correc / channels, 3))
            time.sleep(sleep_delay)
            V_out_meas, I_out_meas, R_out_meas = dc_load.measure_all()
            P_out_meas = V_out_meas * I_out_meas
            if V_out_calc > 0 and I_out_calc > 0 and P_out_calc > 0 and R_out_calc > 0:
                Err_V = 100 * abs(V_out_calc - V_out_meas) / V_out_calc
                Err_I = 100 * abs(I_out_calc - I_out_meas) / I_out_calc
                Err_R = 100 * abs(R_out_calc - R_out_meas) / R_out_calc
                Err_P = 100 * abs(P_out_calc - P_out_meas) / P_out_calc
            supply_mode = supply.query(":OUTP:CVCC? CH1").strip()
            log_in_corrections_database(correc_cycle, time.time() - start_time, time.time() - I_initial_loop_time,
                                        loop_type, loop_iter, V_out_calc, V_out_correc, V_out_meas, I_out_calc,
                                        I_out_correc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas,
                                        Err_V, Err_I, Err_P, Err_R, str(supply_mode))
            if Err_V > 10:
                V_out_correc = V_out_calc
                dc_power.set_voltage_current(1, round(V_out_correc, 3), round(I_out_correc / channels, 3))
                dc_power.set_voltage_current(2, round(V_out_correc, 3), round(I_out_correc / channels, 3))
                time.sleep(sleep_delay)
            I_out_correc += I_correc_factor
            loop_iter += 1
    supply_mode = supply.query(":OUTP:CVCC? CH1").strip()
    log_in_corrections_database(correc_cycle, time.time() - start_time, "",
                                "", "", V_out_calc, V_out_correc, V_out_meas, I_out_calc,
                                I_out_correc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas,
                                Err_V, Err_I, Err_P, Err_R, str(supply_mode))
    if Err_P >= 200:
        print("THE POWER SUPPLY COULDN'T STABILIZE IN THE DESIRED VALUES, OUTPUTS SET TO ZERO!")
        dc_power.set_voltage_current(1, 0, 0)
        dc_power.set_voltage_current(2, 0, 0)
        dc_load.set_resistance(0.1)
        time.sleep(sleep_delay)
    V_out_meas, I_out_meas, R_out_meas = dc_load.measure_all()
    P_out_meas = V_out_meas * I_out_meas
    if V_out_calc > 0 and I_out_calc > 0 and P_out_calc > 0 and R_out_calc > 0:
        Err_V = 100 * abs(V_out_calc - V_out_meas) / V_out_calc
        Err_I = 100 * abs(I_out_calc - I_out_meas) / I_out_calc
        Err_R = 100 * abs(R_out_calc - R_out_meas) / R_out_calc
        Err_P = 100 * abs(P_out_calc - P_out_meas) / P_out_calc
    supply_mode = supply.query(":OUTP:CVCC? CH1").strip()
    correction_time = time.time() - start_time
    log_in_corrections_database(correc_cycle, time.time() - start_time, "",
                                "", "", V_out_calc, V_out_correc, V_out_meas, I_out_calc,
                                I_out_correc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas,
                                Err_V, Err_I, Err_P, Err_R, str(supply_mode))
    correc_cycle += 1
    return V_out_calc, I_out_calc, P_out_calc, R_out_calc, V_out_meas, I_out_meas, P_out_meas, R_out_meas, Err_V, Err_I, Err_P, Err_R, supply_mode, correction_time

def send_to_RIGOL(V_out_calc, I_out_calc):
    global Err_V, Err_I, Err_R, Err_P, supply_ON, channels, RES_range, values_set
    values_set = 0
    V_correc_factor = 1.05
    I_correc_factor = 0.01
    V_max_iter = 3
    I_max_iter = 3
    R_out_calc = (V_out_calc / I_out_calc)
    P_out_calc = V_out_calc * I_out_calc
    print("-----------------------------------------------------------------------------------------------------------")
    print(f"Calculated Values:        V = {V_out_calc:.3f} V     I = {I_out_calc:.3f} A     P = {P_out_calc:.3f} W     R = {R_out_calc:.3f} Ω")

    turn_off_equipment(channels, RES_range)
    time.sleep(1)
    turn_on_equipment(channels)
    time.sleep(1)
    set_equipment_values(V_out_calc, I_out_calc, R_out_calc)
    time.sleep(2)

    V_out_meas, I_out_meas, R_out_meas = dc_load.measure_all()
    P_out_meas = V_out_meas * I_out_meas

    if V_out_calc > 0 and I_out_calc > 0 and P_out_calc > 0 and R_out_calc > 0:
        Err_V = 100 * abs(V_out_calc - V_out_meas) / V_out_calc
        Err_I = 100 * abs(I_out_calc - I_out_meas) / I_out_calc
        Err_R = 100 * abs(R_out_calc - R_out_meas) / R_out_calc
        Err_P = 100 * abs(P_out_calc - P_out_meas) / P_out_calc

    print(f"Measured Values:          V = {V_out_meas:.3f} V     I = {I_out_meas:.3f} A     P = {P_out_meas:.3f} W     R = {R_out_meas:.3f} Ω")
    print(f"Measured Errors:          V = {Err_V:.2f} %      I = {Err_I:.2f} %      P = {Err_P:.2f} %      R = {Err_R:.2f} %")
    print("Attempting to reduce errors...")
    if Err_P > 0.5:
        V_out_calc, I_out_calc, P_out_calc, R_out_calc, V_out_meas, I_out_meas, P_out_meas, R_out_meas, Err_V, Err_I, Err_P, Err_R, supply_mode, correction_time = correct_outputs(V_out_calc, I_out_calc, P_out_calc, R_out_calc, V_out_meas, I_out_meas, P_out_meas, R_out_meas, Err_V, Err_I, Err_P, Err_R, V_correc_factor, I_correc_factor, V_max_iter, I_max_iter)
    print(f"Measured Values:          V = {V_out_meas:.3f} V     I = {I_out_meas:.3f} A     P = {P_out_meas:.3f} W     R = {R_out_meas:.3f} Ω")
    print(f"Measured Errors:          V = {Err_V:.2f} %      I = {Err_I:.2f} %      P = {Err_P:.2f} %      R = {Err_R:.2f} %")
    print("-----------------------------------------------------------------------------------------------------------")

    return P_out_calc, R_out_calc, V_out_meas, I_out_meas, P_out_meas, R_out_meas, supply_mode, correction_time

def main_loop(GAS_ID_DATA_BASE, GAS_ID_CONTROL_PANEL):
    global google_message, last_google_message
    global Start, PV, N_s, N_p, G, T_c, Ang_Deg, CV, CVV, last_PV
    global T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s_pv, K_v, K_i, E_g, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, I_ph, I_o, R_s, R_sh
    global V_out_calc, V_out_meas, I_out_calc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas, Err_V, Err_I, Err_P, Err_R
    global supply_ON, channels, correc_cycle
    while True:
        google_message = gs.read_google_sheets_message(GAS_ID_CONTROL_PANEL)
        print("Google Sheets message: ", google_message)
        if google_message != "0" and google_message != last_google_message and google_message[2] == "0": # If Stop = 0, turn off equipment
            last_google_message = google_message
            dc_power.turn_off_channel(1)
            dc_power.turn_off_channel(2)
            dc_load.turn_off_load()
            RES_range = "max"
            dc_load.set_resistance_range(RES_range)
            supply_ON = 0
            print("The equipment was turned off!")
        if google_message != "0" and google_message != last_google_message and google_message[2] == "1":  # Only calculate a new operational point when new conditions are set
            last_google_message = google_message
            input_params, panel_params = gs.extract_params(google_message)
            Start, PV, N_s, N_p, G, T_c, Ang_Deg, CV, CVV = gs.parse_input_params(input_params)
            if PV != last_PV:
                last_PV = PV
                T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s_pv, K_v, K_i, E_g, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref = gs.parse_panel_params(panel_params)
            if N_s != 1 or N_p != 1:
                if CV == 0:
                    CVV = CVV / N_s
                else:
                    CVV = CVV / N_p
            n, I_ph, I_o, R_s, R_sh, V_out_calc, I_out_calc, P_out_calc, V_out_meas, I_out_meas, P_out_meas = PVM.Analytical_Model(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, CV, CVV, N_s, N_p, N_s_pv)
            P_out_calc, R_out_calc, V_out_meas, I_out_meas, P_out_meas, R_out_meas, supply_mode, correction_time = send_to_RIGOL(V_out_calc, I_out_calc)
            gs.send_to_google_sheets_long(GAS_ID_DATA_BASE, PV, N_s, N_p, G, T_c, Ang_Deg, CV, V_out_calc, V_out_meas,I_out_calc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas, Err_V, Err_I, Err_P, Err_R, n, I_ph, I_o, R_s, R_sh,supply_mode,correction_time)
            write_in_csv(PV, N_s, N_p, G, T_c, Ang_Deg, CV, V_out_calc, V_out_meas, I_out_calc, I_out_meas, P_out_calc, P_out_meas, R_out_calc, R_out_meas, Err_V, Err_I, Err_P, Err_R, n, I_ph, I_o, R_s, R_sh,supply_mode,correction_time)

        elif google_message == "0" or google_message[2] == "1":
            if supply_ON == 1:
                V_out_meas, I_out_meas, R_out_meas = dc_load.measure_all()
                P_out_meas = V_out_meas * I_out_meas
                Err_V = 100 * abs(V_out_calc - V_out_meas) / V_out_calc
                Err_I = 100 * abs(I_out_calc - I_out_meas) / I_out_calc
                Err_R = 100 * abs(R_out_calc - R_out_meas) / R_out_calc
                Err_P = 100 * abs(P_out_calc - P_out_meas) / P_out_calc
                print("-----------------------------------------------------------------------------------------------------------")
                print(f"Calculated Values:        V = {V_out_calc:.3f} V     I = {I_out_calc:.3f} A     P = {P_out_calc:.3f} W     R = {R_out_calc:.3f} Ω")
                print(f"Measured Values:          V = {V_out_meas:.3f} V     I = {I_out_meas:.3f} A     P = {P_out_meas:.3f} W     R = {R_out_meas:.3f} Ω")
                print(f"Measured Errors:          V = {Err_V:.2f} %      I = {Err_I:.2f} %      P = {Err_P:.2f} %      R = {Err_R:.2f} %")
                print("-----------------------------------------------------------------------------------------------------------")
                gs.send_to_google_sheets_long(GAS_ID_DATA_BASE,PV,N_s,N_p,G,T_c,Ang_Deg,CV,V_out_calc,V_out_meas,I_out_calc,I_out_meas,P_out_calc,P_out_meas,R_out_calc,R_out_meas,Err_V,Err_I,Err_P,Err_R,n,I_ph,I_o,R_s,R_sh,supply_mode,correction_time)
                write_in_csv(PV,N_s,N_p,G,T_c,Ang_Deg,CV,V_out_calc,V_out_meas,I_out_calc,I_out_meas,P_out_calc,P_out_meas,R_out_calc,R_out_meas,Err_V,Err_I,Err_P,Err_R,n,I_ph,I_o,R_s,R_sh,supply_mode,correction_time)

google_message = ""
last_google_message = ""

# Inputs
Start = 0           # 1 = Start, 0 = Stop
PV = 0              # Solar panel
N_s = 0             # Number of rows in the solar array (Ns)
N_p = 0             # Number of columns in the solar array (Np)
G = 0               # Irradiance
T_c = 0             # Temperature of the cell
Ang_Deg = 0         # Incidence angle
CV = 0              # Control variable
CVV = 0             # Control variable value
last_PV = 0

# Solar panel parameters
T_c_ref = 0         # Cell temperature at ref. conditions
G_ref = 0           # Solar irradiance at ref. conditions
V_oc = 0            # Open Circuit Voltage
I_sc = 0            # Short Circuit Current
V_mp = 0            # MPP Voltage
I_mp = 0            # MPP Current
P_mp = 0            # MPP Power
N_s_pv = 0          # Number of cells in series (in a single solar panel)
K_v = 0             # Voc temperature coefficient
K_i = 0             # Isc temperature coefficient
E_g = 0             # Band gap
n = 0               # Diode ideality factor
I_ph_ref = 0        # Photoelectric current at reference conditions
I_o_ref = 0         # Diode inverse saturation current at reference conditions
R_s_ref = 0         # Series resistance at reference conditions
R_sh_ref = 0        # Shunt resistance at reference conditions
I_ph = 0            # Photoelectric current
I_o = 0             # Diode inverse saturation current
R_s = 0             # Series resistance
R_sh = 0            # Shunt resistance

# Outputs
V_out_calc = 0      # Voltage output calculated
V_out_meas = 0      # Voltage output sensed (sent by MCU_S1)
I_out_calc = 0      # Current output calculated
I_out_meas = 0      # Current output sensed (sent by MCU_S1)
P_out_calc = 0      # Power output calculated (V_out_calc * I_out_calc)
P_out_meas = 0      # Power output sensed (V_out_meas * I_out_meas)
R_out_calc = 0
R_out_meas = 0

Err_V = 0
Err_I = 0
Err_P = 0
Err_R = 0

supply_ON = 0
correc_cycle = 0
RES_range = "max"

rm = pyvisa.ResourceManager()
supply = rm.open_resource(rm.list_resources()[1])
load = rm.open_resource(rm.list_resources()[0])
dc_power = RIGOL.power_supply(supply, "DC Power Supply")
dc_load = RIGOL.load(load, "DC Electronic Load")
turn_off_equipment(channels, RES_range)

main_loop(GAS_ID_DATA_BASE, GAS_ID_CONTROL_PANEL)
