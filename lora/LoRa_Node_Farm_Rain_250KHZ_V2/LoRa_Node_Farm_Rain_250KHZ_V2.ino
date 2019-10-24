#include <SPI.h>
#include <LoRa.h>

#include "DHT.h"
#define DHTPIN 4     // what pin we're connected to
#define DHTTYPE DHT11   // DHT 11 
DHT dht(DHTPIN, DHTTYPE);
float t = 0.00;
float h = 0.00;
int MosituresensorPin = A0;    // select the input pin for the potentiometer
int MositureValue = 0;
int LightsensorPin = A3;    // select the input pin for the potentiometer
int LightValue = 0;
//int RainsensorPin = A2;    // select the input pin for the potentiometer
//int RainValue = 0;

const int LoRa_Ready_LED = 3;  //LoRa Ready status
const int LoRa_Trans_LED = 5;  // LoRa Transmion status

#define LoRaID 99

int retval;
#define DEBUG true

