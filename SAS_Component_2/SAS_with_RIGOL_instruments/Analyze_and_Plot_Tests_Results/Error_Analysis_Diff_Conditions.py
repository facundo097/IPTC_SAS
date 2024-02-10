import csv

class Solar_Panel_Array:
    def __init__(self, Err_V_avg, Err_V_max, Err_I_avg, Err_I_max, Err_P_avg, Err_P_max, Err_R_avg, Err_R_max, MAPE):
        self.Err_V_avg = Err_V_avg
        self.Err_V_max = Err_V_max
        self.Err_I_avg = Err_I_avg
        self.Err_I_max = Err_I_max
        self.Err_P_avg = Err_P_avg
        self.Err_P_max = Err_P_max
        self.Err_R_avg = Err_R_avg
        self.Err_R_max = Err_R_max
        self.MAPE = MAPE

base_filepath = "C:/Users/xblcn/OneDrive/Documents/PyCharm Projects/SAS_PowerSupply_Potentiometer/SAS_Tests"

panel_name_1 = "AZUR_3G30A"
panel_name_2 = "AZUR_4G32C"
panel_name_3 = "CESI_CTJ30"
panel_name_4 = "Spectrolab_UTJ"

def calculate_average(*args):
    if len(args) == 0:
        return 0  # To avoid division by zero if no arguments are provided
    return sum(args) / len(args)

