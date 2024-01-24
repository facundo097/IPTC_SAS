#include <Arduino.h>
#include <HardwareSerial.h>
#include <SPI.h>
#include <SD.h>
#include <Wire.h>  
#include <LiquidCrystal_I2C.h>  
#include <math.h>
#include <RTClib.h>

// UART communication config
HardwareSerial Serial1(USART1);
HardwareSerial Serial4(USART4);
String PIC_data;
String ESP_data;


// RTC Config
RTC_DS3231 rtc;
bool date_updated = 0;
String string_time;
String string_date;
String string_filename;

/*STM32RTC& rtc = STM32RTC::getInstance();
byte day = 0;
byte month = 0;
byte year = 0;
byte hours = 0;
byte minutes = 0;
byte seconds = 0;
char date_time[20]; 
bool date_updated = 0;
char filename[13];*/

//LCD display Config
LiquidCrystal_I2C lcd(0x27, 16, 2);

// SD Card Config
const int chipSelect = 10;
int header_written = 0;

// Inputs sent by the MCU_S2
int Start = 0;        // 1 = Start, 0 = Stop || I01
int PV = 0;        // Solar panel|| I02
int N_s = 0;        // Number of rows in the solar array (Ns) || I03
int N_p = 0;        // Number of columns in the solar array (Np)|| I04
float G = 0;      // Irradiance || I05
float T_c = 273.15;      // Temperature of the cell || I06
float Ang_Deg = 0;      // Incidence angle || I07
int CV = 0;        // Control variable || I08
float CVV = 0;      // Control variable value || I09
int last_panel = 9; 
int panel_loaded = 0;
String last_message = "zyx";
int changes_applied = 0;

String input_params = "";
String datasheet_params = "";
String five_params = "";

String I_o_sci_notation;
double Test;
int power = 0;

// Outputs sent by the MCU_S1
float V_s = 0;

// Outputs that will be stored in both the local and cloud data bases
float V_out_calc = 0;      // Voltage output calculated
float V_out_meas = 0;      // Voltage output sensed (sent by MCU_S1)
float I_out_calc = 0;      // Current output calculated
float I_out_meas = 0;      // Current output sensed (sent by MCU_S1)
float P_out_calc = 0;      // Power output calculated (V_out_calc*I_out_calc)
float P_out_meas = 0;      // Power output sensed (V_out_meas*I_out_meas)
float Err_V = 0;
float Err_I = 0;
float Err_P = 0;

// Solar panel parameters at reference conditions sent by the MCU_S2
float T_c_ref = 0;  // Cell temperature at ref. conditions
float G_ref = 0;    // Solar irradiance at ref. conditions
float V_oc = 0;     // Open Circuit Voltage
float I_sc = 0;     // Short Circuit Current
float V_mp = 0;     // MPP Voltage
float I_mp = 0;     // MPP Current
float P_mp = 0;     // MPP Power
int N_s_pv = 0;     // Number of cells in series (in a single solar panel)
float K_v = 0;      // Voc temperature coefficient
float K_i = 0;      // Isc temperature coefficient
float E_g = 0;      // Band gap
float n = 0;        // Diode ideality factor
double I_ph = 0;     // Photoelectric current
double I_o = 0;      // Diode inverse saturation current
double R_s = 0;      // Series resistance
double R_sh = 0;     // Shunt resistance
double I_ph_ref = 0;     // Photoelectric current
double I_o_ref = 0;      // Diode inverse saturation current
double R_s_ref = 0;      // Series resistance
double R_sh_ref = 0;     // Shunt resistance


// Constants
double k = 1.38064852E-23;  // Boltzmann constant
double q = 1.60217662E-19;  // Electron charge

int count = 0;
int measured_values_received = 0;
int print_outputs_timer = 0;
int parameters_loaded = 0;

String waiting_r = "";
String ESP_message = "";
String outputs_message = "";


