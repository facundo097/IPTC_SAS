import csv
import os
import PV_functions
import PV_Plotting
import time

def Export_Datasets_CSV(panel_manuf, panel_model, V_ref, I_ref, P_ref, I_calc, P_calc, folder):
    file_name = panel_manuf + "_" + panel_model + "_Datasets.csv"
    file_path = os.path.join(folder, file_name)
    max_length = max(len(V_ref), len(I_ref), len(P_ref), len(I_calc), len(P_calc))
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["V_ref", "I_ref", "P_ref", "I_calc", "P_calc"])  # Writing header

        for i in range(max_length):
            row = [
                V_ref[i] if i < len(V_ref) else '',
                I_ref[i] if i < len(I_ref) else '',
                P_ref[i] if i < len(P_ref) else '',
                I_calc[i] if i < len(I_calc) else '',
                P_calc[i] if i < len(P_calc) else ''
            ]
            csv_writer.writerow(row)


def Import_Dataset_from_CSV(file_path):
    V_ref = []
    I_ref = []
    P_ref = []
    I_calc = []
    P_calc = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            V_ref.append(float(row['V_ref']))
            I_ref.append(float(row['I_ref']))
            P_ref.append(float(row['P_ref']))
            I_calc.append(float(row['I_calc']))
            P_calc.append(float(row['P_calc']))

    V_oc = max(V_ref)
    I_sc = max(I_ref)
    P_mp = max(P_ref)
    P_mp_index = P_ref.index(P_mp)
    V_mp = V_ref[P_mp_index]
    I_mp = I_ref[P_mp_index]
    return V_ref, I_ref, P_ref, I_calc, P_calc, V_oc, I_sc, V_mp, I_mp, P_mp


def Export_Datasheet_CSV(panel_manuf, panel_model, panel_type, panel_eff, T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s, TK_V_oc, TK_I_sc, E_g, n, I_o, I_ph, R_s, R_sh, RMSE, nRMSE, R2, MAPE, folder):
    start_time = time.time()
    file_name = f"{panel_manuf}_{panel_model}_Datasheet.csv"
    file_path = os.path.join(folder, file_name)
    col1 = ["Parameter",
            panel_manuf,
            panel_model,
            panel_type,
            panel_eff,
            T_c_ref,
            G_ref,
            V_oc,
            I_sc,
            V_mp,
            I_mp,
            P_mp,
            N_s,
            TK_V_oc,
            TK_I_sc,
            E_g,
            n,
            I_ph,
            I_o,
            R_s,
            R_sh,
            RMSE,
            nRMSE,
            R2,
            MAPE]

    col2 = ["Unit",
            "",
            "",
            "",
            "%",
            "K",
            "W/m²",
            "V",
            "A",
            "V",
            "A",
            "W",
            "",
            "V/K",
            "A/K",
            "eV",
            " ",
            "A",
            "A",
            "Ω",
            "Ω",
            " ",
            " ",
            " ",
            "%"]

    col3 = ["Symbol",
            "",
            "",
            "",
            "η",
            "T_c_ref",
            "G_ref",
            "V_oc",
            "I_sc",
            "V_mp",
            "I_mp",
            "P_mp",
            "N_s",
            "TK_V_oc",
            "TK_I_sc",
            "E_g",
            "n",
            "I_ph",
            "I_o",
            "R_s",
            "R_sh",
            "RMSE",
            "nRMSE",
            "R2",
            "MAPE"]

    col4 = ["Description",
            "Panel manufacturer",
            "Panel model",
            "Panel type",
            "Panel efficiency",
            "Cell temperature at reference conditions",
            "Solar irradiance at reference conditions",
            "Open Circuit Voltage",
            "Short Circuit Current",
            "MPP Voltage",
            "MPP Current",
            "MPP Power",
            "Number of cells in series",
            "V_oc temperature coefficient",
            "I_sc temperature coefficient",
            "Band gap",
            "Diode ideality factor",
            "Photoelectric current",
            "Diode inverse saturation current",
            "Series resistance",
            "Shunt resistance",
            "Root-Mean-Squared-Error of n, I_ph, I_o, R_s, R_sh",
            "Normalized Root-Mean-Squared-Error of n, I_ph, I_o, R_s, R_sh",
            "Coefficient of Determination of n, I_ph, I_o, R_s, R_sh",
            "Mean Absolute Percentage Error of n, I_ph, I_o, R_s, R_sh"]

    max_length = max(len(col1), len(col2), len(col3), len(col4))

    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)

        for i in range(max_length):
            row = [
                col1[i] if i < len(col1) else '',
                col2[i] if i < len(col2) else '',
                col3[i] if i < len(col3) else '',
                col4[i] if i < len(col4) else ''
            ]
            csv_writer.writerow(row)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"'Export_Datasheet_CSV' execution time: {elapsed_time:.6f} seconds")


