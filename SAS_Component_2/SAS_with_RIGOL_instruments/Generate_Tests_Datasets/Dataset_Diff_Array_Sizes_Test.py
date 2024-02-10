import SAS_Tests as test
import Google_Sheets as gs
from Secrets import GAS_ID_CONTROL_PANEL

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


google_message = gs.read_google_sheets_message(GAS_ID_CONTROL_PANEL)
print("Google Sheets message: ", google_message)

if google_message != "0":
    input_params, panel_params = gs.extract_params(google_message)
    Start, PV, N_s, N_p, G, T_c, Ang_Deg, CV, CVV = gs.parse_input_params(input_params)
    T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s_pv, K_v, K_i, E_g, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref = gs.parse_panel_params(panel_params)
    if PV == 1:
        PV_name = "AZUR_3G30A"
    elif PV == 2:
        PV_name = "AZUR_4G32C"
    elif PV == 3:
        PV_name = "CESI_CTJ30"
    elif PV == 4:
        PV_name = "Spectrolab_UTJ"
    else:
        PV_name = "New_Panel"
    print("Solar panel: ", PV_name)
    print("Panel datasheet: ", T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s_pv, K_v, K_i, E_g, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref)
    test.get_datasets_for_all_array_sizes(PV_name, G_ref, T_c_ref, Ang_Deg, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, N_s_pv)

else:
    print("Invalid Google message")