void setup() {
  // UART setup
  Serial1.begin(9600);
  Serial4.begin(115200);

  // RTC setup
  rtc.begin();

  // LCD display setup
  lcd.clear();
  lcd.init();
  lcd.backlight();  // Turn on the backlight
  lcd.setCursor(0, 0); // Set the cursor to the first row, first column
  lcd.print("    Welcome!    ");

  // SD card setup
  SD.begin(chipSelect);

  // Cycle to pudate time and date of the RTC
  while(date_updated == 0){
    //date_updated = 1; // delete this
    if (Serial4.available()) {
      ESP_data = Serial4.readStringUntil('\n');
      if (ESP_data.charAt(0) == 't') {
        set_time(ESP_data);
      }
    }
  }
  delay(1000);
  lcd.clear();
}


void loop() {

  ///////////////////////////////////////////////////////////////////////////////////
  if (Serial4.available()) {
    ESP_data = Serial4.readStringUntil('\n');
    if (ESP_data.charAt(0) == 's'){
      measured_values_received = 0;
      input_params = "";
      Serial4.println("r");
      while (input_params == ""){
        if (Serial4.available()) {
          ESP_data = Serial4.readStringUntil('\n');
          if (ESP_data.charAt(0) == 'i'){
            input_params = ESP_data;
          }
        }
      }
      delay(50);
      Serial4.println("c");
      load_only_inputs(input_params);
      Analytical_Model(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, N_s_pv, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, CV, CVV);
      delay(50);
    }

    else if (ESP_data.charAt(0) == 'a'){
      measured_values_received = 0;
      input_params = "";
      datasheet_params = "";
      five_params = "";
      Serial4.println("r");
      while (input_params == ""){
        if (Serial4.available()) {
          ESP_data = Serial4.readStringUntil('\n');
          if (ESP_data.charAt(0) == 'i'){
            input_params = ESP_data;
            Serial4.println("i");
          }
        }
      }
      while (datasheet_params == ""){
        if (Serial4.available()) {
          ESP_data = Serial4.readStringUntil('\n');
          if (ESP_data.charAt(0) == 'd'){
            datasheet_params = ESP_data;
            Serial4.println("d");
          }
        }
      }
      while (five_params == ""){
        if (Serial4.available()) {
          ESP_data = Serial4.readStringUntil('\n');
          if (ESP_data.charAt(0) == 'p'){
            five_params = ESP_data;
            Serial4.println("p");
          }
        }
      }
      delay(50);
      Serial4.println("c");
      load_inputs_and_panel(input_params, datasheet_params, five_params);
      Analytical_Model(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, N_s_pv, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, CV, CVV);
      delay(50);
    }
    Serial1.println(String(V_out_calc) + "," + String(I_out_calc));
    delay(500);
    parameters_loaded = 1;
  }
  ///////////////////////////////////////////////////////////////////////////////////
  if (Serial1.available()) {
    PIC_data = Serial1.readStringUntil('\n');
    if (PIC_data.length() > 3){
      parse_output_message(PIC_data);
      delay(50);
      measured_values_received = 1;
    }
  }
  //////////////////////////////////////////////////////////////////////////
  if (print_outputs_timer == 20){
    print_outputs_LCD(V_out_meas, I_out_meas, P_out_meas);
    send_outputs_sequence();
    print_outputs_timer = 0;
  }
  print_outputs_timer++;
  delay(50);
}


void send_outputs_sequence(){
  if (Err_V > 0 || Err_I > 0 || Err_P > 0) {
    Err_V = 100 * abs(V_out_calc - V_out_meas) / V_out_calc;
    Err_I = 100 * abs(I_out_calc - I_out_meas) / I_out_calc;
    Err_P = 100 * abs(P_out_calc - P_out_meas) / P_out_calc;
  }
  if (Err_P < 5){
    outputs_message = "o," + String(V_out_calc, 4) + "," + String(V_out_meas, 4) + "," + String(I_out_calc, 4) + "," + String(I_out_meas, 4) + "," + String(P_out_calc, 4) + "," + String(P_out_meas, 4);
    outputs_message += "," + String(n, 2) + "," + String(I_ph, 4) + "," + I_o_sci_notation + "," + String(R_s, 4) + "," + String(R_sh, 2);
    write_to_SD_card();
  }
  delay(50);
  Serial4.println(outputs_message);
}

