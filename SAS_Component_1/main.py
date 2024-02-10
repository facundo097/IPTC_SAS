import PV_functions
import PV_Plotting
import PV_CSV

# Paste the folder path where you want the results to be saved. For example: "D:\Python_Programs\IPTC_SAS_Results"
results_folder_path = "D:\Python_Programs\IPTC_SAS_Results"
print(f"Results folder path: {results_folder_path}")

# Adjust the following binary variables according to your needs
generate_data_from_images = 1         # set to 0 if you want to import already generated datasets and datasheets
generate_plots_ref_conditions = 1
generate_plots_diff_conditions = 1

if generate_data_from_images == 1:
    # The following functions extract the reference dataset from pictures of I-V curves using computer vision,
    # calculates the unknown parameters of the single diode model, and generates the solar panels' datasheets
    # Make sure these images are in this project's folder:
    # https://drive.google.com/drive/folders/1WbK3gCMJvdKTDe39xvYG48LmgBFiwgz9?usp=sharing
    AZUR_3G30A = PV_functions.Generate_Data_Solar_Panel_1(results_folder_path)
    AZUR_4G32C = PV_functions.Generate_Data_Solar_Panel_2(results_folder_path)
    CESI_CTJ30 = PV_functions.Generate_Data_Solar_Panel_3(results_folder_path)
    Spectrolab_UTJ = PV_functions.Generate_Data_Solar_Panel_4(results_folder_path)

else:
    # The following functions read already generated datasets and datasheets in order to extract the panel's data
    # Make sure these .CSV files are in the results folder path:
    # https://drive.google.com/drive/folders/1yPj-dm1EeBoBbwi2-qfjow7O5xVr8PZF?usp=sharing
    AZUR_3G30A = PV_CSV.Import_Solar_Panel_Data("AZUR_3G30A", results_folder_path, 0.5, 0.1, 0.1, 0, 0.1, 0.2)
    AZUR_4G32C = PV_CSV.Import_Solar_Panel_Data("AZUR_4G32C", results_folder_path, 0.5, 0.1, 0.1, 0, 0, 0.1)
    CESI_CTJ30 = PV_CSV.Import_Solar_Panel_Data("CESI_CTJ30", results_folder_path, 0.5, 0.1, 0.1, 0, 0, 0.1)
    Spectrolab_UTJ = PV_CSV.Import_Solar_Panel_Data("Spectrolab_UTJ", results_folder_path, 0.5, 0.1, 0.1, 0, 0, 0.1)

if generate_plots_ref_conditions == 1:
    # The following functions plot panels' I-V and P-V curves at reference conditions
    PV_Plotting.Plot_Panel_Curves(AZUR_3G30A, results_folder_path)
    PV_Plotting.Plot_Panel_Curves(AZUR_4G32C, results_folder_path)
    PV_Plotting.Plot_Panel_Curves(CESI_CTJ30, results_folder_path)
    PV_Plotting.Plot_Panel_Curves(Spectrolab_UTJ, results_folder_path)

if generate_plots_diff_conditions == 1:
    # The following functions scale the panel's parameters to other conditions of temperature and irradiance
    # and plots the I-V and P-V curves at 5 different conditions
    # The multiple offsets help to properly adjust the curves location in the plots
    PV_Plotting.Plot_Curves_Different_Conditions(AZUR_3G30A, 3.5, results_folder_path,
                                                 -0.5, 0.05, # V_offset_IV_1, I_offset_IV_1   |    AZUR_3G30A_7.png
                                                 -0.5, 0.1,  # V_offset_PV_1, I_offset_PV_1   |    AZUR_3G30A_8.png
                                                 -1.0, 0.0,  # V_offset_IV_2, I_offset_IV_2   |    AZUR_3G30A_9.png
                                                 -1.0, 0.6,  # V_offset_PV_2, I_offset_PV_2   |    AZUR_3G30A_10.png
                                                 -0.5, 0.1,  # V_offset_IV_3, I_offset_IV_3   |    AZUR_3G30A_11.png
                                                 -0.5, 0.1)  # V_offset_PV_3, I_offset_PV_3   |    AZUR_3G30A_12.png
    PV_Plotting.Plot_Curves_Different_Conditions(AZUR_4G32C, 4, results_folder_path,
                                                 -0.5, 0.0,  # V_offset_IV_1, I_offset_IV_1   |    AZUR_4G32C_7.png
                                                 -0.5, 0.1,  # V_offset_PV_1, I_offset_PV_1   |    AZUR_4G32C_8.png
                                                 -1.0, 0.0,  # V_offset_IV_2, I_offset_IV_2   |    AZUR_4G32C_9.png
                                                 -1.0, 0.7,  # V_offset_PV_2, I_offset_PV_2   |    AZUR_4G32C_10.png
                                                 -0.5, 0.0,  # V_offset_IV_3, I_offset_IV_3   |    AZUR_4G32C_11.png
                                                 -0.5, 0.2)  # V_offset_PV_3, I_offset_PV_3   |    AZUR_4G32C_12.png
    PV_Plotting.Plot_Curves_Different_Conditions(CESI_CTJ30, 4, results_folder_path,
                                                 -1.0, 0.0,  # V_offset_IV_1, I_offset_IV_1   |    CESI_CTJ30_7.png
                                                 -1.0, 0.1,  # V_offset_PV_1, I_offset_PV_1   |    CESI_CTJ30_8.png
                                                 -1.5, 0.0,  # V_offset_IV_2, I_offset_IV_2   |    CESI_CTJ30_9.png
                                                 -1.5, 0.7,  # V_offset_PV_2, I_offset_PV_2   |    CESI_CTJ30_10.png
                                                 -1.0, 0.0,  # V_offset_IV_3, I_offset_IV_3   |    CESI_CTJ30_11.png
                                                 -1.0, 0.1)  # V_offset_PV_3, I_offset_PV_3   |    CESI_CTJ30_12.png
    PV_Plotting.Plot_Curves_Different_Conditions(Spectrolab_UTJ, 4, results_folder_path,
                                                 -1.0, 0.0,  # V_offset_IV_1, I_offset_IV_1   |    Spectrolab_UTJ_7.png
                                                 -1.0, 0.25, # V_offset_PV_1, I_offset_PV_1   |    Spectrolab_UTJ_8.png
                                                 -1.5, 0.0,  # V_offset_IV_2, I_offset_IV_2   |    Spectrolab_UTJ_9.png
                                                 -1.5, 0.7,  # V_offset_PV_2, I_offset_PV_2   |    Spectrolab_UTJ_10.png
                                                 -1.0, 0.0,  # V_offset_IV_3, I_offset_IV_3   |    Spectrolab_UTJ_11.png
                                                 -1.0, 0.1)  # V_offset_PV_3, I_offset_PV_3   |    Spectrolab_UTJ_12.png

