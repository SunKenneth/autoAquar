void LoRa_init()
{
  if (!LoRa.begin(915E6)) {
    Serial.println(F("Starting LoRa failed!"));
    digitalWrite(LoRa_Ready_LED,LOW);
    while (1);
  }
    // Bandwidth
    LoRa.setSignalBandwidth(250E3); 
    //LoRa.setSpreadingFactor(8); 
    //delay(100);
    Serial.println(F("Starting LoRa OK!"));
    digitalWrite(LoRa_Ready_LED,HIGH);
}

void Mini_LoRa_Transmit()
{
  Serial.println(F("LoRa Send data...250KHZ.."));
/*
  char comma = char(44) ;   // ,
  char mark = char(58) ;   // :
  char Lsqm = char(123) ; // {
  char Rsqm = char(125) ; // } 
  char sqm = char(34) ;   // "
  char lf = char(13) ;   // \n
*/
  String comma = "," ;    
  String mark = ":" ;    
  String Lsqm = "{" ;  
  String Rsqm = "}" ;  
  String sqm ="\"" ;   // "
  char lf = char(13) ;   // \n

// JSON format 
  String Sending ="";
  Sending = Lsqm + sqm + "ID" + sqm + mark + LoRaID + comma+  sqm + "Temp" + sqm +mark +String(t) + comma + sqm +"Humi" + sqm +mark +String(h)
   + comma+  sqm + "Mositure" + sqm +mark +String(MositureValue)+ comma+  sqm + "Light" + sqm +mark +String(LightValue)
   //+ comma+  sqm + "Rain" + sqm +mark +String(RainValue) 
   + Rsqm  +"\r"+"\n";
  digitalWrite(LoRa_Trans_LED,HIGH);

  LoRa.beginPacket();
  delay(50);
  if (DEBUG)  Serial.println(Sending);
  LoRa.print(Sending);
  LoRa.endPacket();
  delay(50);
  digitalWrite(LoRa_Trans_LED,LOW);
  
// JSON format 
/*
 LoRa.beginPacket();
 delay(50);
 LoRa.print(Lsqm); 
 LoRa.print(sqm); LoRa.print(F("LoRaID"));  LoRa.print(sqm);  LoRa.print(mark); LoRa.print(LoRaID); LoRa.print(comma);
 //LoRa.print(sqm); LoRa.print(F("PM25"));  LoRa.print(sqm);  LoRa.print(mark); LoRa.print(pm25); LoRa.print(comma);
 LoRa.print(sqm); LoRa.print(F("Temp"));  LoRa.print(sqm);  LoRa.print(mark); LoRa.print(t); LoRa.print(comma);
 LoRa.print(sqm); LoRa.print(F("Humi"));  LoRa.print(sqm);  LoRa.print(mark); LoRa.print(h); LoRa.print(comma);
 //LoRa.print(sqm); LoRa.print(F("CO2"));  LoRa.print(sqm);  LoRa.print(mark); LoRa.print(CO2);
 LoRa.print(Rsqm);
 LoRa.endPacket();
*/

// CSV format
/* 
 LoRa.beginPacket();
 delay(10);
 LoRa.print(LoRaID); LoRa.print(comma);
 LoRa.print(pm25); LoRa.print(comma);
 LoRa.print(t); LoRa.print(comma);
 LoRa.print(h); LoRa.print(comma);
 LoRa.print(CO2); LoRa.print(comma);
 LoRa.print(battpower); LoRa.print(comma);
 LoRa.print(chargestatus);
 LoRa.print(F("\n"));
 LoRa.endPacket();
 delay(10);
 */
}

