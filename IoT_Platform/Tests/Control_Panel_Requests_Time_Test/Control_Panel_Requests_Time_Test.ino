// PuTTy was used to to log the serial monitor's outputs in a .txt file

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>

const char* ssid = "FamiliaMS";
const char* password = "familia4232";

String GAS_ID_CONTROL_PANEL = "type-gas-id"; 
String google_message = "";

const unsigned long requestInterval = 8000; // Interval between requests in milliseconds
unsigned long startTime = 0;  
unsigned long elapsedTime = 0;
int counter = 1;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(10);
  // Connect to Wi-Fi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void loop() {
  read_google_sheets_message();
  Serial.print(counter);
  Serial.print(";");
  Serial.print(elapsedTime);
  Serial.print(";");
  Serial.println(google_message);
  counter++;
  delay(10000);
}


void read_google_sheets_message(){ 
  std::unique_ptr<BearSSL::WiFiClientSecure>client(new BearSSL::WiFiClientSecure);
  client->setInsecure();
  HTTPClient https;
  String url="https://script.google.com/macros/s/"+GAS_ID_CONTROL_PANEL+"/exec?action=readA1";
  startTime = millis();  
  https.begin(*client, url.c_str());   
  https.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS); //Removes the error "302 Moved Temporarily Error"   
  int httpCode = https.GET(); //Get the returning HTTP status code   
  String payload = https.getString(); //reading data comming from Google Sheet
  if(httpCode == 200){
      google_message = payload; 
  }       
  https.end();
  elapsedTime = millis() - startTime;
}