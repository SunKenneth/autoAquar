void getDHT()
{
  t=0.0;
  h=0.0;
  t = dht.readTemperature();
  delay(10);
  h = dht.readHumidity();
  if (DEBUG) Display_DHT();
}

void Display_DHT()
{

  Serial.print("T = ");
  Serial.print(t);
  Serial.print("*C");
  Serial.print(",H = ");
  Serial.print(h);
  Serial.println("%");

}