def extract_errors_and_add_to_class(panel_name, array_size, condition, base_filepath):
    error_analysis_filepath = f"{base_filepath}/{panel_name}/RESULTS/{condition}/{panel_name}_{array_size}_errors_analysis_{condition}.csv"

    # Initialize variables
    Err_V_avg, Err_V_max, Err_I_avg, Err_I_max, Err_P_avg, Err_P_max, Err_R_avg, Err_R_max, MAPE = (None,) * 9

    # Read the CSV file
    with open(error_analysis_filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == 'Voltage':
                Err_V_avg, Err_V_max = float(row[1]), float(row[2])
            elif row[0] == 'Current':
                Err_I_avg, Err_I_max = float(row[1]), float(row[2])
            elif row[0] == 'Power':
                Err_P_avg, Err_P_max = float(row[1]), float(row[2])
            elif row[0] == 'Resistance':
                Err_R_avg, Err_R_max = float(row[1]), float(row[2])
            elif row[0] == 'MAPE (%)':
                MAPE = float(row[1])

    panel_instance = Solar_Panel_Array(Err_V_avg, Err_V_max, Err_I_avg, Err_I_max, Err_P_avg, Err_P_max, Err_R_avg,
                                       Err_R_max, MAPE)
    return panel_instance


def create_error_analysis_table(attribute, filename, base_filepath):
    condition = "G"
    array_size = "2x3"
    AZUR_3G30A_G = extract_errors_and_add_to_class(panel_name_1, array_size, condition, base_filepath)
    AZUR_4G32C_G = extract_errors_and_add_to_class(panel_name_2, array_size, condition, base_filepath)
    CESI_CTJ30_G = extract_errors_and_add_to_class(panel_name_3, array_size, condition, base_filepath)
    Spectrolab_UTJ_G = extract_errors_and_add_to_class(panel_name_4, array_size, condition, base_filepath)

    condition = "T"
    array_size = "2x3"
    AZUR_3G30A_T = extract_errors_and_add_to_class(panel_name_1, array_size, condition, base_filepath)
    AZUR_4G32C_T = extract_errors_and_add_to_class(panel_name_2, array_size, condition, base_filepath)
    CESI_CTJ30_T = extract_errors_and_add_to_class(panel_name_3, array_size, condition, base_filepath)
    Spectrolab_UTJ_T = extract_errors_and_add_to_class(panel_name_4, array_size, condition, base_filepath)

    condition = "Ang"
    array_size = "2x1"
    AZUR_3G30A_Ang = extract_errors_and_add_to_class(panel_name_1, array_size, condition, base_filepath)
    AZUR_4G32C_Ang = extract_errors_and_add_to_class(panel_name_2, array_size, condition, base_filepath)
    CESI_CTJ30_Ang = extract_errors_and_add_to_class(panel_name_3, array_size, condition, base_filepath)
    Spectrolab_UTJ_Ang = extract_errors_and_add_to_class(panel_name_4, array_size, condition, base_filepath)


    Avg_AZUR_3G30A = calculate_average(getattr(AZUR_3G30A_G, attribute), getattr(AZUR_3G30A_T, attribute),getattr(AZUR_3G30A_Ang, attribute))
    Avg_AZUR_4G32C = calculate_average(getattr(AZUR_4G32C_G, attribute), getattr(AZUR_4G32C_T, attribute),getattr(AZUR_4G32C_Ang, attribute))
    Avg_CESI_CTJ30 = calculate_average(getattr(CESI_CTJ30_G, attribute), getattr(CESI_CTJ30_T, attribute),getattr(CESI_CTJ30_Ang, attribute))
    Avg_Spectrolab_UTJ = calculate_average(getattr(Spectrolab_UTJ_G, attribute), getattr(Spectrolab_UTJ_T, attribute),getattr(Spectrolab_UTJ_Ang, attribute))

    Avg_G = calculate_average(getattr(AZUR_3G30A_G, attribute), getattr(AZUR_4G32C_G, attribute), getattr(CESI_CTJ30_G, attribute), getattr(Spectrolab_UTJ_G, attribute))
    Avg_T = calculate_average(getattr(AZUR_3G30A_T, attribute), getattr(AZUR_4G32C_T, attribute), getattr(CESI_CTJ30_T, attribute), getattr(Spectrolab_UTJ_T, attribute))
    Avg_Ang = calculate_average(getattr(AZUR_3G30A_Ang, attribute), getattr(AZUR_4G32C_Ang, attribute), getattr(CESI_CTJ30_Ang, attribute), getattr(Spectrolab_UTJ_Ang, attribute))

    Attribute_global = calculate_average(Avg_G, Avg_T, Avg_Ang)

    row1 = "Condición variable,AZUR 3G30A,AZUR 4G32C,CESI CTJ30,Spectrolab UTJ, Promedio (condición)"
    row2 = "Irradiancia," + str(getattr(AZUR_3G30A_G, attribute)) + "," + str(getattr(AZUR_4G32C_G, attribute)) + "," + str(getattr(CESI_CTJ30_G, attribute)) + "," + str(getattr(Spectrolab_UTJ_G, attribute)) + "," + str(Avg_G)
    row3 = "Temperatura," + str(getattr(AZUR_3G30A_T, attribute)) + "," + str(getattr(AZUR_4G32C_T, attribute)) + "," + str(getattr(CESI_CTJ30_T, attribute)) + "," + str(getattr(Spectrolab_UTJ_T, attribute)) + "," + str(Avg_T)
    row4 = "Ángulo de incidencia," + str(getattr(AZUR_3G30A_Ang, attribute)) + "," + str(getattr(AZUR_4G32C_Ang, attribute)) + "," + str(getattr(CESI_CTJ30_Ang, attribute)) + "," + str(getattr(Spectrolab_UTJ_Ang, attribute)) + "," + str(Avg_Ang)
    row5 = "Promedio (panel)," + str(Avg_AZUR_3G30A) + "," + str(Avg_AZUR_4G32C) + "," + str(Avg_CESI_CTJ30) + "," + str(Avg_Spectrolab_UTJ) + "," + str(Attribute_global)

    filepath = f"{base_filepath}/{filename}.csv"
    with open(filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row1.split(','))
        csvwriter.writerow(row2.split(','))
        csvwriter.writerow(row3.split(','))
        csvwriter.writerow(row4.split(','))
        csvwriter.writerow(row5.split(','))

create_error_analysis_table("MAPE", "Conditions_MAPE_Analysis", base_filepath)
create_error_analysis_table("Err_V_max", "Conditions_Err_V_max_Analysis", base_filepath)
create_error_analysis_table("Err_I_max", "Conditions_Err_I_max_Analysis", base_filepath)
create_error_analysis_table("Err_P_max", "Conditions_Err_P_max_Analysis", base_filepath)
create_error_analysis_table("Err_R_max", "Conditions_Err_R_max_Analysis", base_filepath)