void load_only_inputs(String input_params){
  parameters_loaded = 0;
  parse_input_params(input_params);
  if(N_s != 1 || N_p != 1){
    if(CV == 0){
      CVV = CVV / N_s;
    } 
    else {
      CVV = CVV / N_p; 
    }
  }
  delay(50);
  Serial1.println(String(V_out_calc)+","+String(I_out_calc));
  delay(50);
  
}

void load_inputs_and_panel(String input_params, String datasheet_params, String five_params){
  parameters_loaded = 0;
  parse_input_params(input_params);
  delay(50);
  if(N_s != 1 || N_p != 1){
    if(CV == 0){
      CVV = CVV / N_s;
    } 
    else {
      CVV = CVV / N_p; 
    }
  }
  parse_datasheet_params(datasheet_params);
  delay(50); 
  parse_five_params(five_params);
  delay(50);
  Serial1.println(String(V_out_calc)+","+String(I_out_calc));
}


void parse_input_params(String input_params) { // Sent by MCU_S2
  input_params = input_params.substring(2);
  // Split the input message by commas
  int index = 0;
  String value = "";  
  for (int i = 0; i < input_params.length(); i++) {
    char c = input_params.charAt(i);
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


void parse_datasheet_params(String datasheet_params) {
  last_panel = PV;
  datasheet_params = datasheet_params.substring(2);
  // Split the string into individual values using the ',' delimiter
  int pos = 0;
  int index = 0;  
  while (datasheet_params.length() > 0) {
    pos = datasheet_params.indexOf(",");
    if (pos == -1) {
      pos = datasheet_params.length();
    }    
    String value_str = datasheet_params.substring(0, pos);
    float value = value_str.toFloat();    
    // Assign the value to the appropriate variable using 'else if' structure
    if (index == 0) T_c_ref = value;
    else if (index == 1) G_ref = value;
    else if (index == 2) V_oc = value;
    else if (index == 3) I_sc = value;
    else if (index == 4) V_mp = value;
    else if (index == 5) I_mp = value;
    else if (index == 6) P_mp = value;
    else if (index == 7) N_s_pv = int(value);
    else if (index == 8) K_v = value;
    else if (index == 9) K_i = value;
    else if (index == 10) E_g = value;
    datasheet_params = datasheet_params.substring(pos + 1);
    index++;
  }
}


void parse_five_params(String five_params) {
  last_panel = PV;
  five_params = five_params.substring(2);
  // Split the string into individual values using the ',' delimiter
  int pos = 0;
  int index = 0;  
  while (five_params.length() > 0) {
    pos = five_params.indexOf(",");
    if (pos == -1) {
      pos = five_params.length();
    }    
    String value_str = five_params.substring(0, pos);
    float value = value_str.toFloat();    
    // Assign the value to the appropriate variable using 'else if' structure
    if (index == 0) n = value;
    else if (index == 1) I_ph_ref = value;
    else if (index == 2) I_o_ref = value;
    else if (index == 3) R_s_ref = value;
    else if (index == 4) R_sh_ref = value;    
    five_params = five_params.substring(pos + 1);
    index++;
  }
}


void parse_output_message(String output_message) { // sent by MCU_S1
  // The message should be something like "V_out,I_out" = "5.24,0.68"
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
      V_out_meas = value.toFloat();
    } else if (i == 1) {
      I_out_meas = value.toFloat();
    } 
    // Update the lastIndex to the next character
    lastIndex = currentIndex + 1;
  }
  P_out_meas = V_out_meas * I_out_meas;
}