def Import_Solar_Panel_Data(panel, folder, V_mult, I_mult, P_mult, V_offset, I_offset, P_offset):
    start_time = time.time()
    file_name_datasheet = f"{panel}_Datasheet.csv"
    file_name_dataset = f"{panel}_Datasets.csv"
    file_path_datasheet = os.path.join(folder, file_name_datasheet)
    file_path_dataset = os.path.join(folder, file_name_dataset)
    datasheet_array = []
    with open(file_path_datasheet, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            datasheet_array.append(row[0])
    V_ref, I_ref, P_ref, I_calc, P_calc, V_oc, I_sc, V_mp, I_mp, P_mp = Import_Dataset_from_CSV(file_path_dataset)
    V_lim = PV_Plotting.Calculate_Axis_Limit(V_oc, V_mult, V_offset)
    I_lim = PV_Plotting.Calculate_Axis_Limit(I_sc, I_mult, I_offset)
    P_lim = PV_Plotting.Calculate_Axis_Limit(P_mp, P_mult, P_offset)
    Panel_instance = PV_functions.Solar_Panel(datasheet_array[1], datasheet_array[2], datasheet_array[3], float(datasheet_array[4]),
                                              float(datasheet_array[5]), float(datasheet_array[6]), float(datasheet_array[7]), float(datasheet_array[8]),
                                              float(datasheet_array[9]), float(datasheet_array[10]), float(datasheet_array[11]), float(datasheet_array[12]),
                                              float(datasheet_array[13]), float(datasheet_array[14]), float(datasheet_array[15]), float(datasheet_array[16]),
                                              float(datasheet_array[17]), float(datasheet_array[18]), float(datasheet_array[19]), float(datasheet_array[20]),
                                              float(datasheet_array[21]), float(datasheet_array[22]), float(datasheet_array[23]), float(datasheet_array[24]),
                                              V_ref, I_ref, P_ref, I_calc, P_calc,
                                              V_lim, I_lim, P_lim)
    PV_functions.Print_Solar_Panel_Data(Panel_instance)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"'Import_Solar_Panel_Datasheet' execution time: {elapsed_time:.6f} seconds")
    return Panel_instance


def export_ref_arrays_to_csv(file_path, V, I, P):
    # Combine arrays into a list of tuples
    data = list(zip(V, I, P))

    # Write data to CSV file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['V_ref', 'I_ref', 'P_ref'])
        # Write data rows
        writer.writerows(data)


def export_arrays_to_csv(filename, header, *arrays):
    # Transpose the data to have arrays in columns
    data = list(zip(*arrays))
    # Write the data to the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(header.split(','))
        # Write the data
        writer.writerows(data)


def log_iteration_data_in_CSV(Iter_info, file_path):
    fieldnames = ['i', 'n', 'I_o', 'I_ph', 'R_s', 'R_sh', 'RMSE', 'nRMSE', 'R2', 'MAPE']
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the file is empty, if so, write header
        csvfile.seek(0, 2)
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(Iter_info)


def Import_Reference_Dataset_from_CSV(file_path):
    V_ref = []
    I_ref = []
    P_ref = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            V_ref.append(float(row['V_ref']))
            I_ref.append(float(row['I_ref']))
            P_ref.append(float(row['P_ref']))

    #V_oc = max(V_ref)
    #I_sc = max(I_ref)
    P_mp = max(P_ref)
    P_mp_index = P_ref.index(P_mp)
    V_mp = V_ref[P_mp_index]
    I_mp = I_ref[P_mp_index]
    len_dataset = len(V_ref)
    return V_ref, I_ref, P_ref, V_mp, I_mp, P_mp, len_dataset

def Calculate_MPP(V_ref, I_ref, P_ref):
    P_mp = max(P_ref)
    P_mp_index = P_ref.index(P_mp)
    V_mp = V_ref[P_mp_index]
    I_mp = I_ref[P_mp_index]
    return V_mp, I_mp, P_mp
