#include <DHT.h>;
#define DHTPIN A5     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);

byte pinWater = A7;
byte pinLight = A6;
byte pinWaterRelay = 7;
byte pinLightRelay = 6;
byte btnWater = 5;
byte btnLight = 4;

int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value

String readCommand() {
  String recv = "";
  String a;
  while (Serial1.available()) {
      a = Serial1.readString(); // read the incoming data as string
      recv = recv + a;
      Serial.print(a);
  }
  Serial.println();
  
  return recv;
}
void setup() {
  pinMode(pinWater, INPUT);
  pinMode(pinLight, INPUT);
  pinMode(pinWaterRelay, OUTPUT);
  pinMode(pinLightRelay, OUTPUT);
  pinMode(btnLight, INPUT);
  pinMode(btnWater, INPUT);  
  dht.begin();

  Serial.begin(115200);
  Serial1.begin(115200);
}

void loop() {
  int valueWater = analogRead(pinWater);
  int valueLight = analogRead(pinLight);
  boolean powerLight = digitalRead(btnLight);
  boolean powerWater = digitalRead(btnWater);  
  Serial.print("Button:"); Serial.print(powerLight); Serial.print("/");Serial.println(powerWater); 
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  Serial.print("[T:" + String(temp) + ":0,");
  Serial.print("H:" + String(hum) + ":0,");
  Serial.print("L:" + String(valueLight) + ":" + String(digitalRead(pinLightRelay)) + ",");
  Serial.println("W:" + String(valueWater) + ":" + String(digitalRead(pinWaterRelay)) + "]");

  Serial1.print("[T:" + String(temp) + ":0,");
  Serial1.print("H:" + String(hum) + ":0,");
  Serial1.print("L:" + String(valueLight) + ":" + String(digitalRead(pinLightRelay)) + ",");
  Serial1.print("W:" + String(valueWater) + ":" + String(digitalRead(pinWaterRelay)) + "]");

  String cmd = readCommand();
  //--> a: power on ligher, b: power off light, c: power on water, d: power off water
  //Check Light command
  if(cmd.indexOf('a')>=0) {
    digitalWrite(pinLightRelay, HIGH);
    Serial.print("Power on the Light.");
  }else if(cmd.indexOf('b')>=0) {
    digitalWrite(pinLightRelay, LOW);
    Serial.print("Power off the Light.");
  }
  //Check Water command
  if(cmd.indexOf('c')>=0) {
    digitalWrite(pinWaterRelay, HIGH);
    Serial.print("Power on the Water.");
  }else if(cmd.indexOf('d')>=0) {
    digitalWrite(pinWaterRelay, LOW);
    Serial.print("Power off the Water.");
  }

  if(powerLight==1) {
    digitalRead(pinLightRelay) ? digitalWrite(pinLightRelay, LOW) : digitalWrite(pinLightRelay, HIGH);

  }

  if(powerWater==1) {
    digitalRead(pinWaterRelay) ? digitalWrite(pinWaterRelay, LOW) : digitalWrite(pinWaterRelay, HIGH);

  }  
 
  delay(500);
}
