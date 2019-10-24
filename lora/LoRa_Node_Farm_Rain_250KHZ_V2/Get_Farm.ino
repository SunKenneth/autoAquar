void getFarm_value()
{
  // read the value from the sensor:
  MositureValue = 1023-analogRead(MosituresensorPin);
  LightValue = 1023-analogRead(LightsensorPin);
  //RainValue = 1023-analogRead(RainsensorPin);  
  Serial.print("MositureValue="); Serial.println(MositureValue);
  Serial.print("LightValu="); Serial.println(LightValue);
  //Serial.print("RainValue="); Serial.println(RainValue);    
}

