import PV_Single_Diode
import PV_CSV
import cv2
import numpy as np
import time
import os

# Creates a class to define all the attributes of the solar panel that should be displayed in its datasheet.
class Solar_Panel:
    def __init__(self, panel_manuf, panel_model, panel_type, panel_eff,
                 T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s, TK_V_oc, TK_I_sc, E_g,
                 n, I_ph, I_o, R_s, R_sh, RMSE, nRMSE, R2, MAPE, V_ref, I_ref, P_ref, I_calc, P_calc, V_lim, I_lim, P_lim):
        self.panel_manuf = panel_manuf     # Panel manufacturer
        self.panel_model = panel_model     # Panel model
        self.panel_type = panel_type       # Panel technology (i.e. mono/poly-crystalline, thin-film, multi-junction, tandem)
        self.panel_eff = panel_eff         # Panel efficiency [%]
        self.T_c_ref = T_c_ref             # Cell temperature at reference conditions [K]
        self.G_ref = G_ref                 # Solar irradiance at reference conditions [W/m^2]
        self.V_oc = V_oc                   # Open Circuit Voltage [V]
        self.I_sc = I_sc                   # Short Circuit Current [A]
        self.V_mp = V_mp                   # MPP Voltage [V]
        self.I_mp = I_mp                   # MPP Current [A]
        self.P_mp = P_mp                   # MPP Power [W]
        self.N_s = N_s                     # Number of cells in series
        self.TK_V_oc = TK_V_oc             # V_oc temperature coefficient [V/K]
        self.TK_I_sc = TK_I_sc             # I_sc temperature coefficient [A/K]
        self.E_g = E_g                     # Band gap energy [eV]
        self.n = n                         # Diode ideality factor at reference conditions
        self.I_ph = I_ph                   # Photoelectric current at reference conditions [A]
        self.I_o = I_o                     # Diode inverse saturation current at reference conditions [A]
        self.R_s = R_s                     # Series resistance at reference conditions [ohm]
        self.R_sh = R_sh                   # Shunt resistance at reference conditions [ohm]
        self.RMSE = RMSE                   # Root-Mean-Squared-Error for the calculated parameters
        self.nRMSE = nRMSE                 # Normalized Root-Mean-Squared-Error for the calculated parameters
        self.R2 = R2                       # Coefficient of Determination for the calculated parameters
        self.MAPE = MAPE                   # Mean-Absolute-Percentage-Error for the calculated parameters
        self.V_ref = V_ref                 # Voltage dataset from manufacturer at reference conditions [V]
        self.I_ref = I_ref                 # Current dataset from manufacturer at reference conditions [A]
        self.P_ref = P_ref                 # Power dataset from manufacturer at reference conditions [W]
        self.I_calc = I_calc               # Current dataset for the calculated parameters at reference conditions [A]
        self.P_calc = P_calc               # Power dataset for the calculated parameters at reference conditions [W]
        self.V_lim = V_lim                 # Voltage axis limit to plot I-V and P-V Curves
        self.I_lim = I_lim                 # Current axis limit to plot I-V and P-V Curves
        self.P_lim = P_lim                 # Power axis limit to plot I-V and P-V Curves


