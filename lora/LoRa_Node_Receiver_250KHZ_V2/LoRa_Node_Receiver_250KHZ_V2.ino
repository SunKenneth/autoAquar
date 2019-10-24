#include "SPI.h"
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

#define NUMFLAKES 10
#define XPOS 0
#define YPOS 1
#define DELTAY 2

String istring;
void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3c); 
  Serial.begin(9600);
  display.display();
 // while (!Serial);
  Serial.println(F("LoRa Receiver"));
 // LoRa.setTxPower(17);

  if (!LoRa.begin(915E6)) {
    Serial.println(F("Starting LoRa failed!"));
    while (1);
  }
  // Bandwidth
  LoRa.setSignalBandwidth(250E3); 
  delay(100);  
  Serial.println(F("MiniLoRa")); 
  display.clearDisplay(); 
  display.display();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.println(F("MiniLoRa")); 
  display.println(F("Staring."));
  display.display(); 
  delay(5000);
}

void loop() {
  display.clearDisplay(); 
  istring="";
  char c;
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet

  Serial.print(F("Received packet, "));
  long rssi = LoRa.packetRssi();
   Serial.print(F("RSSI : "));
   Serial.println(rssi);
    display.setTextSize(2);
    display.setCursor(0,0);
    display.print(F("RSSI:"));
    display.println(rssi);
  //  display.println("");
  //  display.println("");
    // read packet
    while (LoRa.available()) {
       c= LoRa.read();
      istring=istring+c;
    }
    Serial.println(istring);
    display.setTextSize(1);
    display.println(istring);
    display.display();   
    delay(1);
  }
}
