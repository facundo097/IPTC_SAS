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

def extract_errors_and_add_to_class(panel_name, array_size, base_filepath):
    error_analysis_filepath = f"{base_filepath}/{panel_name}/RESULTS/{array_size}/{panel_name}_{array_size}errors_analysis.csv"

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
    array_size = "1x1"
    AZUR_3G30A_1x1 = extract_errors_and_add_to_class(panel_name_1, array_size, base_filepath)
    AZUR_4G32C_1x1 = extract_errors_and_add_to_class(panel_name_2, array_size, base_filepath)
    CESI_CTJ30_1x1 = extract_errors_and_add_to_class(panel_name_3, array_size, base_filepath)
    Spectrolab_UTJ_1x1 = extract_errors_and_add_to_class(panel_name_4, array_size, base_filepath)

    array_size = "1x2"
    AZUR_3G30A_1x2 = extract_errors_and_add_to_class(panel_name_1, array_size, base_filepath)
    AZUR_4G32C_1x2 = extract_errors_and_add_to_class(panel_name_2, array_size, base_filepath)
    CESI_CTJ30_1x2 = extract_errors_and_add_to_class(panel_name_3, array_size, base_filepath)
    Spectrolab_UTJ_1x2 = extract_errors_and_add_to_class(panel_name_4, array_size, base_filepath)

    array_size = "2x1"
    AZUR_3G30A_2x1 = extract_errors_and_add_to_class(panel_name_1, array_size, base_filepath)
    AZUR_4G32C_2x1 = extract_errors_and_add_to_class(panel_name_2, array_size, base_filepath)
    CESI_CTJ30_2x1 = extract_errors_and_add_to_class(panel_name_3, array_size, base_filepath)
    Spectrolab_UTJ_2x1 = extract_errors_and_add_to_class(panel_name_4, array_size, base_filepath)

    array_size = "2x3"
    AZUR_3G30A_2x3 = extract_errors_and_add_to_class(panel_name_1, array_size, base_filepath)
    AZUR_4G32C_2x3 = extract_errors_and_add_to_class(panel_name_2, array_size, base_filepath)
    CESI_CTJ30_2x3 = extract_errors_and_add_to_class(panel_name_3, array_size, base_filepath)
    Spectrolab_UTJ_2x3 = extract_errors_and_add_to_class(panel_name_4, array_size, base_filepath)

    array_size = "1x6"
    AZUR_3G30A_1x6 = extract_errors_and_add_to_class(panel_name_1, array_size, base_filepath)
    AZUR_4G32C_1x6 = extract_errors_and_add_to_class(panel_name_2, array_size, base_filepath)
    CESI_CTJ30_1x6 = extract_errors_and_add_to_class(panel_name_3, array_size, base_filepath)
    Spectrolab_UTJ_1x6 = extract_errors_and_add_to_class(panel_name_4, array_size, base_filepath)

    array_size = "6x1"
    AZUR_3G30A_6x1 = extract_errors_and_add_to_class(panel_name_1, array_size, base_filepath)
    AZUR_4G32C_6x1 = extract_errors_and_add_to_class(panel_name_2, array_size, base_filepath)
    CESI_CTJ30_6x1 = extract_errors_and_add_to_class(panel_name_3, array_size, base_filepath)
    Spectrolab_UTJ_6x1 = extract_errors_and_add_to_class(panel_name_4, array_size, base_filepath)

    Avg_AZUR_3G30A = calculate_average(getattr(AZUR_3G30A_1x1, attribute), getattr(AZUR_3G30A_1x2, attribute),
                                       getattr(AZUR_3G30A_2x1, attribute), getattr(AZUR_3G30A_2x3, attribute),
                                       getattr(AZUR_3G30A_1x6, attribute), getattr(AZUR_3G30A_6x1, attribute))
    Avg_AZUR_4G32C = calculate_average(getattr(AZUR_4G32C_1x1, attribute), getattr(AZUR_4G32C_1x2, attribute),
                                       getattr(AZUR_4G32C_2x1, attribute), getattr(AZUR_4G32C_2x3, attribute),
                                       getattr(AZUR_4G32C_1x6, attribute), getattr(AZUR_4G32C_6x1, attribute))
    Avg_CESI_CTJ30 = calculate_average(getattr(CESI_CTJ30_1x1, attribute), getattr(CESI_CTJ30_1x2, attribute),
                                       getattr(CESI_CTJ30_2x1, attribute), getattr(CESI_CTJ30_2x3, attribute),
                                       getattr(CESI_CTJ30_1x6, attribute), getattr(CESI_CTJ30_6x1, attribute))
    Avg_Spectrolab_UTJ = calculate_average(getattr(Spectrolab_UTJ_1x1, attribute),
                                           getattr(Spectrolab_UTJ_1x2, attribute),
                                           getattr(Spectrolab_UTJ_2x1, attribute),
                                           getattr(Spectrolab_UTJ_2x3, attribute),
                                           getattr(Spectrolab_UTJ_1x6, attribute),
                                           getattr(Spectrolab_UTJ_6x1, attribute))

    Avg_1x1 = calculate_average(getattr(AZUR_3G30A_1x1, attribute), getattr(AZUR_4G32C_1x1, attribute),
                                getattr(CESI_CTJ30_1x1, attribute), getattr(Spectrolab_UTJ_1x1, attribute))
    Avg_1x2 = calculate_average(getattr(AZUR_3G30A_1x2, attribute), getattr(AZUR_4G32C_1x2, attribute),
                                getattr(CESI_CTJ30_1x2, attribute), getattr(Spectrolab_UTJ_1x2, attribute))
    Avg_1x6 = calculate_average(getattr(AZUR_3G30A_1x6, attribute), getattr(AZUR_4G32C_1x6, attribute),
                                getattr(CESI_CTJ30_1x6, attribute), getattr(Spectrolab_UTJ_1x6, attribute))
    Avg_2x1 = calculate_average(getattr(AZUR_3G30A_2x1, attribute), getattr(AZUR_4G32C_2x1, attribute),
                                getattr(CESI_CTJ30_2x1, attribute), getattr(Spectrolab_UTJ_2x1, attribute))
    Avg_2x3 = calculate_average(getattr(AZUR_3G30A_2x3, attribute), getattr(AZUR_4G32C_2x3, attribute),
                                getattr(CESI_CTJ30_2x3, attribute), getattr(Spectrolab_UTJ_2x3, attribute))
    Avg_6x1 = calculate_average(getattr(AZUR_3G30A_6x1, attribute), getattr(AZUR_4G32C_6x1, attribute),
                                getattr(CESI_CTJ30_6x1, attribute), getattr(Spectrolab_UTJ_6x1, attribute))

    MAPE_global = calculate_average(Avg_1x1, Avg_1x2, Avg_1x6, Avg_2x1, Avg_2x3, Avg_6x1)

    row1 = "Arreglo,AZUR 3G30A,AZUR 4G32C,CESI CTJ30,Spectrolab UTJ, Promedio (arreglo)"
    row2 = "1x1," + str(getattr(AZUR_3G30A_1x1, attribute)) + "," + str(getattr(AZUR_4G32C_1x1, attribute)) + "," + str(
        getattr(CESI_CTJ30_1x1, attribute)) + "," + str(getattr(Spectrolab_UTJ_1x1, attribute)) + "," + str(Avg_1x1)
    row3 = "1x2," + str(getattr(AZUR_3G30A_1x2, attribute)) + "," + str(getattr(AZUR_4G32C_1x2, attribute)) + "," + str(
        getattr(CESI_CTJ30_1x2, attribute)) + "," + str(getattr(Spectrolab_UTJ_1x2, attribute)) + "," + str(Avg_1x2)
    row4 = "1x6," + str(getattr(AZUR_3G30A_1x6, attribute)) + "," + str(getattr(AZUR_4G32C_1x6, attribute)) + "," + str(
        getattr(CESI_CTJ30_1x6, attribute)) + "," + str(getattr(Spectrolab_UTJ_1x6, attribute)) + "," + str(Avg_1x6)
    row5 = "2x1," + str(getattr(AZUR_3G30A_2x1, attribute)) + "," + str(getattr(AZUR_4G32C_2x1, attribute)) + "," + str(
        getattr(CESI_CTJ30_2x1, attribute)) + "," + str(getattr(Spectrolab_UTJ_2x1, attribute)) + "," + str(Avg_2x1)
    row6 = "2x3," + str(getattr(AZUR_3G30A_2x3, attribute)) + "," + str(getattr(AZUR_4G32C_2x3, attribute)) + "," + str(
        getattr(CESI_CTJ30_2x3, attribute)) + "," + str(getattr(Spectrolab_UTJ_2x3, attribute)) + "," + str(Avg_2x3)
    row7 = "6x1," + str(getattr(AZUR_3G30A_6x1, attribute)) + "," + str(getattr(AZUR_4G32C_6x1, attribute)) + "," + str(
        getattr(CESI_CTJ30_6x1, attribute)) + "," + str(getattr(Spectrolab_UTJ_6x1, attribute)) + "," + str(Avg_6x1)
    row8 = "Promedio (panel)," + str(Avg_AZUR_3G30A) + "," + str(Avg_AZUR_4G32C) + "," + str(
        Avg_CESI_CTJ30) + "," + str(Avg_Spectrolab_UTJ) + "," + str(MAPE_global)

    filepath = f"{base_filepath}/{filename}.csv"
    with open(filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row1.split(','))
        csvwriter.writerow(row2.split(','))
        csvwriter.writerow(row3.split(','))
        csvwriter.writerow(row4.split(','))
        csvwriter.writerow(row5.split(','))
        csvwriter.writerow(row6.split(','))
        csvwriter.writerow(row7.split(','))
        csvwriter.writerow(row8.split(','))


create_error_analysis_table("MAPE", "Arrays_MAPE_Analysis", base_filepath)
create_error_analysis_table("Err_V_max", "Arrays_Err_V_max_Analysis", base_filepath)
create_error_analysis_table("Err_I_max", "Arrays_Err_I_max_Analysis", base_filepath)
create_error_analysis_table("Err_P_max", "Arrays_Err_P_max_Analysis", base_filepath)
create_error_analysis_table("Err_R_max", "Arrays_Err_R_max_Analysis", base_filepath)