# Creates a function to print the solar panel datasheet in the console
def Print_Solar_Panel_Data(solar_panel):
    print("---------------------------------- SOLAR PANEL DATA ----------------------------------")
    print("  Panel manufacturer__________________________________", solar_panel.panel_manuf)
    print("  Panel model_________________________________________", solar_panel.panel_model)
    print("  Panel type__________________________________________", solar_panel.panel_type)
    print("  Panel efficiency____________________________________", solar_panel.panel_eff)
    print("  Temp. at ref. conditions____________________________", solar_panel.T_c_ref)
    print("  Irrad. at ref. conditions___________________________", solar_panel.G_ref)
    print("  Open Circuit Voltage________________________________", solar_panel.V_oc)
    print("  Short Circuit Current_______________________________", solar_panel.I_sc)
    print("  MPP Voltage_________________________________________", solar_panel.V_mp)
    print("  MPP Current_________________________________________", solar_panel.I_mp)
    print("  MPP Power___________________________________________", solar_panel.P_mp)
    print("  Number of cells in series___________________________", solar_panel.N_s)
    print("  V_oc temp. coefficient______________________________", solar_panel.TK_V_oc)
    print("  I_sc temp. coefficient______________________________", solar_panel.TK_I_sc)
    print("  Band gap____________________________________________", solar_panel.E_g)
    print("  Diode ideality factor_______________________________", solar_panel.n)
    print("  Photoelectric current_______________________________", solar_panel.I_ph)
    print("  Diode inv. sat. current_____________________________", solar_panel.I_o)
    print("  Series resistance___________________________________", solar_panel.R_s)
    print("  Shunt resistance____________________________________", solar_panel.R_sh)
    print("  Root-Mean-Squared-Error_____________________________", solar_panel.RMSE)
    print("  Normalized-Root-Mean-Squared-Error__________________", solar_panel.nRMSE)
    print("  Coefficient of Determination________________________", solar_panel.R2)
    print("  Mean-Absolute-Percentage-Error______________________", solar_panel.MAPE)
    print("  Voltage array at reference conditions lenght________", len(solar_panel.V_ref))
    print("  Currrent array at reference conditions lenght_______", len(solar_panel.I_ref))
    print("  Power array at reference conditions lenght__________", len(solar_panel.P_ref))
    print("  Currrent array calculated by the model lenght_______", len(solar_panel.I_calc))
    print("  Power array calculated by the model lenght__________", len(solar_panel.P_calc))
    print("  Voltage axis limit to plot I-V and P-V Curves_______", solar_panel.V_lim)
    print("  Current axis limit to plot I-V and P-V Curves_______", solar_panel.I_lim)
    print("  Power axis limit to plot I-V and P-V Curves_________", solar_panel.P_lim)
    print("--------------------------------------------------------------------------------------")


def Generate_Data_Solar_Panel_1(folder_path):
    # Panel AZUR 3G30A - Parameters from datasheet
    panel_manuf = "AZUR"
    panel_model = "3G30A"
    panel_type = "Triple Junction GaAs"
    panel_eff = 30
    T_c_ref = 273.15 + 28
    G_ref = 1367
    V_oc = 2.6987  # Known open-circuit voltage from datasheet
    I_sc = 0.4958  # Known short-circuit current from datasheet
    TK_V_oc = -6.2e-3  # [V/°C] temperature coefficient of V_oc
    TK_I_sc = 3.6e-4  # [A/°C] temperature coefficient of I_sc
    N_s = 1  # Number of solar cells in series, usually specified in the datasheet. If not, assume it's 1
    E_g = 1.6  # [eV]. Energy bandgap for triple junction cells, for silicon cells E_g_ref = 1.121 eV (De Soto, 2006)

    # Axis limits to plot I-V and P-V Curves
    V_lim = 3.0  # Voltage-axis limit in the reference I-V Curve from the datasheet
    I_lim = 0.6  # Current-axis limit in the reference I-V Curve from the datasheet
    P_lim = 1.5  # Power-axis limit in the reference P-V Curve from the datasheet

    # Variables to calculate the 5 unknown parameters from the single-diode model using the Hussein method (2017)
    R_s_guess = 0.3  # Initial value for R_s. When you get an overflow error, usually it's because you set this value too low
    n_inc = 0.01  # The increments of the ideality factor for each loop
    tol = 1e-8  # The tolerance limit for R_s in the Newton-Rhapson loop

    # Function to calculate the unknown parameters and generate a datasheet and datasets for the panel
    Panel_instance = Generate_Panel_Data(panel_manuf, panel_model, panel_type, panel_eff, folder_path, V_oc, I_sc, N_s,
                                         TK_V_oc, TK_I_sc, E_g, R_s_guess, n_inc, tol, T_c_ref, G_ref, V_lim, I_lim, P_lim)
    return Panel_instance


