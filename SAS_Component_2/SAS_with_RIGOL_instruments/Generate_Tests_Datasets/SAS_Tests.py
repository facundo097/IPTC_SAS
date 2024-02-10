import PV_Model as PVM
import time

def identify_MPP_for_a_given_range_of_G_T_or_Ang(file_name, variable, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv, N_s, N_p):
    V_start = 0
    if variable == "G":
        G = 100
        while G <= 1375:
            n, I_ph, I_o, R_s, R_sh = PVM.Scale_Parameters(G, T_c_ref, 54.7, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g)
            V_arr, I_arr, P_arr, R_arr = PVM.calculate_curve_arrays(V_start, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref, N_s, N_p)
            V_mp, I_mp, P_mp, R_mp, MPP_index = PVM.find_MPP(V_arr, I_arr, P_arr)
            time.sleep(0.1)
            V_arr.clear()
            I_arr.clear()
            P_arr.clear()
            PVM.write_MPP_in_csv(file_name, variable, G, V_mp, I_mp, P_mp, R_mp)
            G += 25

    elif variable == "T_c":
        T_c = -80
        while T_c <= 80:
            n, I_ph, I_o, R_s, R_sh = PVM.Scale_Parameters(G_ref, T_c, 54.7, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g)
            V_arr, I_arr, P_arr, R_arr = PVM.calculate_curve_arrays(V_start, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref, N_s, N_p)
            V_mp, I_mp, P_mp, R_mp, MPP_index = PVM.find_MPP(V_arr, I_arr, P_arr)
            time.sleep(0.1)
            V_arr.clear()
            I_arr.clear()
            P_arr.clear()
            PVM.write_MPP_in_csv(file_name, variable, T_c, V_mp, I_mp, P_mp, R_mp)
            T_c += 5

    elif variable == "Ang_Deg":
        Ang_Deg = 0
        while Ang_Deg <= 87.5:
            n, I_ph, I_o, R_s, R_sh = PVM.Scale_Parameters(G_ref, T_c_ref, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g)
            V_arr, I_arr, P_arr, R_arr = PVM.calculate_curve_arrays(V_start, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref, N_s, N_p)
            V_mp, I_mp, P_mp, R_mp, MPP_index = PVM.find_MPP(V_arr, I_arr, P_arr)
            time.sleep(0.1)
            V_arr.clear()
            I_arr.clear()
            P_arr.clear()
            PVM.write_MPP_in_csv(file_name, variable, Ang_Deg, V_mp, I_mp, P_mp, R_mp)
            Ang_Deg += 2.5


def get_data_set(V_start, N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv):
    file_name = PV_name + "_datasets_for_array_" + str(N_s) + "x" + str(N_p) + ".csv"
    n, I_ph, I_o, R_s, R_sh = PVM.Scale_Parameters(G_ref, T_c_ref, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g)
    V_arr, I_arr, P_arr, R_arr = PVM.calculate_curve_arrays(V_start, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref, N_s, N_p)
    V_mp, I_mp, P_mp, R_mp, MPP_index = PVM.find_MPP(V_arr, I_arr, P_arr)
    reduced_V_arr, reduced_I_arr, reduced_P_arr, reduced_R_arr = PVM.reduce_points_in_curve(V_arr, I_arr, P_arr, R_arr, MPP_index)
    PVM.write_array_dataset_in_csv(file_name, reduced_V_arr, reduced_I_arr, reduced_P_arr, reduced_R_arr)
    print("Dataset of array" + str(N_s) + "x" + str(N_p) + " written")

def get_datasets_for_all_array_sizes(PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv):
    # Minimum voltage values in which the equipment is stable. Determined experimentally.
    if PV_name == "AZUR_3G30A":
        V_start = [1.38, 1.37, 1.36, 1.37, 1.36, 1.36, 1.36]
    elif PV_name == "AZUR_4G32C":
        V_start = [1.36, 1.34, 1.34, 1.34, 1.34, 1.35, 1.35]
    elif PV_name == "CESI_CTJ30":
        V_start = [1.35, 1.34, 1.35, 1.34, 1.34, 1.34, 1.36]
    elif PV_name == "Spectrolab_UTJ":
        V_start = [1.35, 1.35, 1.35, 1.35, 1.34, 1.35, 1.35]
    else:
        V_start = [0, 0, 0, 0, 0, 0, 0]
    N_s = 1
    N_p = 1
    get_data_set(V_start[0], N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)

    N_s = 1
    N_p = 2
    get_data_set(V_start[1], N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)

    N_s = 2
    N_p = 1
    get_data_set(V_start[2], N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)

    N_s = 2
    N_p = 2
    get_data_set(V_start[3], N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)

    N_s = 2
    N_p = 3
    get_data_set(V_start[4], N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)

    N_s = 1
    N_p = 6
    get_data_set(V_start[5], N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)

    N_s = 6
    N_p = 1
    get_data_set(V_start[6], N_s, N_p, PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)