void Analytical_Model(float G, float T_c, float Ang_Deg, float G_ref, float T_c_ref, float V_oc, float I_sc, float K_v, float K_i, int N_s_pv, float n, double I_ph_ref, double I_o_ref, double R_s_ref, double R_sh_ref, float E_g, int CV, float CVV){
  n, I_ph, I_o, R_s, R_sh = Scale_Parameters(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g);
  if(CV == 1){ // CVV = Current
    V_out_calc = Solve_for_Voltage(CVV, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c);
    V_out_calc = V_out_calc * N_s; // multiplies by the number of rows in the solar array
    I_out_calc = CVV * N_p; // multiplies by the number of columns in the solar array
  }
  else {      // CVV = Voltage
    I_out_calc = Solve_for_Current(CVV, n, I_o, I_ph, R_s, R_sh, N_s_pv, T_c_ref);
    I_out_calc = I_out_calc * N_p; // multiplies by the number of columns in the solar array
    V_out_calc = CVV * N_s; // multiplies by the number of rows in the solar array;
  }
  P_out_calc = V_out_calc * I_out_calc;
  find_sci_notation(I_o);
}


double Scale_Parameters(float G, float T_c, float Ang_Deg, float G_ref, float T_c_ref, float V_oc, float I_sc, float K_v, float K_i, float n, double I_ph_ref, double I_o_ref, double R_s_ref, double R_sh_ref, float E_g) {
  T_c+=273.15;
  T_c_ref+=273.15;
  double delta_T = (T_c - T_c_ref);
  double Ang_Rad = radians(Ang_Deg);
  double G_new = G * cos(Ang_Rad); // LK03
  double alpha_G = G_new / G_ref;
  R_s = R_s_ref / alpha_G; // PV09
  R_sh = R_sh_ref / alpha_G; // PV04, PV09
  I_ph = alpha_G * (I_ph_ref + K_i * delta_T); // PV04, PV03
  I_o = I_o_ref * pow((T_c / T_c_ref), 3) * exp((E_g * q) / (n * k) * (1 / T_c_ref - 1 / T_c)); // PV11
  return n, I_ph, I_o, R_s, R_sh;
}


double Solve_for_Current(double V, double n, double I_o, double I_ph, double R_s, double R_sh, int N_s_pv, double T_c_ref) {
  T_c+=273.15;
  T_c_ref+=273.15;
  double V_T = (N_s_pv * n * k * T_c_ref) / q;
  double I_guess = 0.0;
  double epsilon = 1e-6; // Tolerance for the root-finding algorithm
  double step = 0.1;     // Initial step size for the root-finding algorithm
  int iteration = 0; // Initialize the iteration counter
  int max_iterations = 1000;
  while (iteration < max_iterations) {
      double exponent = (V + I_guess * R_s) / V_T;
      double clipped_exponent = fmin(fmax(exponent, -700), 700); // Clip the exponent
      double new_I = I_ph - I_o * (exp(clipped_exponent) - 1) - ((V + I_guess * R_s) / R_sh) - I_guess;
      if (fabs(new_I) < epsilon) {
          // The solution is close enough to zero
          return I_guess;
      }
      // Update the guess using the Newton-Raphson method
      double derivative = -I_o * R_s * exp(clipped_exponent) / V_T - R_s / R_sh - 1;
      I_guess = I_guess - new_I / derivative;
      // Limit the step size to avoid overshooting the root
      I_guess = fmax(0, I_guess); // Ensure the current is non-negative
      I_guess = fmin(I_guess, V / R_s); // Limit current to prevent negative voltage across the diode
      iteration++; // Increment the iteration counter
  }
  // If the maximum number of iterations is reached, return a special value (you can choose another value if needed)
  return -1.0; // Or any other value to indicate that the solution was not found within the specified iterations
}


float Solve_for_Voltage(float I, float n, double I_o, double I_ph, double R_s, double R_sh, int N_s_pv, float T_c_ref) {
  T_c+=273.15;
  T_c_ref+=273.15;
  double V_T = (N_s_pv * n * k * T_c_ref) / q;
  double V = 0.0; // Initial guess for voltage
  double epsilon = 1e-6; // Tolerance for convergence
  int max_iterations = 100; // Maximum number of iterations 
  // Newton-Raphson loop
  for (int i = 0; i < max_iterations; i++) {
    double eq = V_T * log((I_ph + I_o - I * (1 + R_s / R_sh) - V / R_sh) / I_o) - I * R_s - V;
    double eq_derivative = -V_T/(I_ph * R_sh + I_o * R_sh - R_s * I - R_sh * I - V) - 1;
    double delta = eq / eq_derivative;   
    V = V - delta;   
    // Check for convergence
    if (fabs(delta) < epsilon) {
      return V;
    }
  } 
  // Return the result after max_iterations if convergence is not achieved
  return V;
}


