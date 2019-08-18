#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>

int TEMPERATURE_PIN = 8;
float TEMPERATURE_DATA = 0;

OneWire oneWire(TEMPERATURE_PIN);
DallasTemperature sensor (&oneWire);

void setup() {

  Serial.begin(9600);
  Serial.println("Test Sensor DS18B20 with Arduino");
  sensor.begin();

}

void loop() {

  sensor.requestTemperatures();
  TEMPERATURE_DATA = sensor.getTempCByIndex(0);
  Serial.print(TEMPERATURE_DATA);
  Serial.println(" C");
  delay(1000);

}