def Generate_Data_Solar_Panel_2(folder_path):
    # Panel AZUR 4G32C - Parameters from datasheet
    panel_manuf = "AZUR"
    panel_model = "4G32C"
    panel_type = "Quadruple Junction GaAs"
    panel_eff = 32
    T_c_ref = 273.15 + 25
    G_ref = 1367
    V_oc = 3.375  # Known open-circuit voltage from datasheet
    I_sc = 0.455  # Known short-circuit current from datasheet
    TK_V_oc = -8.4e-3  # [V/°C] temperature coefficient of V_oc
    TK_I_sc = 7.0e-5   # [A/°C] temperature coefficient of I_sc
    N_s = 1  # Number of solar cells in series, usually specified in the datasheet. If not, assume it's 1
    E_g = 1.6 # [eV]. Energy bandgap for triple junction cells, for silicon cells E_g_ref = 1.121 eV (De Soto, 2006)

    # Axis limits to plot I-V and P-V Curves
    V_lim = 3.5  # Voltage-axis limit in the reference I-V Curve from the datasheet
    I_lim = 0.5  # Current-axis limit in the reference I-V Curve from the datasheet
    P_lim = 1.4  # Power-axis limit in the reference P-V Curve from the datasheet

    # Variables to calculate the 5 unknown parameters from the single-diode model using the Hussein method (2017)
    R_s_guess = 0.4  # Initial value for R_s. When you get an overflow error, usually it's because you set this value too low
    n_inc = 0.01  # The increments of the ideality factor for each loop
    tol = 1e-8  # The tolerance limit for R_s in the Newton-Rhapson loop

    # Function to calculate the unknown parameters and generate a datasheet and datasets for the panel
    Panel_instance = Generate_Panel_Data(panel_manuf, panel_model, panel_type, panel_eff, folder_path, V_oc, I_sc, N_s,
                                         TK_V_oc, TK_I_sc, E_g, R_s_guess, n_inc, tol, T_c_ref, G_ref, V_lim, I_lim, P_lim)
    return Panel_instance


def Generate_Data_Solar_Panel_3(folder_path):
    # Panel CESI CTJ30 - Parameters from datasheet
    panel_manuf = "CESI"
    panel_model = "CTJ30"
    panel_type = "Triple Junction InGaP/GaAs/Ge"
    panel_eff = 29.5
    T_c_ref = 273.15 + 25
    G_ref = 1367
    V_oc = 2.6  # Known open-circuit voltage from datasheet
    I_sc = 0.473  # Known short-circuit current from datasheet
    TK_V_oc = -8.4e-3  # [V/°C] temperature coefficient of V_oc
    TK_I_sc = 7.0e-5  # [A/°C] temperature coefficient of I_sc
    N_s = 1  # Number of solar cells in series, usually specified in the datasheet. If not, assume it's 1
    E_g = 1.6  # [eV]. Energy bandgap for triple junction cells, for silicon cells E_g_ref = 1.121 eV (De Soto, 2006)

    # Axis limits to plot I-V and P-V Curves
    V_lim = 3.0  # Voltage-axis limit in the reference I-V Curve from the datasheet
    I_lim = 0.5  # Current-axis limit in the reference I-V Curve from the datasheet
    P_lim = 1.1  # Power-axis limit in the reference P-V Curve from the datasheet

    # Variables to calculate the 5 unknown parameters from the single-diode model using the Hussein method (2017)
    R_s_guess = 0.4  # Initial value for R_s. When you get an overflow error, usually it's because you set this value too low
    n_inc = 0.01  # The increments of the ideality factor for each loop
    tol = 1e-8  # The tolerance limit for R_s in the Newton-Rhapson loop

    # Function to calculate the unknown parameters and generate a datasheet and datasets for the panel
    Panel_instance = Generate_Panel_Data(panel_manuf, panel_model, panel_type, panel_eff, folder_path, V_oc, I_sc, N_s,
                                         TK_V_oc, TK_I_sc, E_g, R_s_guess, n_inc, tol, T_c_ref, G_ref, V_lim, I_lim, P_lim)
    return Panel_instance


