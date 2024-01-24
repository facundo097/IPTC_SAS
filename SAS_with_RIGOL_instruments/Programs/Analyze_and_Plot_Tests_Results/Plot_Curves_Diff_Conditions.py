import pandas as pd
import numpy as np
import csv
import math
import matplotlib.font_manager as font_manager
import matplotlib as mpl
from matplotlib.ticker import StrMethodFormatter

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font_path = r'C:\Users\xblcn\AppData\Local\Microsoft\Windows\Fonts\Symbola.ttf'
font_label = FontProperties(size=12, fname=font_path)

# Cross-tests / Cross-panels functions
def clean_data(manuf, panel, array_size, parameter, base_filepath):
    raw_csv_file = manuf + "_" + panel + "_" + array_size + "_raw_data_" + parameter + ".csv"
    cleaned_csv_file = manuf + "_" + panel + "_" + array_size + "_cleaned_data_" + parameter + ".csv"
    filepath_input = f"{base_filepath}/{manuf}_{panel}/RAW_DATA/{raw_csv_file}"
    filepath_output = f"{base_filepath}/{manuf}_{panel}/RESULTS/{parameter}/{cleaned_csv_file}"

    # Read the raw data from the CSV file
    data = pd.read_csv(filepath_input)

    # Group the data by the 'G' column and calculate the mean for each group
    cleaned_data = data.groupby(parameter).mean().reset_index()

    # Write the cleaned data to the new CSV file
    cleaned_data.to_csv(filepath_output, index=False)

    return filepath_output

def extract_arrays_from_csv(cleaned_csv_file, parameter):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(cleaned_csv_file)

    # Extract arrays for each column
    parameter_arr = df[parameter].to_numpy()
    V_calc = df['V_calc'].to_numpy()
    V_meas = df['V_meas'].to_numpy()
    I_calc = df['I_calc'].to_numpy()
    I_meas = df['I_meas'].to_numpy()
    P_calc = df['P_calc'].to_numpy()
    P_meas = df['P_meas'].to_numpy()
    R_calc = df['R_calc'].to_numpy()
    R_meas = df['R_meas'].to_numpy()
    Err_V = df['Err_V'].to_numpy()
    Err_I = df['Err_I'].to_numpy()
    Err_P = df['Err_P'].to_numpy()
    Err_R = df['Err_R'].to_numpy()

    return parameter_arr, V_calc, V_meas, I_calc, I_meas, P_calc, P_meas, R_calc, R_meas, Err_V, Err_I, Err_P, Err_R

