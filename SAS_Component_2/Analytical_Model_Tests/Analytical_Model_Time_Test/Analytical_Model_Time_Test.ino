// This program randomly changes the inputs so that the model has to calculate 
// a new operational point everytime

#include <SPI.h>
#include <SD.h>
#include <LiquidCrystal_I2C.h>  

//LCD display Config
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Define the chip select pin for the SD card module
const int chipSelect = 10;

// File name
const char* fileName = "data.txt";

// Inputs sent by the MCU_S2
int N_s = 2;        // Number of rows in the solar array (Ns) || I03
int N_p = 3;        // Number of columns in the solar array (Np)|| I04
float G = 0;      // Irradiance || I05
float T_c = 0;      // Temperature of the cell || I06
float Ang_Deg = 0;      // Incidence angle || I07
int CV = 0;        // Control variable || I08
float CVV = 0;      // Control variable value || I09

// Outputs that will be stored in both the local and cloud data bases
float V_out_calc = 0;      // Voltage output calculated
float I_out_calc = 0;      // Current output calculated

// Solar panel parameters at reference conditions sent by the MCU_S2
float T_c_ref = 28;  // Cell temperature at ref. conditions
float G_ref = 1367;    // Solar irradiance at ref. conditions
float V_oc = 2.699;     // Open Circuit Voltage
float I_sc = 0.496;     // Short Circuit Current
float V_mp = 2.387;     // MPP Voltage
float I_mp = 0.487;     // MPP Current
float P_mp = 1.162;     // MPP Power
int N_s_pv = 2;     // Number of cells in series (in a single solar panel)
float K_v = -6.20E-03;      // Voc temperature coefficient
float K_i = 3.60E-04;      // Isc temperature coefficient
float E_g = 1.6;      // Band gap
float n = 1.23;        // Diode ideality factor
double I_ph = 0;     // Photoelectric current
double I_o = 0;      // Diode inverse saturation current
double R_s = 0;      // Series resistance
double R_sh = 0;     // Shunt resistance
double I_ph_ref = 0.496;     // Photoelectric current
double I_o_ref = 9.44E-38;      // Diode inverse saturation current
double R_s_ref = 0.3555;      // Series resistance
double R_sh_ref = 996.98;     // Shunt resistance

// Constants
double k = 1.38064852E-23;  // Boltzmann constant
double q = 1.60217662E-19;  // Electron charge

int header_written = 0;
unsigned long excec_time = 0;
unsigned long excec_time_start = 0;


void setup() {
  randomSeed(analogRead(0));

  // LCD display setup
  lcd.clear();
  lcd.init();
  lcd.backlight();  // Turn on the backlight

  // Initialize SD card
  if (!SD.begin(chipSelect)) {
    lcd.setCursor(0, 0); // Set the cursor to the first row, first column
    lcd.print("SD Failed!");
  } else {
    lcd.setCursor(0, 0); // Set the cursor to the first row, first column
    lcd.print("SD Success!");
  }
  delay(2000);
}

void loop() {
  CVV = 2.0 + random(3000) / 1000.0; // Generates a random float between 2 and 5
  G = random(1176) + 200; // Generates a random integer between 200 and 1375
  T_c = random(161) - 80;    // Generates a random integer between -80 and 80
  Ang_Deg = random(86);    // Generates a random integer between 0 and 85
  delay(1000);
  Analytical_Model(G, T_c, Ang_Deg, G_ref, T_c_ref, V_oc, I_sc, K_v, K_i, N_s_pv, n, I_ph_ref, I_o_ref, R_s_ref, R_sh_ref, E_g, CV, CVV);
  delay(1000);
  writeData();
  lcd.clear();
  lcd.setCursor(0, 0); // Set the cursor to the first row, first column
  lcd.print(excec_time);lcd.print(" ");lcd.print(CVV);lcd.print(" ");lcd.print(G);
  lcd.setCursor(0, 1); // Set the cursor to the first row, first column
  lcd.print(T_c);lcd.print(" ");lcd.print(Ang_Deg);
  delay(1000);
}

void Analytical_Model(float G, float T_c, float Ang_Deg, float G_ref, float T_c_ref, float V_oc, float I_sc, float K_v, float K_i, int N_s_pv, float n, double I_ph_ref, double I_o_ref, double R_s_ref, double R_sh_ref, float E_g, int CV, float CVV){
  excec_time_start = millis();
  if(N_s != 1 || N_p != 1){
    if(CV == 0){
      CVV = CVV / N_s;
    } 
    else {
      CVV = CVV / N_p; 
    }
  }
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
  excec_time = millis() - excec_time_start;
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

void writeData() {
  // Open the data file
  File dataFile = SD.open(fileName, FILE_WRITE);
  if (dataFile) {
    if(header_written == 0){
      dataFile.println("t,V,I,G,Ang");
      header_written = 1;
    }
    dataFile.print(excec_time);dataFile.print(",");
    dataFile.print(V_out_calc);dataFile.print(",");
    dataFile.print(I_out_calc);dataFile.print(",");
    dataFile.print(G);dataFile.print(",");
    dataFile.print(T_c);dataFile.print(",");
    dataFile.println(Ang_Deg);
    dataFile.close();
  } 
}
