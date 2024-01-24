import requests

def read_google_sheets_message(GAS_ID_CONTROL_PANEL):
    url = "https://script.google.com/macros/s/" + GAS_ID_CONTROL_PANEL + "/exec?action=readA1"

    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Retrieve the data from the response
        payload = response.text
        return payload
    else:
        # Handle the error
        print("Failed to retrieve data from Google Sheets. Status code:", response.status_code)
        return None

def send_to_google_sheets(GAS_ID_DATA_BASE,PV,N_s,N_p,G,T_c,Ang_Deg,CV,V_out_calc,V_out_meas,I_out_calc,I_out_meas,P_out_calc,P_out_meas,R_out_calc,R_out_meas,Err_V,Err_I,Err_P,Err_R,n,I_ph,I_o,R_s,R_sh,supply_mode,correction_time):
    url = f"https://script.google.com/macros/s/{GAS_ID_DATA_BASE}/exec?"
    url += f"I02={PV}&I03={N_s}&I04={N_p}&I05={G}&I06={T_c}&I07={Ang_Deg}&I08={CV}"
    url += f"&Q01={V_out_calc}&Q02={V_out_meas}&Q03={I_out_calc}&Q04={I_out_meas}"
    url += f"&Q05={P_out_calc}&Q06={P_out_meas}&Q07={R_out_calc}&Q08={R_out_meas}"
    url += f"&Q09={Err_V}&Q10={Err_I}&Q11={Err_P}&Q12={Err_R}"
    url += f"&Q13={n}&Q14={I_ph}&Q15={I_o}&Q16={R_s}&Q17={R_sh}"
    url += f"&Q18={supply_mode}&Q19={correction_time}"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        print("Data sent to Google Sheets successfully")
    else:
        print("Failed to send data to Google Sheets")

def send_to_google_sheets_short(GAS_ID_DATA_BASE,PV,N_s,N_p,G,T_c,Ang_Deg,CV,V_out_calc,V_out_meas,I_out_calc,I_out_meas,P_out_calc,P_out_meas,R_out_calc,R_out_meas,Err_V,Err_I,Err_P,Err_R,n,I_ph,I_o,R_s,R_sh,supply_mode,correction_time):
    url = f"https://script.google.com/macros/s/{GAS_ID_DATA_BASE}/exec?"
    url += f"I02={PV}&I03={N_s}&I04={N_p}&I05={G}&I06={T_c}&I07={Ang_Deg}&I08={CV}"
    url += f"&Q01={V_out_calc}&Q02={V_out_meas}&Q03={I_out_calc}&Q04={I_out_meas}"
    url += f"&Q06={P_out_meas}&Q08={R_out_meas}"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        print("Data sent to Google Sheets successfully")
    else:
        print("Failed to send data to Google Sheets")

def send_to_google_sheets_long(GAS_ID_DATA_BASE,PV,N_s,N_p,G,T_c,Ang_Deg,CV,V_out_calc,V_out_meas,I_out_calc,I_out_meas,P_out_calc,P_out_meas,R_out_calc,R_out_meas,Err_V,Err_I,Err_P,Err_R,n,I_ph,I_o,R_s,R_sh,supply_mode,correction_time):
    url = f"https://script.google.com/macros/s/{GAS_ID_DATA_BASE}/exec?"
    url += f"I02={PV}&I03={N_s}&I04={N_p}&I05={G}&I06={T_c}&I07={Ang_Deg}&I08={CV}"
    url += f"&Q01={V_out_calc}&Q02={V_out_meas}&Q03={I_out_calc}&Q04={I_out_meas}"
    url += f"&Q06={P_out_meas}&Q08={R_out_meas}"
    url += f"&Q13={n}&Q14={I_ph}&Q15={I_o}&Q16={R_s}&Q17={R_sh}"
    url += f"&Q18={supply_mode}&Q19={correction_time}"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        print("Data sent to Google Sheets successfully")
    else:
        print("Failed to send data to Google Sheets")

def extract_params(google_message):
    # Find the index where input_params starts and ends
    start_index = google_message.find("i,") + 2
    end_index = google_message.find(",d")

    # Extract input_params
    input_params = google_message[start_index:end_index]

    # Find the index where panel_params starts
    panel_start_index = google_message.find("d,") + 2

    # Extract panel_params
    panel_params = google_message[panel_start_index:]

    # Remove "d," and "p," from panel_params
    panel_params = panel_params.replace("d,", "").replace("p,", "")

    return input_params, panel_params

def parse_input_params(input_params):
    values = input_params.split(',')
    Start, PV, N_s, N_p, G, T_c, Ang_Deg, CV, CVV = map(float, values)
    return Start, PV, N_s, N_p, G, T_c, Ang_Deg, CV, CVV

def parse_panel_params(panel_params):
    values = panel_params.split(',')
    T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s_pv, K_v, K_i, E_g, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref = map(float, values)
    return T_c_ref, G_ref, V_oc, I_sc, V_mp, I_mp, P_mp, N_s_pv, K_v, K_i, E_g, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref