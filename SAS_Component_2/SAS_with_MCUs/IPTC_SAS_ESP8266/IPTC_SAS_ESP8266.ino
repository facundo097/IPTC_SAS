#include "Secrets.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>
#include <math.h>
String sci_notation;
double Test;
int power = 0;


// Inputs sent from the Google Sheets control panel
int Start = 0;     // 1 = Start, 0 = Stop
int PV = 0;     // Solar panel
int N_s = 0;     // Number of rows in the solar array (Ns)
int N_p = 0;     // Number of columns in the solar array (Np)
float G = 0;   // Irradiance
float T_c = 0;   // Temperature of the cell
float Ang_Deg = 0;   // Incidence angle
int CV = 0;     // Control variable
float CVV = 0;   // Control variable value

// Outputs sent from MCU_M
float V_out_calc = 0;   // Voltage output calculated
float V_out_meas = 0;   // Voltage output sensed
float I_out_calc = 0;   // Current output calculated
float I_out_meas = 0;   // Current output sensed
float P_out_calc = 0;   // Power output calculated
float P_out_meas = 0;   // Power output sensed
float Err_V = 0;
float Err_I = 0;
float Err_P = 0;
float n = 0;   // Diode Ideality factor
float I_ph = 0;   // Photoelectric current
float I_o = 0;   // Diode Saturation current
float R_s = 0;   // Series resistance
float R_sh = 0;   // Shunt resistance

// Variables to manage how often the control panel is checked
int update_delay = 1; // seconds
int count = 0;
int count_read = 0;

// Google Sheets config
String MCU_M_message = "";
String google_message = "";
String output_message = "";
String last_message = "";

String input_params = "";
String datasheet_params = "";
String five_params = "";

String waiting_i = "";
String waiting_d = "";
String waiting_p = "";
String waiting_r = "";

int parse_full_message = 0;
int last_panel = 0;

String date_time = "t,1,1,00,0,0,0";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(500);

  WiFi.begin();
  delay(1000);  // Delay to allow the module to initialize

  // Scan for available networks
  int numNetworks = WiFi.scanNetworks();
  for (int i = 0; i < numNetworks; i++) {
    String currentSSID = WiFi.SSID(i);
    if (currentSSID == ssid_1) {
      ssid = ssid_1;
      password = password_1;
      break;
    } else if (currentSSID == ssid_2) {
      ssid = ssid_2;
      password = password_2;
      break;
    }
  }
  delay(100);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
  }
  delay(500);
  // Get date and time
  read_google_sheets_message("A2");
  delay(1000);
  while (count <= 50) { // Print for 5 seconds
    Serial.println(date_time);
    count++;
    delay(100);
  }
  count = 0;
}

int update_outputs_counter = 0;
String outputs_variables = "";

void loop() {
  if (update_outputs_counter == 1) {
    update_outputs_counter = 0;
    outputs_variables = "";
    while (outputs_variables == ""){
      if (Serial.available()) {
        MCU_M_message = Serial.readStringUntil('\n'); // Read the message until a newline character is received
        if (MCU_M_message.charAt(0) == 'o') {
          outputs_variables = MCU_M_message;
          parse_output_variables(outputs_variables); // Process the message to assign the values of the output variables 
          delay(50);
        }
      }
    }
  }

  if (count_read == 5){
    count_read = 0;
    read_google_sheets_message("A1"); // assigns value to google_message
  }
  if(google_message!="0" && google_message != last_message){
    last_message = google_message;
    PV = google_message.charAt(4) - '0';
    if (PV != last_panel){
      parse_full_message = 1;
      last_panel = PV;
    }
    split_google_sheets_message(google_message);
  }
  
  Start = google_message.charAt(2) - '0';
  if(count == update_delay){
    if(Start == 1){
      parse_input_variables(input_params);
      if (Err_P > 0) {
        Err_P = 100 * abs(P_out_calc - P_out_meas) / P_out_calc;
      }
      if (Err_P < 5){
        send_to_google_sheets();
      }
    }
    count = 0;    
  }
  count_read++;
  count++;
  update_outputs_counter++;
  delay(100);
}

void send_messages_sequence() {
  if (parse_full_message == 0){ // send only input_params

    while (output_message.charAt(0) != 'c'){ // sends input_params until MCU_M sends "c", meaning it already received the input_params
      while(waiting_r.charAt(0) != 'r'){ // sends "s" until MCU_M sends "r", meaning it is ready to receive input_params
        Serial.println("s");
        if (Serial.available()) {
          waiting_r = Serial.readStringUntil('\n'); // Read the message until a newline character is received
        }
        delay(200);
      }

      Serial.println(input_params);
      if (Serial.available()) {
          output_message = Serial.readStringUntil('\n'); 
      }
      //Serial.println("waiting for 'c'...");
      delay(250);
    }
    output_message = "";
    waiting_r = "";
  }

  else if (parse_full_message == 1){ // send all params

    while (output_message.charAt(0) != 'c'){  // ends only when MCU_M confirms all data was received

      while(waiting_r.charAt(0) != 'r'){ // sends "a" until MCU_M sends "r", meaning it is ready to receive all parameters
        Serial.println("a");
        if (Serial.available()) {
          waiting_r = Serial.readStringUntil('\n'); 
        }
        delay(250);
      }

      while(waiting_i.charAt(0) != 'i'){ // sends input_params until MCU_M sends "i", meaning it already received the input_params
        Serial.println(input_params);
        if (Serial.available()) {
          waiting_i = Serial.readStringUntil('\n'); 
        }
        delay(250);
      }

      while(waiting_d.charAt(0) != 'd'){ // sends datasheet_params until MCU_M sends "d", meaning it already received the datasheet_params
        Serial.println(datasheet_params);
        if (Serial.available()) {
          waiting_d = Serial.readStringUntil('\n'); 
        }
        delay(250);
      }

      while(waiting_p.charAt(0) != 'p'){ // sends five_params until MCU_M sends "p", meaning it already received the five_params
        Serial.println(five_params);
        if (Serial.available()) {
          waiting_p = Serial.readStringUntil('\n'); 
        }
        delay(250);
      }

      if (Serial.available()) {
          output_message = Serial.readStringUntil('\n'); 
      }

      //Serial.println("waiting for 'c'...");
      delay(250);
    }
    waiting_i = "";
    waiting_d = "";
    waiting_p = "";
    waiting_r = "";
    output_message = "";
  }

  //Serial.println("'c' received!");
}

void split_google_sheets_message(String google_message) {
  // Find the position of 'd' and 'p' in the message
  int d_pos = google_message.indexOf("d");
  int p_pos = google_message.indexOf("p");
  // Extract input_params
  input_params = google_message.substring(google_message.indexOf("i"), d_pos - 1); 
  if (parse_full_message == 1) {
    // Extract datasheet_params
    datasheet_params = google_message.substring(d_pos, p_pos - 1);    
    // Extract five_params
    five_params = google_message.substring(p_pos);
    //Serial.println(datasheet_params); 
    //Serial.println(five_params);
  }
  //Serial.println(input_params);
  send_messages_sequence();
  parse_full_message = 0;
}

void parse_input_variables(String input_message) {
  input_message = input_message.substring(2);
  // Split the input message by commas
  int index = 0;
  String value = "";
  
  for (int i = 0; i < input_message.length(); i++) {
    char c = input_message.charAt(i);
    if (c == ',') {
      // Convert the value to the appropriate data type and assign it to the respective variable
      if (index == 0) {
        Start = value.toInt();
      } else if (index == 1) {
        PV = value.toInt();
      } else if (index == 2) {
        N_s = value.toInt();
      } else if (index == 3) {
        N_p = value.toInt();
      } else if (index == 4) {
        G = value.toFloat();
      } else if (index == 5) {
        T_c = value.toFloat();
      } else if (index == 6) {
        Ang_Deg = value.toFloat();
      } else if (index == 7) {
        CV = value.toInt();
      } else if (index == 8) {
        CVV = value.toFloat();
      }
      
      // Reset the value and move to the next variable
      value = "";
      index++;
    } else {
      value += c;
    }
  }
  
  // Handle the last value after the final comma
  if (index == 8) {
    CVV = value.toFloat();
  }
}


void parse_output_variables(String output_message) {
  output_message = output_message.substring(2);
  // Split the input string by commas to get individual values
  int currentIndex = 0;
  int lastIndex = 0;
  for (int i = 0; i < 11; i++) {
    // Find the position of the next comma
    currentIndex = output_message.indexOf(',', lastIndex);    
    // Extract the substring between the last index and the current comma
    String value = output_message.substring(lastIndex, currentIndex);    
    // Convert the substring to a float and assign it to the respective variable
    if (i == 0) {
      V_out_calc = value.toFloat();
    } else if (i == 1) {
      V_out_meas = value.toFloat();
    } else if (i == 2) {
      I_out_calc = value.toFloat();
    } else if (i == 3) {
      I_out_meas = value.toFloat();
    } else if (i == 4) {
      P_out_calc = value.toFloat();
    } else if (i == 5) {
      P_out_meas = value.toFloat();
    } else if (i == 6) {
      n = value.toFloat();
    } else if (i == 7) {
      I_ph = value.toFloat();
    } else if (i == 8) {
      I_o = value.toFloat();
    } else if (i == 9) {
      R_s = value.toFloat();
    } else if (i == 10) {
      R_sh = value.toFloat();
    }
    // Update the lastIndex to the next character
    lastIndex = currentIndex + 1;
  }
}


void send_to_google_sheets() {
  find_sci_notation(I_o);
  std::unique_ptr<BearSSL::WiFiClientSecure>client(new BearSSL::WiFiClientSecure);
  client->setInsecure();
  HTTPClient https;
  String url = "https://script.google.com/macros/s/" + GAS_ID_DATA_BASE + "/exec?I02=" + String(PV, DEC) + "&I03=" + String(N_s, DEC) + "&I04=" + String(N_p, DEC);
  url += "&I05=" + String(G, DEC) + "&I06=" + String(T_c, DEC) + "&I07=" + String(Ang_Deg, DEC) + "&I08=" + String(CV, DEC) + "&Q01=" + String(V_out_calc, 6) + "&Q02=" + String(V_out_meas, 6);
  url += "&Q03=" + String(I_out_calc, 6) + "&Q04=" + String(I_out_meas, 6) + "&Q05=" + String(P_out_calc, 6) + "&Q06=" + String(P_out_meas, 6) + "&Q07=" + String(n, DEC);
  url += "&Q08=" + String(I_ph, 6) + "&Q09=" + sci_notation + "&Q10=" + String(R_s, 6) + "&Q11=" + String(R_sh, 6);
  https.begin(*client, url.c_str());    
  int httpCode = https.GET(); //Get the returning HTTP status code   
  /*if(httpCode <= 0){
    // PONER ACÁ ERRORES DE LED
    https.end(); 
    return;}*/	 
  https.end();  
  //Serial.println(url);
}

void read_google_sheets_message(String cell){   
  std::unique_ptr<BearSSL::WiFiClientSecure>client(new BearSSL::WiFiClientSecure);
  client->setInsecure();
  HTTPClient https;
  String url="https://script.google.com/macros/s/"+GAS_ID_CONTROL_PANEL+"/exec?action=read"+cell;
  https.begin(*client, url.c_str());   
  https.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS); //Removes the error "302 Moved Temporarily Error"   
  int httpCode = https.GET(); //Get the returning HTTP status code   
  /*if(httpCode <= 0){
    // PONER ACÁ ERRORES DE LED
    https.end(); 
    return;}*/
  if (cell == "A1"){
    String payload = https.getString(); //reading data comming from Google Sheet   
    if(httpCode == 200){
      google_message = payload; 
    } 
  }      
  if (cell == "A2"){
    String payload_date_time = https.getString(); //reading data comming from Google Sheet   
    if(httpCode == 200){
      date_time = payload_date_time; 
    } 
  }
  https.end();
}

void find_sci_notation(double input){
  String StrTest = "0";
  power = 1;
  while (StrTest.charAt(0) == '0'){
    Test = input * pow(10, power);
    StrTest = String(Test,10);
    power++;
  }
  power--;
  sci_notation = String(Test) + "E-" + String(power);
}