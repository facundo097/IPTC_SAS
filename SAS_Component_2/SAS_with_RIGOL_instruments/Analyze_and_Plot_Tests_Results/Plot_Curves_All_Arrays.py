import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib as mpl
from matplotlib.ticker import StrMethodFormatter

def clean_data(manuf, panel, array_size, base_filepath):
    raw_csv_file = manuf + "_" + panel + "_" + array_size + "_raw_data" + ".csv"
    cleaned_csv_file = manuf + "_" + panel + "_" + array_size + "_cleaned_data" + ".csv"
    filepath_input = f"{base_filepath}/{manuf}_{panel}/RAW_DATA/{raw_csv_file}"
    filepath_output = f"{base_filepath}/{manuf}_{panel}/RESULTS/{array_size}/{cleaned_csv_file}"

    # Create dictionaries to store data for each unique value of V_calc
    data_dict = {}
    # Create dictionaries to store the counts for each unique value of V_calc
    count_dict = {}

    # Read the input CSV file and populate the dictionaries
    with open(filepath_input, 'r') as input_csv:
        csv_reader = csv.DictReader(input_csv)

        for row in csv_reader:
            V_calc = float(row['V_calc'])
            # Check if this V_calc value is already in the dictionary
            if V_calc in data_dict:
                for key in row:
                    if key != 'V_calc':
                        data_dict[V_calc][key] += float(row[key])
                count_dict[V_calc] += 1
            else:
                data_dict[V_calc] = {key: float(row[key]) for key in row if key != 'V_calc'}
                count_dict[V_calc] = 1

    # Calculate the average values for each unique value of V_calc
    for V_calc, data in data_dict.items():
        for key in data:
            data[key] /= count_dict[V_calc]

    # Write the calculated data to the output CSV file
    with open(filepath_output, 'w', newline='') as output_csv:
        fieldnames = ['V_calc', 'V_meas', 'I_calc', 'I_meas', 'P_calc', 'P_meas', 'R_calc', 'R_meas', 'Err_V', 'Err_I',
                      'Err_P', 'Err_R']
        csv_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        csv_writer.writeheader()

        for V_calc, data in data_dict.items():
            row = {'V_calc': V_calc}
            row.update(data)
            csv_writer.writerow(row)

    print(f"Data processed and saved in {cleaned_csv_file}")
    return filepath_output


def extract_arrays_from_csv(cleaned_csv_file):

    # Read the CSV file into a DataFrame
    df = pd.read_csv(cleaned_csv_file)

    # Extract arrays for each column
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

    return V_calc, V_meas, I_calc, I_meas, P_calc, P_meas, Err_V, Err_I, Err_P, Err_R