def Generate_Data_Solar_Panel_4(folder_path):
    # Panel Spectrolab UTJ - Parameters from datasheet
    panel_manuf = "Spectrolab"
    panel_model = "UTJ"
    panel_type = "Triple Junction GaInP2/InGaAs/Ge"
    panel_eff = 28.3
    T_c_ref = 273.15 + 28
    G_ref = 1353
    V_oc = 2.660  # Known open-circuit voltage from datasheet
    I_sc = 0.548  # Known short-circuit current from datasheet
    TK_V_oc = -5.9e-3  # [V/°C] temperature coefficient of V_oc
    TK_I_sc = 3.84e-5  # [A/°C] temperature coefficient of I_sc
    N_s = 1  # Number of solar cells in series, usually specified in the datasheet. If not, assume it's 1
    E_g = 1.6  # [eV]. Energy bandgap for triple junction cells, for silicon cells E_g_ref = 1.121 eV (De Soto, 2006)

    # Axis limits to plot I-V and P-V Curves
    V_lim = 3.0  # Voltage-axis limit in the reference I-V Curve from the datasheet
    I_lim = 0.6  # Current-axis limit in the reference I-V Curve from the datasheet
    P_lim = 1.3  # Power-axis limit in the reference P-V Curve from the datasheet

    # Variables to calculate the 5 unknown parameters from the single-diode model using the Hussein method (2017)
    R_s_guess = 0.4  # Initial value for R_s. When you get an overflow error, usually it's because you set this value too low
    n_inc = 0.01  # The increments of the ideality factor for each loop
    tol = 1e-8  # The tolerance limit for R_s in the Newton-Rhapson loop

    # Function to calculate the unknown parameters and generate a datasheet and datasets for the panel
    Panel_instance = Generate_Panel_Data(panel_manuf, panel_model, panel_type, panel_eff, folder_path, V_oc, I_sc, N_s,
                                         TK_V_oc, TK_I_sc, E_g, R_s_guess, n_inc, tol, T_c_ref, G_ref, V_lim, I_lim, P_lim)
    return Panel_instance


# Computer-Vision-based algorith to extract the dataset from the picture of an I-V curve provided by the manufacturer
def Extract_Dataset_from_Image(panel_manuf, panel_model, V_oc, I_sc, dataset_res, folder):
    start_time = time.time()
    panel_name = panel_manuf + "_" + panel_model
    image_path = f"{panel_name}_0.png"
    original_image = cv2.imread(image_path)
    # Flip the image along the lower x-axis. This is so the (0,0) pixel coordinate of the image coincides with the origin of the curve
    mirrored_image = cv2.flip(original_image, 0)
    # Apply filters to the image to get a high contrast between the graph's background and the curve
    gray_image = cv2.cvtColor(mirrored_image, cv2.COLOR_BGR2GRAY)
    output, image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # The algorithm selects a pixel in the X axis and checks which of its corresponding pixels in Y are white
    # When a white pixel is found, its coordinates are added to arrays X and Y
    # After scanning all the pixels in Y corresponding to the current pixel in X,
    # the loop jumps to a new pixel in X and starts over
    # The algorithm ends when the new pixel in X is greater than the length of the X axis of the image
    y_length, x_length = image.shape  # Get dimensions of the image
    next_x = x_length // dataset_res  # Determines the size of the jump to the next pixel in the x-axis
    current_x = 0  # Initial pixel in the x-axis
    current_y = y_length - 1  # Initial pixel in the y-axis
    X = []  # Arrays to store coordinates where the curve is found
    Y = []
    while current_x <= x_length - 1:
        while current_y >= 0:
            if image[current_y, current_x] == 255:  # Check if the pixel is white
                X.append(current_x)
                Y.append(current_y)
            current_y -= 1

        current_x += next_x
        current_y = y_length - 1
    # Find all the Y values that correspond to a single X value and calculate the average Y value
    # These average values are added to a new array
    cumulative_sum = {}
    count = {}
    for x_val, y_val in zip(X, Y):
        if x_val not in cumulative_sum:
            cumulative_sum[x_val] = y_val
            count[x_val] = 1
        else:
            cumulative_sum[x_val] += y_val
            count[x_val] += 1
    X_unique = np.array(list(cumulative_sum.keys()))
    Y_unique = np.array([cumulative_sum[x_val] / count[x_val] for x_val in X_unique])
    # Scale all the values in the arrays, which are in pixels, to the expected values of current and voltage
    # From the datasheet of the panel, we know the maximum values, given by V_oc and I_sc
    # We also know that the minimum values for both voltage and current are zero
    V = (X_unique - X_unique.min()) * (V_oc - 0) / (X_unique.max() - X_unique.min())
    I = (Y_unique - Y_unique.min()) * (I_sc - 0) / (Y_unique.max() - Y_unique.min())
    # Calculate the corresponding power to each pair of V and I
    P = []
    for v, i in zip(V, I):
        p = v * i
        P.append(p)
    file_name = f"{panel_manuf}_{panel_model}_Reference_Datasets.csv"
    file_path = os.path.join(folder, file_name)
    PV_CSV.export_ref_arrays_to_csv(file_path, V, I, P)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"'Extract_Dataset_from_Image' execution time: {elapsed_time:.6f} seconds")
    return V, I, P