def calculate_average_errors(manuf, panel, array_size, parameter, Err_V, Err_I, Err_P, Err_R, base_filepath):
    file_name = manuf + "_" + panel + "_" + array_size + "_errors_analysis_" + parameter + ".csv"
    filepath_output = f"{base_filepath}/{manuf}_{panel}/RESULTS/{parameter}/{file_name}"

    # Create a list to store the lines
    lines = []

    header = "Parameter,Average Relative Percent Error (%),Maximum Relative Percent Error (%)"
    print(header)
    lines.append(header)

    V = "Voltage," + str(round(np.mean(Err_V), 3)) + "," + str(round(np.max(Err_V), 3))
    print(V)
    lines.append(V)

    I = "Current," + str(round(np.mean(Err_I), 3)) + "," + str(round(np.max(Err_I), 3))
    print(I)
    lines.append(I)

    P = "Power," + str(round(np.mean(Err_P), 3)) + "," + str(round(np.max(Err_P), 3))
    print(P)
    lines.append(P)

    R = "Resistance," + str(round(np.mean(Err_R), 3)) + "," + str(round(np.max(Err_R), 3))
    print(R)
    lines.append(R)

    MAPE = "MAPE (%)," + str(round((np.mean(Err_V) + np.mean(Err_I) + np.mean(Err_P) + np.mean(Err_R)) / 4, 3))
    print(MAPE)
    lines.append(MAPE)

    #V_high_error = "Tolerable Error Threshold (V)," + str(V_calc[hi_err_index])
    #print(V_high_error)
    #lines.append(V_high_error)

    # Save the lines to a CSV file
    with open(filepath_output, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([line.split(",") for line in lines])

def plot_tests_curves(manuf, panel, array_size, X_id, X_arr, V_calc, I_calc, P_calc, R_calc, V_meas, I_meas, P_meas, R_meas, base_filepath, axis_ranges=None):
    X_name = ""
    x_label = ""
    y_label_1 = ""
    y_label_2 = ""
    if X_id == "G":
        X_name = "Irradiance"
        x_label = "Irradiance (W/m²)"
        y_label_1 = "Voltage (V), Current (A), Power (W)"
        y_label_2 = "Resistance (Ω)"
    elif X_id == "T":
        X_name = "Temperature"
        x_label = "Temperature (°C)"
        y_label_1 = "Voltage (V), Power (W), Resistance (Ω)"
        y_label_2 = "Current (A)"
    elif X_id == "Ang":
        X_name = "Incidence Angle"
        x_label = "Incidence Angle (°)"
        y_label_1 = "Voltage (V), Current (A), Power (W)"
        y_label_2 = "Resistance (Ω)"

    fig_name = f"{manuf}_{panel}_{array_size}_MPPT_curve_{X_id}.png"
    fig_filepath = f"{base_filepath}/{manuf}_{panel}/RESULTS/{X_id}/{fig_name}"
    title_1 = "Maximum Power Point Tracking for different values of"
    if manuf[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        title_2 = f"{X_name} on an {manuf} {panel} {array_size} array"
    else:
        title_2 = f"{X_name} on a {manuf} {panel} {array_size} array"
    title_3 = " "

    title_fontsize = 20
    label_fontsize = 12
    tick_fontsize = 10
    legend_fontsize = 12
    marker_size = 4
    X_marker_size = 30
    num_y_ticks = 6
    num_x_ticks = 8
    labelpad = 10

    # Use CMU Serif font
    mpl.rcParams['font.family'] = 'serif'
    cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
    mpl.rcParams['font.serif'] = cmfont.get_name()
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['axes.unicode_minus'] = False

    # Create a figure and primary axis
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Adjust subplot parameters to set the height of the plot area
    plt.subplots_adjust(bottom=0.11, top=0.77, left=0.08, right=0.92)

    # Customize the title
    ax1.set_title(f"{title_1}\n{title_2}\n{title_3}\n{title_3}", fontsize=title_fontsize, fontweight='bold')

    # Customize the axis labels and tick label font size for primary y-axis and x-axis
    ax1.set_xlabel(x_label, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold', fontproperties=font_label)
    ax1.set_ylabel(y_label_1, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold', fontproperties=font_label)
    ax1.tick_params(axis='both', labelsize=tick_fontsize)

    # Specify the number of x and y ticks for the primary y-axis
    ax1.xaxis.set_major_locator(plt.MaxNLocator(num_x_ticks))
    ax1.yaxis.set_major_locator(plt.MaxNLocator(num_y_ticks))

    # Format the tick labels with two decimals for both x and y axes
    ax1.xaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
    ax1.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

    # Increase the distance between x-axis label and tick labels
    ax1.xaxis.labelpad = labelpad

    if X_id == "G" or X_id == "Ang":
        # Plot the data on the primary y-axis
        ax1.plot(X_arr, V_calc, label='Ref. Voltage', marker='v', linestyle='--', color='g', markersize=marker_size, zorder=1)
        ax1.scatter(X_arr, V_meas, label="Meas. Voltage", color='lime', marker='x', s=X_marker_size,zorder=1)
        ax1.plot(X_arr, I_calc, label='Ref. Current', marker='o', linestyle='--', color='b', markersize=marker_size, zorder=1)
        ax1.scatter(X_arr, I_meas, label="Meas. Current", color='deepskyblue', marker='x', s=X_marker_size, zorder=1)
        ax1.plot(X_arr, P_calc, label='Ref. Power', marker='s', linestyle='--', color='firebrick', markersize=marker_size, zorder=1)
        ax1.scatter(X_arr, P_meas, label="Meas. Power", color='darksalmon', marker='x', s=X_marker_size, zorder=1)

        # Create a secondary y-axis
        ax2 = ax1.twinx()

        # Plot R_calc and R_meas on the secondary y-axis
        ax2.plot(X_arr, R_calc, label='Ref. Resistance', marker='D', linestyle='--', color='darkorchid', markersize=marker_size, zorder=1)
        ax2.scatter(X_arr, R_meas, label="Meas. Resistance", color='violet', marker='x', s=X_marker_size, zorder=1)

        ax1.legend(loc='upper left', bbox_to_anchor=(0.062, 1.1625), ncol=3, frameon=False, fontsize=legend_fontsize)
        ax2.legend(loc='upper left', bbox_to_anchor=(0.702, 1.1625), ncol=1, frameon=False, fontsize=legend_fontsize)

    else:
        # Plot the data on the primary y-axis
        ax1.plot(X_arr, V_calc, label='Ref. Voltage', marker='v', linestyle='--', color='g', markersize=marker_size, zorder=1)
        ax1.scatter(X_arr, V_meas, label="Meas. Voltage", color='lime', marker='x', s=X_marker_size, zorder=1)
        ax1.plot(X_arr, P_calc, label='Ref. Power', marker='s', linestyle='--', color='firebrick', markersize=marker_size, zorder=1)
        ax1.scatter(X_arr, P_meas, label="Meas. Power", color='darksalmon', marker='x', s=X_marker_size, zorder=1)
        ax1.plot(X_arr, R_calc, label='Ref. Resistance', marker='D', linestyle='--', color='darkorchid', markersize=marker_size, zorder=1)
        ax1.scatter(X_arr, R_meas, label="Meas. Resistance", color='violet', marker='x', s=X_marker_size, zorder=1)

        # Create a secondary y-axis
        ax2 = ax1.twinx()

        # Plot I_calc and I_meas on the secondary y-axis
        ax2.plot(X_arr, I_calc, label='Ref. Current', marker='o', linestyle='--', color='b', markersize=marker_size, zorder=1)
        ax2.scatter(X_arr, I_meas, label="Meas. Current", color='deepskyblue', marker='x', s=X_marker_size, zorder=1)
        ax2.set_ylim(round(min(I_calc) / 0.05) * 0.05 - 0.05, math.ceil((max(I_calc) + max(I_calc) * 0.25) / 0.05) * 0.05)

        ax1.legend(loc='upper left', bbox_to_anchor=(0.055, 1.1625), ncol=3, frameon=False, fontsize=legend_fontsize)
        ax2.legend(loc='upper left', bbox_to_anchor=(0.73, 1.1625), ncol=1, frameon=False, fontsize=legend_fontsize)

    # Set labels and tick label font size for the secondary y-axis
    ax2.set_ylabel(y_label_2, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold', fontproperties=font_label)
    ax2.tick_params(axis='y', labelsize=tick_fontsize)

    # Specify the number of y ticks for the secondary y-axis
    ax2.yaxis.set_major_locator(plt.MaxNLocator(num_y_ticks))

    # Format the tick labels with two decimals for the secondary y-axis
    ax2.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

    # Set the number of x ticks for the primary x-axis
    ax1.xaxis.set_major_locator(plt.MaxNLocator(num_x_ticks))

    # Format the tick labels with two decimals for the primary x-axis
    ax1.xaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

    # Set axis ranges if provided
    if axis_ranges:
        ax1.set_xlim(axis_ranges['x'])
        ax1.set_ylim(axis_ranges['y1'])
        ax2.set_ylim(axis_ranges['y2'])

    # Add grid to both axes
    ax1.grid(True)
    ax2.grid(True)

    # Save picture as .png
    plt.savefig(fig_filepath, dpi=600, format='png')

def plot_tests_errors(manuf, panel, array_size, X_variable_id, X_variable_arr, X_variable_name, X_variable_unit, Err_V, Err_I, Err_P, Err_R, base_filepath, axis_ranges=None):
    title_1 = "Measured Relative Percent Error at different values of"
    # Customize the title
    if manuf[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        title_2 = X_variable_name + " on an " + manuf + " " + panel + " " + array_size + " array"
    else:
        title_2 = X_variable_name + " on a " + manuf + " " + panel + " " + array_size + " array"
    title_3 = ""

    fig_name = f"{manuf}_{panel}_{array_size}_MPPT_errors_curves_{X_variable_id}.png"
    fig_filepath = f"{base_filepath}/{manuf}_{panel}/RESULTS/{X_variable_id}/{fig_name}"

    x_label = X_variable_name + " " + X_variable_unit
    y_label_1 = "Percentage (%)"

    title_fontsize = 20
    label_fontsize = 12
    tick_fontsize = 10
    legend_fontsize = 12
    marker_size = 4
    num_y_ticks = 10
    num_x_ticks = 10
    labelpad = 10

    # Use CMU Serif font
    mpl.rcParams['font.family'] = 'serif'
    cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
    mpl.rcParams['font.serif'] = cmfont.get_name()
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['axes.unicode_minus'] = False


    # Create a figure and primary axis
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Adjust subplot parameters to set the height of the plot area
    plt.subplots_adjust(bottom=0.11, top=0.82, left=0.08, right=0.92)


    ax1.set_title(f"{title_1}\n{title_2}\n{title_3}", fontsize=title_fontsize, fontweight='bold')

    # Customize the axis labels and tick label font size for primary y-axis and x-axis
    ax1.set_xlabel(x_label, labelpad=labelpad, fontproperties=font_label)
    ax1.set_ylabel(y_label_1, labelpad=labelpad, fontproperties=font_label)
    ax1.tick_params(axis='both', labelsize=tick_fontsize)

    # Specify the number of x and y ticks for the primary y-axis
    ax1.xaxis.set_major_locator(plt.MaxNLocator(num_x_ticks))
    ax1.yaxis.set_major_locator(plt.MaxNLocator(num_y_ticks))

    # Format the tick labels with two decimals for both x and y axes
    ax1.xaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
    ax1.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

    # Increase the distance between x-axis label and tick labels
    ax1.xaxis.labelpad = labelpad

    # Add grid to both axes
    ax1.grid(True)

    # Plot the data on the primary y-axis
    ax1.plot(X_variable_arr, Err_V, label="Voltage", color='g', linestyle=':', marker='v', markersize=marker_size, zorder=1)
    ax1.plot(X_variable_arr, Err_I, label="Current", color='b', linestyle='-', marker='o', markersize=marker_size, zorder=1)
    ax1.plot(X_variable_arr, Err_P, label="Power", color='firebrick', linestyle='--', marker='s', markersize=marker_size-0.5, zorder=1)
    ax1.plot(X_variable_arr, Err_R, label="Resistance", color='darkorchid', linestyle='-.', marker='D', markersize=marker_size-0.5, zorder=1)

    # Set the number of x ticks for the primary x-axis
    ax1.xaxis.set_major_locator(plt.MaxNLocator(num_x_ticks))

    # Format the tick labels with two decimals for the primary x-axis
    ax1.xaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))


    # Set axis ranges if provided
    if axis_ranges:
        ax1.set_xlim(axis_ranges['x'])
        ax1.set_ylim(axis_ranges['y1'])

    # Add legends for both y-axes with specified font size
    ax1.legend(loc='upper left', bbox_to_anchor=(0.175, 1.085), ncol=4, frameon=False, fontsize=legend_fontsize)

    # Save picture as .png
    plt.savefig(fig_filepath, dpi=600, format='png')

def plot_curves_G(manuf, panel, base_filepath):
    cleaned_csv_file = clean_data(manuf, panel, "2x3", "G", base_filepath)
    G, V_calc, V_meas, I_calc, I_meas, P_calc, P_meas, R_calc, R_meas, Err_V, Err_I, Err_P, Err_R = extract_arrays_from_csv(cleaned_csv_file, "G")
    calculate_average_errors(manuf, panel, "2x3", "G", Err_V, Err_I, Err_P, Err_R, base_filepath)
    plot_tests_curves(manuf, panel, "2x3", "G", G, V_calc, I_calc, P_calc, R_calc, V_meas, I_meas, P_meas, R_meas, base_filepath)
    plot_tests_errors(manuf, panel, "2x3", "G", G, "Irradiance", "(W/m²)", Err_V, Err_I, Err_P, Err_R, base_filepath)

def plot_curves_T(manuf, panel, base_filepath):
    cleaned_csv_file = clean_data(manuf, panel, "2x3", "T", base_filepath)
    T, V_calc, V_meas, I_calc, I_meas, P_calc, P_meas, R_calc, R_meas, Err_V, Err_I, Err_P, Err_R = extract_arrays_from_csv(cleaned_csv_file, "T")
    calculate_average_errors(manuf, panel, "2x3", "T", Err_V, Err_I, Err_P, Err_R, base_filepath)
    plot_tests_curves(manuf, panel, "2x3", "T", T, V_calc, I_calc, P_calc, R_calc, V_meas, I_meas, P_meas, R_meas, base_filepath)
    plot_tests_errors(manuf, panel, "2x3", "T", T, "Temperature", "(°C)", Err_V, Err_I, Err_P, Err_R, base_filepath)

def plot_curves_Ang(manuf, panel, base_filepath):
    cleaned_csv_file = clean_data(manuf, panel, "2x1", "Ang", base_filepath)
    Ang, V_calc, V_meas, I_calc, I_meas, P_calc, P_meas, R_calc, R_meas, Err_V, Err_I, Err_P, Err_R = extract_arrays_from_csv(cleaned_csv_file, "Ang")
    calculate_average_errors(manuf, panel, "2x1", "Ang", Err_V, Err_I, Err_P, Err_R, base_filepath)
    plot_tests_curves(manuf, panel, "2x1", "Ang", Ang, V_calc, I_calc, P_calc, R_calc, V_meas, I_meas, P_meas, R_meas, base_filepath)
    plot_tests_errors(manuf, panel, "2x1", "Ang", Ang, "Incidence Angle", "(°)", Err_V, Err_I, Err_P, Err_R, base_filepath)

def generate_panel_plots(manuf, panel, base_filepath):
    plot_curves_G(manuf, panel, base_filepath)
    plot_curves_T(manuf, panel, base_filepath)
    plot_curves_Ang(manuf, panel, base_filepath)

base_filepath = "C:/Users/xblcn/OneDrive/Documents/PyCharm Projects/SAS_PowerSupply_Potentiometer/SAS_Tests"

generate_panel_plots("AZUR", "3G30A", base_filepath)
generate_panel_plots("AZUR", "4G32C", base_filepath)
generate_panel_plots("CESI", "CTJ30", base_filepath)
generate_panel_plots("Spectrolab", "UTJ", base_filepath)