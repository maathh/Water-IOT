void setup() {
  Serial.begin(9600);
  pinMode(8,  INPUT);
}

void loop() {
  Serial.print(digitalRead(8));
  delay(100);
}