def plot_two_curves(manuf, panel, array_size, V_calc, I_calc, P_calc, V_meas, I_meas, P_meas, base_filepath, axis_ranges=None):
    fig_name = f"{manuf}_{panel}_{array_size}_iv_pv_curves.png"
    fig_filepath = f"{base_filepath}/{manuf}_{panel}/RESULTS/{array_size}/{fig_name}"

    x_label = "Voltage (V)"
    y_label_1 = "Current (A)"
    y_label_2 = "Power (W)"

    title_fontsize = 20
    label_fontsize = 12
    tick_fontsize = 10
    legend_fontsize = 12
    marker_size = 4
    X_marker_size = 20
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
    plt.subplots_adjust(bottom=0.11, top=0.82, left=0.08, right=0.92)

    # Customize the title
    if manuf[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        title_1 = "I-V and P-V Curves of an " + manuf + " " + panel + " " + array_size + " array"
    else:
        title_1 = "I-V and P-V Curves of a " + manuf + " " + panel + " " + array_size + " array"
    title_2 = " "
    ax1.set_title(f"{title_1}\n{title_2}\n{title_2}", fontsize=title_fontsize, fontweight='bold')

    # Customize the axis labels and tick label font size for primary y-axis and x-axis
    ax1.set_xlabel(x_label, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold')
    ax1.set_ylabel(y_label_1, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold')
    ax1.tick_params(axis='both', labelsize=tick_fontsize)

    # Specify the number of x and y ticks for the primary y-axis
    ax1.xaxis.set_major_locator(plt.MaxNLocator(num_x_ticks))
    ax1.yaxis.set_major_locator(plt.MaxNLocator(num_y_ticks))

    # Format the tick labels with two decimals for both x and y axes
    ax1.xaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
    ax1.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

    # Increase the distance between x-axis label and tick labels
    ax1.xaxis.labelpad = labelpad

    # Plot the data on the primary y-axis
    ax1.plot(V_calc, I_calc, label="Reference Current", color='blue', linestyle='-', marker='o', markersize=marker_size, zorder=1)
    ax1.scatter(V_meas, I_meas, label="Measured Current", color='deepskyblue', marker='x', s=X_marker_size, zorder=1)

    # Create a secondary y-axis
    ax2 = ax1.twinx()

    # Plot the data on the secondary axis
    ax2.plot(V_calc, P_calc, label="Reference Power", color='firebrick', linestyle='--', marker='s', markersize=marker_size-0.5, zorder=1)
    ax2.scatter(V_meas, P_meas, label="Measured Power", color='darksalmon', marker='x', s=X_marker_size, zorder=1)

    # Set labels and tick label font size for the secondary y-axis
    ax2.set_ylabel(y_label_2, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold')
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

    # Add legends for both y-axes with specified font size
    ax1.legend(loc='upper left', bbox_to_anchor=(0.002, 1.125), ncol=2, frameon=False, fontsize=legend_fontsize)
    ax2.legend(loc='upper left', bbox_to_anchor=(0.522, 1.125), ncol=2, frameon=False, fontsize=legend_fontsize)

    # Add grid to both axes
    ax1.grid(True)
    ax2.grid(True)

    # Save picture as .png
    plt.savefig(fig_filepath, dpi=600, format='png')

def plot_errors(manuf, panel, array_size, V_calc, Err_V, Err_I, Err_P, Err_R, base_filepath, axis_ranges=None):
    # Customize the title
    if manuf[0].lower() in ['a', 'e', 'i', 'o', 'u']:
        title_1 = "Measured Relative Percent Error along the Curves of an"
    else:
        title_1 = "Measured Relative Percent Error along the Curves of a"
    title_2 = manuf + " " + panel + " " + array_size + " array"
    title_3 = ""

    fig_name = f"{manuf}_{panel}_{array_size}_errors_curves.png"
    fig_filepath = f"{base_filepath}/{manuf}_{panel}/RESULTS/{array_size}/{fig_name}"

    x_label = "Reference Voltage (V)"
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
    ax1.set_xlabel(x_label, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold')
    ax1.set_ylabel(y_label_1, fontsize=label_fontsize, labelpad=labelpad, fontweight='bold')
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
    ax1.plot(V_calc, Err_V, label="Voltage", color='g', linestyle=':', marker='v', markersize=marker_size, zorder=1)
    ax1.plot(V_calc, Err_I, label="Current", color='b', linestyle='-', marker='o', markersize=marker_size, zorder=1)
    ax1.plot(V_calc, Err_P, label="Power", color='firebrick', linestyle='--', marker='s', markersize=marker_size-0.5, zorder=1)
    ax1.plot(V_calc, Err_R, label="Resistance", color='darkorchid', linestyle='-.', marker='D', markersize=marker_size-0.5, zorder=1)

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

def calculate_average_errors(manuf, panel, array_size, Err_V, Err_I, Err_P, Err_R, V_calc, base_filepath):
    file_name = manuf + "_" + panel + "_" + array_size + "errors_analysis" + ".csv"
    output_filepath = f"{base_filepath}/{manuf}_{panel}/RESULTS/{array_size}/{file_name}"
    #hi_err_index = find_high_error_index(Err_V, Err_I, Err_P, Err_R)

    # Create a list to store the lines
    lines = []

    header = "Parameter,Average Relative Percent Error (%),Maximum Relative Percent Error (%)"
    print(header)
    lines.append(header)

    V = "Voltage," + str(round(np.mean(Err_V), 3)) + "," + str(np.max(Err_V))
    print(V)
    lines.append(V)

    I = "Current," + str(round(np.mean(Err_I), 3)) + "," + str(np.max(Err_I))
    print(I)
    lines.append(I)

    P = "Power," + str(round(np.mean(Err_P), 3)) + "," + str(np.max(Err_P))
    print(P)
    lines.append(P)

    R = "Resistance," + str(round(np.mean(Err_R), 3)) + "," + str(np.max(Err_R))
    print(R)
    lines.append(R)

    MAPE = "MAPE (%)," + str(round((np.mean(Err_V) + np.mean(Err_I) + np.mean(Err_P) + np.mean(Err_R)) / 4,3))
    print(MAPE)
    lines.append(MAPE)

    # Save the lines to a CSV file
    with open(output_filepath, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([line.split(",") for line in lines])

def generate_graphs_for_an_array(array_size, manuf, panel, y1_max, y2_max, base_filepath):
    cleaned_csv_file = clean_data(manuf, panel, array_size, base_filepath)
    V_calc, V_meas, I_calc, I_meas, P_calc, P_meas, Err_V, Err_I, Err_P, Err_R = extract_arrays_from_csv(cleaned_csv_file)
    axis_ranges = {'x': (min(V_calc) - 0.02 * max(V_calc), max(V_calc) + 0.02 * max(V_calc)), 'y1': (0, y1_max),'y2': (0, y2_max)}
    plot_two_curves(manuf, panel, array_size, V_calc, I_calc, P_calc, V_meas, I_meas, P_meas, base_filepath, axis_ranges)
    plot_errors(manuf, panel, array_size, V_calc, Err_V, Err_I, Err_P, Err_R, base_filepath)
    #calculate_average_errors(manuf, panel, array_size, Err_V, Err_I, Err_P, Err_R, V_calc, base_filepath)

def generate_graphs_for_all_arrays(manuf, panel, base_filepath):
    generate_graphs_for_an_array("1x1", manuf, panel, 0.55, 0.55*2.5, base_filepath)
    generate_graphs_for_an_array("1x2", manuf, panel, 0.55*2, 0.55*2.5*2, base_filepath)
    generate_graphs_for_an_array("1x6", manuf, panel, 0.55*6, 0.55*2.5*6, base_filepath)
    generate_graphs_for_an_array("2x1", manuf, panel, 0.55, 0.55*2.5*2, base_filepath)
    generate_graphs_for_an_array("2x3", manuf, panel, 0.55*3, 0.55*2.5*6, base_filepath)
    generate_graphs_for_an_array("6x1", manuf, panel, 0.55, 0.55*2.5*6, base_filepath)


base_filepath = "C:/Users/xblcn/OneDrive/Documents/PyCharm Projects/SAS_PowerSupply_Potentiometer/SAS_Tests"

generate_graphs_for_all_arrays("AZUR", "3G30A", base_filepath)
generate_graphs_for_all_arrays("AZUR", "4G32C", base_filepath)
generate_graphs_for_all_arrays("CESI", "CTJ30", base_filepath)
generate_graphs_for_all_arrays("Spectrolab", "UTJ", base_filepath)