void set_time(String time_data) {
  // time_data is a string like this: "t,12,1,24,11,39,16" -> d,M,yy,H,m,s
  time_data = time_data.substring(2);
  int values[6];
  int currentIndex = 0;
  String currentToken = "";
  for (int i = 0; i < time_data.length(); i++) {
    char c = time_data.charAt(i);
    if (c == ',') {
      // Convert the currentToken to an integer and store it in the values array
      values[currentIndex] = currentToken.toInt();
      currentIndex++;
      currentToken = ""; // Reset the currentToken
    } else {
      currentToken += c;
    }
  }
  values[currentIndex] = currentToken.toInt();
  rtc.adjust(DateTime(values[2], values[1], values[0], values[3], values[4], values[5])); // comment after setting it for the first time: year, month, day, hour, minute, seconds 
  date_updated = 1;
  DateTime now = rtc.now(); 
  get_date_time_chars(now);
  lcd.setCursor(0, 1); 
  lcd.print(string_date + " " + string_time);
  delay(2000);
  lcd.clear();
  //print_outputs_LCD();
}

void get_date_time_chars(DateTime date) {
  // Update Date + Time
  char char_date[9];
  char filename[13];
  sprintf(char_date, "%02d/%02d/%02d", date.day(), date.month(), date.year()); // date in DD/MM/YY format
  sprintf(filename, "%02d%02d%02d.txt", date.year(), date.month(), date.day()); // file name: "<YY><MM><DD>.txt" 
  char char_time[10] = "hh:mm:ss"; date.toString(char_time); // time in hh:mm:ss format
  string_time = String(char_time);
  string_date = String(char_date);
  string_filename = String(filename);
}


void print_outputs_LCD(float V_out_meas, float I_out_meas, float P_out_meas){
  // Print a message to the LCD
  lcd.clear();
  lcd.setCursor(0, 0); // Set the cursor to the first row, first column
  lcd.print("V=");  // Print your message
  lcd.print(V_out_meas);  // Print your message
  lcd.setCursor(9, 0); // Set the cursor to the first col, first row
  lcd.print("I=");  // Print your message
  lcd.print(I_out_meas);  // Print your message
  lcd.setCursor(4, 1);
  lcd.print("P=");  // Print your message
  lcd.print(P_out_meas);  // Print your message
}


void write_to_SD_card(){
  // Update date and time
  DateTime now = rtc.now(); 
  get_date_time_chars(now);
  char filename[13];
  string_filename.toCharArray(filename, sizeof(filename));
  // Write output in SD card
  File dataFile = SD.open(filename, FILE_WRITE);
  if (dataFile) {
    if(header_written == 0){
      dataFile.println("Date,Time,PV,N_s,N_p,G,T,Ang,CV,V_out_calc,V_out_meas,I_out_calc,I_out_meas,P_out_calc,P_out_meas,Err_V,Err_I,Err_P,n,I_ph,I_o,R_s,R_sh");
      header_written =1;
    }
    dataFile.print(string_date + "," + string_time + "," + String(PV) + "," + String(N_s) + "," + String(N_p) + "," + String(G) + "," + String(T_c-273.15) + "," + String(Ang_Deg) + "," + String(CV) + ","); 
    dataFile.print(String(V_out_calc) + "," + String(V_out_meas) + "," + String(I_out_calc) + "," + String(I_out_meas) + "," + String(P_out_calc) + "," + String(P_out_meas) + ",");
    dataFile.print(String(Err_V) + "," + String(Err_I) + "," + String(Err_P) + ",");
    dataFile.println(String(n) + "," + String(I_ph) + "," + I_o_sci_notation + "," + String(R_s) + "," + String(R_sh));
    dataFile.close();
  }
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
  I_o_sci_notation = String(Test) + "E-" + String(power);
}