def Generate_Panel_Data(panel_manuf, panel_model, panel_type, panel_eff, folder_path, V_oc, I_sc, N_s, TK_V_oc, TK_I_sc, E_g, R_s_guess, n_inc, tol, T_c_ref, G_ref, V_lim, I_lim, P_lim):
    # Function to calculate dataset from the picture of the panel's I-V Curve
    V_ref, I_ref, P_ref = Extract_Dataset_from_Image(panel_manuf, panel_model, V_oc, I_sc, 500, folder_path)

    # Function to calculate the MPP points from the generated reference datasets
    V_mp, I_mp, P_mp = PV_CSV.Calculate_MPP(V_ref, I_ref, P_ref)

    # Function to calculate the 5 parameters at reference conditions of temperature and irradiance
    n, I_o, I_ph, R_s, R_sh, RMSE, nRMSE, R2, MAPE = PV_Single_Diode.hussein2017(V_oc, I_sc, V_mp, I_mp, N_s, R_s_guess, n_inc, V_ref,
                                                                I_ref, tol, T_c_ref, panel_manuf, panel_model, folder_path)

    # Calculate dataset of current and power at the reference conditions
    I_calc, P_calc = Calculate_Current_and_Power(V_ref, n, I_o, I_ph, R_s, R_sh, N_s, T_c_ref)

    # Create a solar panel instance with its parameters (at reference conditions)
    Panel_instance = Solar_Panel(panel_manuf, panel_model, panel_type, panel_eff,
                                 T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s, TK_V_oc, TK_I_sc, E_g,
                                 n, I_ph, I_o, R_s, R_sh, RMSE, nRMSE, R2, MAPE, V_ref, I_ref, P_ref,
                                 I_calc, P_calc, V_lim, I_lim, P_lim)

    # Export datasets and datasheet of the panel in .CSV files
    PV_CSV.Export_Datasets_CSV(panel_manuf, panel_model, V_ref, I_ref, P_ref, I_calc, P_calc, folder_path)
    PV_CSV.Export_Datasheet_CSV(panel_manuf, panel_model, panel_type, panel_eff, T_c_ref, G_ref,
                                V_oc, I_sc, V_mp, I_mp, P_mp, N_s, TK_V_oc, TK_I_sc, E_g,
                                n, I_o, I_ph, R_s, R_sh, RMSE, nRMSE, R2, MAPE, folder_path)

    # Print solar panel datasheet
    Print_Solar_Panel_Data(Panel_instance)

    # Return solar panel instance
    return Panel_instance


