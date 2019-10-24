// the loop function runs over and over again forever
void loop() {
    getDHT();
    getFarm_value();
    Mini_LoRa_Transmit();
    delay(5000);
// End of Loop 
 }
