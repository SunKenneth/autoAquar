void setup()
{
  Serial.begin(9600);
  
  pinMode(LoRa_Ready_LED, OUTPUT);
  pinMode(LoRa_Trans_LED, OUTPUT);

  LoRa_init();
  dht.begin();
  delay(5000);
}
