import matplotlib.pyplot as plt
import os
import PV_functions
import PV_CSV


def Plot_Single_Curve(fig_num, title, panel_manuf, panel_model, x_data, y_data, x_lim, y_lim, x_label, y_label, marker, linestyle, color, grid, method, folder):
    panel_name = panel_manuf + "_" + panel_model
    file_name = f"{panel_name}_{fig_num}.png"
    file_path = os.path.join(folder, file_name)
    font_size = 12
    plt.figure(figsize=(15, 10))
    plt.xlim(0, x_lim)  # Set X axis range
    plt.ylim(0, y_lim)  # Set Y axis range
    plt.plot(x_data, y_data, marker=marker, linestyle=linestyle, color=color, linewidth=3)
    plt.title(title + " for " + panel_manuf + " " + panel_model + method, fontsize=20)
    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.grid(grid)
    plt.savefig(file_path, dpi=500)
    #plt.show()


def Plot_Two_Curves(fig_num, title, panel_manuf, panel_model, x_data, y1_data, y2_data, x_lim, y_lim, x_label, y_label, marker, linestyle, color1, color2, grid, method, folder):
    graph_title = title + " for " + panel_manuf + " " + panel_model + method
    panel_name = panel_manuf + "_" + panel_model
    file_name = f"{panel_name}_{fig_num}.png"
    file_path = os.path.join(folder, file_name)
    font_size = 12
    x_vs_y1_legend = "Reference"
    x_vs_y2_legend = "Calculated"
    plt.figure(figsize=(15, 10))
    ax = plt.subplot(111)
    ax.set_xlim(0, x_lim)
    ax.set_ylim(0, y_lim)
    ax.plot(x_data, y1_data, label=x_vs_y1_legend, marker=marker, linestyle=linestyle, color=color1, linewidth=3)
    ax.plot(x_data, y2_data, label=x_vs_y2_legend, marker=marker, linestyle=linestyle, color=color2, linewidth=3)
    ax.set_xlabel(x_label, fontsize=font_size)
    ax.set_ylabel(y_label, fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.grid()
    ax.legend(fontsize=font_size)
    ax.set_title(graph_title, fontsize=20)
    plt.savefig(file_path, dpi=500)
    #plt.show()


def Plot_from_Parameters(panel_manuf, panel_model, V_ref, I_ref, P_ref, I_calc, P_calc, V_lim, I_lim, P_lim, T_c, folder):
    Plot_Single_Curve("1", "Reference I-V Curve", panel_manuf, panel_model, V_ref, I_ref, V_lim, I_lim,
                      "Voltage (V)", "Current (A)", ',', '-', "b", True, "", folder)
    Plot_Single_Curve("2", "Calculated I-V Curve", panel_manuf, panel_model, V_ref, I_calc, V_lim, I_lim,
                      "Voltage (V)", "Current (A)", ',', '-', "r", True, " (Husseim)", folder)
    Plot_Single_Curve("3", "Reference P-V Curve", panel_manuf, panel_model, V_ref, P_ref, V_lim, P_lim,
                      "Voltage (V)", "Power (W)", ',', '-', "b", True, "", folder)
    Plot_Single_Curve("4", "Calculated P-V Curve", panel_manuf, panel_model, V_ref, P_calc, V_lim, P_lim,
                      "Voltage (V)", "Power (W)", ',', '-', "r", True, " (Husseim)", folder)
    Plot_Two_Curves("5", "Comparison of I-V Curves", panel_manuf, panel_model, V_ref, I_ref, I_calc, V_lim, I_lim,
                    "Voltage (V)", "Current (A)", ",", "-", "b", "r", True, " (Husseim)", folder)
    Plot_Two_Curves("6", "Comparison of P-V Curves", panel_manuf, panel_model, V_ref, P_ref, P_calc, V_lim, P_lim,
                    "Voltage (V)", "Power (W)", ",", "-", "b", "r", True, " (Husseim)", folder)


def Plot_Panel_Curves(Panel,folder):
    # Plot and save I-V and P-V Curves, get datasets in form of arrays
    Plot_from_Parameters(Panel.panel_manuf, Panel.panel_model,
                         Panel.V_ref, Panel.I_ref, Panel.P_ref,
                         Panel.I_calc, Panel.P_calc,
                         Panel.V_lim, Panel.I_lim, Panel.P_lim,
                         Panel.T_c_ref,folder)


def Calculate_Axis_Limit(number, multiple, offset):
    closest_multiple = number + (multiple - number % multiple) + offset
    return closest_multiple


def Plot_Five_Curves(fig_num, title1, title2, panel_instance, x_data, y1_data, y2_data, y3_data, y4_data,y5_data, y1_level, y2_level, y3_level, y4_level,y5_level,level_unit, x_label, y_label, marker, linestyle, color1, color2, color3, color4, color5, offset_x_lim, offset_y_lim, folder):
    graph_title = title1 + panel_instance.panel_manuf + " " + panel_instance.panel_model + title2
    panel_name = panel_instance.panel_manuf + "_" + panel_instance.panel_model
    file_name = f"{panel_name}_{fig_num}.png"
    file_path = os.path.join(folder, file_name)
    font_size = 12
    x_lim = Calculate_Axis_Limit(max(x_data), 0.5, offset_x_lim)
    y_lim = Calculate_Axis_Limit(max(y1_data), 0.1, offset_y_lim)
    x_vs_y1_legend = str(y1_level) + " " + level_unit
    x_vs_y2_legend = str(y2_level) + " " + level_unit
    x_vs_y3_legend = str(y3_level) + " " + level_unit
    x_vs_y4_legend = str(y4_level) + " " + level_unit
    x_vs_y5_legend = str(y5_level) + " " + level_unit
    plt.figure(figsize=(15, 10))
    ax = plt.subplot(111)
    ax.set_xlim(0, x_lim)
    ax.set_ylim(0, y_lim)
    ax.plot(x_data, y1_data, label=x_vs_y1_legend, marker=marker, linestyle=linestyle, color=color1, linewidth=3)
    ax.plot(x_data, y2_data, label=x_vs_y2_legend, marker=marker, linestyle=linestyle, color=color2, linewidth=3)
    ax.plot(x_data, y3_data, label=x_vs_y3_legend, marker=marker, linestyle=linestyle, color=color3, linewidth=3)
    ax.plot(x_data, y4_data, label=x_vs_y4_legend, marker=marker, linestyle=linestyle, color=color4, linewidth=3)
    ax.plot(x_data, y5_data, label=x_vs_y5_legend, marker=marker, linestyle=linestyle, color=color5, linewidth=3)
    ax.set_xlabel(x_label, fontsize=font_size)
    ax.set_ylabel(y_label, fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.grid()
    ax.legend(fontsize=font_size)
    ax.set_title(graph_title, fontsize=20)
    plt.savefig(file_path, dpi=500)
    #plt.show()


def Plot_Curves_Different_Conditions(panel_instance, V_max, folder, V_offset_IV_1, I_offset_IV_1, V_offset_PV_1, I_offset_PV_1, V_offset_IV_2, I_offset_IV_2, V_offset_PV_2, I_offset_PV_2, V_offset_IV_3, I_offset_IV_3, V_offset_PV_3, I_offset_PV_3):
    # Test conditions:
    G_1 = 1375
    G_2 = 1100
    G_3 = 825
    G_4 = 550
    G_5 = 275
    T_c_1 = 273.15 + 80
    T_c_2 = 273.15 + 40
    T_c_3 = 273.15 + 0
    T_c_4 = 273.15 - 40
    T_c_5 = 273.15 - 80
    ang_1 = 0
    ang_2 = 20
    ang_3 = 40
    ang_4 = 60
    ang_5 = 80

    test_G = 1367
    test_T = 273.15 + 25

    header = "V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5"
    V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5 = PV_functions.Create_5_Datasets_Constant_T(V_max, 300, panel_instance,
                                                                                                        test_T, G_1, G_2, G_3, G_4, G_5)
    dataset_file_name = f"{panel_instance.panel_manuf}_{panel_instance.panel_model}_Irradiance_Range_Dataset.csv"
    dataset_file_path = os.path.join(folder, dataset_file_name)
    PV_CSV.export_arrays_to_csv(dataset_file_path, header, V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5)
    Plot_Five_Curves("7", "I-V Curves of ", " at different levels of irradiance (T = " + f"{(test_T - 273.15):.0f}" + " °C)",
                     panel_instance, V_ref, I_1, I_2, I_3, I_4, I_5, G_1, G_2, G_3, G_4, G_5,
                     "W/m²", "Voltage (V)", "Current (A)", ',', '-', "b", "g", "r", "c", "m", V_offset_IV_1, I_offset_IV_1, folder)

    Plot_Five_Curves("8", "P-V Curves of ", " at different levels of irradiance (T = " + f"{(test_T - 273.15):.0f}" + " °C)",
                     panel_instance, V_ref, P_1, P_2, P_3, P_4, P_5, G_1, G_2, G_3, G_4, G_5,
                     "W/m²", "Voltage (V)", "Current (A)", ',', '-', "b", "g", "r", "c", "m", V_offset_PV_1, I_offset_PV_1, folder)

    V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5 = PV_functions.Create_5_Datasets_Constant_G(V_max+1.5, 300, panel_instance,
                                                                                             test_G,T_c_1, T_c_2, T_c_3, T_c_4, T_c_5)
    dataset_file_name = f"{panel_instance.panel_manuf}_{panel_instance.panel_model}_Temperature_Range_Datasets.csv"
    dataset_file_path = os.path.join(folder, dataset_file_name)
    PV_CSV.export_arrays_to_csv(dataset_file_path, header, V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5)
    Plot_Five_Curves("9", "I-V Curves of ", " at different temperatures (G = " + f"{(test_G):.0f}" + " W/m²)",
                     panel_instance, V_ref, I_1, I_2, I_3, I_4, I_5, T_c_1 - 273.15, T_c_2 - 273.15,
                     T_c_3 - 273.15, T_c_4 - 273.15, T_c_5 - 273.15,
                     "°C", "Voltage (V)", "Power (W)", ',', '-', "b", "g", "r", "c", "m", V_offset_IV_2, I_offset_IV_2, folder)

    Plot_Five_Curves("10", "P-V Curves of ", " at different temperatures (G = " + f"{(test_G):.0f}" + " W/m²)",
                     panel_instance, V_ref, P_1, P_2, P_3, P_4, P_5, T_c_1 - 273.15, T_c_2 - 273.15,
                     T_c_3 - 273.15, T_c_4 - 273.15, T_c_5 - 273.15,
                     "°C", "Voltage (V)", "Power (W)", ',', '-', "b", "g", "r", "c", "m", V_offset_PV_2, I_offset_PV_2, folder)

    V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5 = PV_functions.Create_5_Datasets_Diff_Angle(V_max, 300, panel_instance, test_G, test_T,
                                                                                                        ang_1, ang_2, ang_3, ang_4, ang_5)
    dataset_file_name = f"{panel_instance.panel_manuf}_{panel_instance.panel_model}_Inc_Angle_Range_Datasets.csv"
    dataset_file_path = os.path.join(folder, dataset_file_name)
    PV_CSV.export_arrays_to_csv(dataset_file_path, header, V_ref, I_1, P_1, I_2, P_2, I_3, P_3, I_4, P_4, I_5, P_5)
    Plot_Five_Curves("11", "I-V Curves of ", " at different incidence angles (G = " + f"{(test_G):.0f}" +
                     " W/m², T = " + f"{(test_T-273.15):.0f}" + " °C)",
                     panel_instance, V_ref, I_1, I_2, I_3, I_4, I_5, ang_1, ang_2, ang_3, ang_4, ang_5,
                     "°", "Voltage (V)", "Power (W)", ',', '-', "b", "g", "r", "c", "m", V_offset_IV_3, I_offset_IV_3, folder)

    Plot_Five_Curves("12", "P-V Curves of ", " at different incidence angles (G = " + f"{(test_G):.0f}" +
                     " W/m², T = " + f"{(test_T-273.15):.0f}" + " °C)",
                     panel_instance, V_ref, P_1, P_2, P_3, P_4, P_5, ang_1, ang_2, ang_3, ang_4, ang_5,
                     "°", "Voltage (V)", "Power (W)", ',', '-', "b", "g", "r", "c", "m", V_offset_PV_3, I_offset_PV_3, folder)

