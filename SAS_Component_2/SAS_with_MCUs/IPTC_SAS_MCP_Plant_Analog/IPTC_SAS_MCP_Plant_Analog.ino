// Initialize variables outside the loop
float V_out = 0.0;
float I_out = 0.0;
bool first_message_received = 0;

void setup() {
  Serial.begin(9600); // Set the baud rate to match your communication speed
}

void loop() {
  // Read the UART data
  String receivedData = readUART();
  if (receivedData.length() > 3){
    // Parse the received data
    parseData(receivedData, V_out, I_out);
    first_message_received = 1;
  }

  if (first_message_received == 1){
    // Calculate 0.0001% of V_out and I_out
    float onePercentV = 0.0001 * V_out;
    float onePercentI = 0.0001 * I_out;

    // Generate random numbers between 0 and 1% of V_out and I_out
    float randomV = randomFloat(-onePercentV, onePercentV);
    float randomI = randomFloat(-onePercentI, onePercentI);

    // Add or subtract the random numbers
    V_out += randomV;
    I_out += randomI;

    // Calculate P_out
    float P_out = V_out * I_out;

    // Print the results
    Serial.print(V_out, 5); // Print with 3 decimal places
    Serial.print(",");
    Serial.println(I_out, 5); // Print with 3 decimal places  
  }
  delay(1000); // Adjust the delay based on your application's requirements
}

String readUART() {
  String data = "";
  while (Serial.available() > 0) {
    char incomingChar = Serial.read();
    if (incomingChar == '\n') {
      break;
    }
    data += incomingChar;
  }
  return data;
}

void parseData(String data, float& V_out, float& I_out) {
  int commaIndex = data.indexOf(',');
  if (commaIndex != -1) {
    V_out = data.substring(0, commaIndex).toFloat();
    I_out = data.substring(commaIndex + 1).toFloat();
  } // If parsing fails, retain the previous values
}

float randomFloat(float min, float max) {
  return min + static_cast<float>(rand()) / RAND_MAX * (max - min);
}