def Create_5_Datasets_Constant_T(max_V, resolution, panel_instance, constant,  variable_1,  variable_2,  variable_3,  variable_4,  variable_5):
    V_ref = Create_V_range(max_V, resolution)

    n_1, I_ph_1, I_o_1, R_s_1, R_sh_1 = PV_Single_Diode.Scale_Parameters(variable_1, constant, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_1: {n_1}, I_ph_1: {I_ph_1}, I_o_1: {I_o_1}, R_s_1: {R_s_1}, R_sh_1: {R_sh_1}")

    n_2, I_ph_2, I_o_2, R_s_2, R_sh_2 = PV_Single_Diode.Scale_Parameters(variable_2, constant, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_2: {n_2}, I_ph_2: {I_ph_2}, I_o_2: {I_o_2}, R_s_2: {R_s_2}, R_sh_2: {R_sh_2}")

    n_3, I_ph_3, I_o_3, R_s_3, R_sh_3 = PV_Single_Diode.Scale_Parameters(variable_3, constant, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_3: {n_3}, I_ph_3: {I_ph_3}, I_o_3: {I_o_3}, R_s_3: {R_s_3}, R_sh_3: {R_sh_3}")

    n_4, I_ph_4, I_o_4, R_s_4, R_sh_4 = PV_Single_Diode.Scale_Parameters(variable_4, constant, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_4: {n_4}, I_ph_3: {I_ph_4}, I_o_3: {I_o_4}, R_s_3: {R_s_4}, R_sh_3: {R_sh_4}")

    n_5, I_ph_5, I_o_5, R_s_5, R_sh_5 = PV_Single_Diode.Scale_Parameters(variable_5, constant, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_5: {n_5}, I_ph_5: {I_ph_5}, I_o_5: {I_o_5}, R_s_5: {R_s_5}, R_sh_5: {R_sh_5}")

    I_1, P_1 = Calculate_Current_and_Power(V_ref, n_1, I_o_1, I_ph_1, R_s_1, R_sh_1, panel_instance.N_s, panel_instance.T_c_ref)
    I_2, P_2 = Calculate_Current_and_Power(V_ref, n_2, I_o_2, I_ph_2, R_s_2, R_sh_2, panel_instance.N_s, panel_instance.T_c_ref)
    I_3, P_3 = Calculate_Current_and_Power(V_ref, n_3, I_o_3, I_ph_3, R_s_3, R_sh_3, panel_instance.N_s, panel_instance.T_c_ref)
    I_4, P_4 = Calculate_Current_and_Power(V_ref, n_4, I_o_4, I_ph_4, R_s_4, R_sh_4, panel_instance.N_s, panel_instance.T_c_ref)
    I_5, P_5 = Calculate_Current_and_Power(V_ref, n_5, I_o_5, I_ph_5, R_s_5, R_sh_5, panel_instance.N_s, panel_instance.T_c_ref)

    return V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5


def Create_5_Datasets_Constant_G(max_V, resolution, panel_instance, constant,  variable_1,  variable_2,  variable_3,  variable_4,  variable_5):
    V_ref = Create_V_range(max_V, resolution)

    n_1, I_ph_1, I_o_1, R_s_1, R_sh_1 = PV_Single_Diode.Scale_Parameters(constant, variable_1, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_1: {n_1}, I_ph_1: {I_ph_1}, I_o_1: {I_o_1}, R_s_1: {R_s_1}, R_sh_1: {R_sh_1}")

    n_2, I_ph_2, I_o_2, R_s_2, R_sh_2 = PV_Single_Diode.Scale_Parameters(constant, variable_2, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_2: {n_2}, I_ph_2: {I_ph_2}, I_o_2: {I_o_2}, R_s_2: {R_s_2}, R_sh_2: {R_sh_2}")

    n_3, I_ph_3, I_o_3, R_s_3, R_sh_3 = PV_Single_Diode.Scale_Parameters(constant, variable_3, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_3: {n_3}, I_ph_3: {I_ph_3}, I_o_3: {I_o_3}, R_s_3: {R_s_3}, R_sh_3: {R_sh_3}")

    n_4, I_ph_4, I_o_4, R_s_4, R_sh_4 = PV_Single_Diode.Scale_Parameters(constant, variable_4, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_4: {n_4}, I_ph_3: {I_ph_4}, I_o_3: {I_o_4}, R_s_3: {R_s_4}, R_sh_3: {R_sh_4}")

    n_5, I_ph_5, I_o_5, R_s_5, R_sh_5 = PV_Single_Diode.Scale_Parameters(constant, variable_5, 0,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_5: {n_5}, I_ph_5: {I_ph_5}, I_o_5: {I_o_5}, R_s_5: {R_s_5}, R_sh_5: {R_sh_5}")

    I_1, P_1 = Calculate_Current_and_Power(V_ref, n_1, I_o_1, I_ph_1, R_s_1, R_sh_1, panel_instance.N_s, panel_instance.T_c_ref)
    I_2, P_2 = Calculate_Current_and_Power(V_ref, n_2, I_o_2, I_ph_2, R_s_2, R_sh_2, panel_instance.N_s, panel_instance.T_c_ref)
    I_3, P_3 = Calculate_Current_and_Power(V_ref, n_3, I_o_3, I_ph_3, R_s_3, R_sh_3, panel_instance.N_s, panel_instance.T_c_ref)
    I_4, P_4 = Calculate_Current_and_Power(V_ref, n_4, I_o_4, I_ph_4, R_s_4, R_sh_4, panel_instance.N_s, panel_instance.T_c_ref)
    I_5, P_5 = Calculate_Current_and_Power(V_ref, n_5, I_o_5, I_ph_5, R_s_5, R_sh_5, panel_instance.N_s, panel_instance.T_c_ref)

    return V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5


def Create_5_Datasets_Diff_Angle(max_V, resolution, panel_instance, constant_G, constant_T, variable_1,  variable_2,  variable_3,  variable_4,  variable_5):
    V_ref = Create_V_range(max_V, resolution)

    n_1, I_ph_1, I_o_1, R_s_1, R_sh_1 = PV_Single_Diode.Scale_Parameters(constant_G, constant_T, variable_1,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_1: {n_1}, I_ph_1: {I_ph_1}, I_o_1: {I_o_1}, R_s_1: {R_s_1}, R_sh_1: {R_sh_1}")

    n_2, I_ph_2, I_o_2, R_s_2, R_sh_2 = PV_Single_Diode.Scale_Parameters(constant_G, constant_T, variable_2,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_2: {n_2}, I_ph_2: {I_ph_2}, I_o_2: {I_o_2}, R_s_2: {R_s_2}, R_sh_2: {R_sh_2}")

    n_3, I_ph_3, I_o_3, R_s_3, R_sh_3 = PV_Single_Diode.Scale_Parameters(constant_G, constant_T, variable_3,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_3: {n_3}, I_ph_3: {I_ph_3}, I_o_3: {I_o_3}, R_s_3: {R_s_3}, R_sh_3: {R_sh_3}")

    n_4, I_ph_4, I_o_4, R_s_4, R_sh_4 = PV_Single_Diode.Scale_Parameters(constant_G, constant_T, variable_4,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_4: {n_4}, I_ph_3: {I_ph_4}, I_o_3: {I_o_4}, R_s_3: {R_s_4}, R_sh_3: {R_sh_4}")

    n_5, I_ph_5, I_o_5, R_s_5, R_sh_5 = PV_Single_Diode.Scale_Parameters(constant_G, constant_T, variable_5,
                                                                         panel_instance.G_ref, panel_instance.T_c_ref,
                                                                         panel_instance.V_oc, panel_instance.I_sc,
                                                                         panel_instance.TK_V_oc, panel_instance.TK_I_sc,
                                                                         panel_instance.n, panel_instance.I_ph,
                                                                         panel_instance.I_o,
                                                                         panel_instance.R_s, panel_instance.R_sh,
                                                                         panel_instance.E_g)
    print(f"n_5: {n_5}, I_ph_5: {I_ph_5}, I_o_5: {I_o_5}, R_s_5: {R_s_5}, R_sh_5: {R_sh_5}")

    I_1, P_1 = Calculate_Current_and_Power(V_ref, n_1, I_o_1, I_ph_1, R_s_1, R_sh_1, panel_instance.N_s, panel_instance.T_c_ref)
    I_2, P_2 = Calculate_Current_and_Power(V_ref, n_2, I_o_2, I_ph_2, R_s_2, R_sh_2, panel_instance.N_s, panel_instance.T_c_ref)
    I_3, P_3 = Calculate_Current_and_Power(V_ref, n_3, I_o_3, I_ph_3, R_s_3, R_sh_3, panel_instance.N_s, panel_instance.T_c_ref)
    I_4, P_4 = Calculate_Current_and_Power(V_ref, n_4, I_o_4, I_ph_4, R_s_4, R_sh_4, panel_instance.N_s, panel_instance.T_c_ref)
    I_5, P_5 = Calculate_Current_and_Power(V_ref, n_5, I_o_5, I_ph_5, R_s_5, R_sh_5, panel_instance.N_s, panel_instance.T_c_ref)

    return V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5


def Calculate_Current_and_Power(V_ref, n, I_o, I_ph, R_s, R_sh, N_s, T_c_ref):
    len_dataset = len(V_ref)
    I_calc = []
    P_calc = []
    consecutive_negative_count = 0

    for i in range(len_dataset):
        V_i = V_ref[i]
        I_i = PV_Single_Diode.Solve_for_Current(V_i, n, I_o, I_ph, R_s, R_sh, N_s, T_c_ref)

        if I_i < 0:
            consecutive_negative_count += 1
        else:
            consecutive_negative_count = 0

        if consecutive_negative_count > 10:
            I_calc.extend([-1] * (len_dataset - i))
            P_calc.extend([-1] * (len_dataset - i))
            break

        P_i = V_i * I_i
        I_calc.append(I_i)
        P_calc.append(P_i)

    return I_calc, P_calc


def Create_V_range(max_V, resolution):
    V_arr = []
    V_i = 0
    inc = max_V / resolution
    while V_i <= max_V:
        V_arr.append(V_i)
        V_i += inc

    return V_arr