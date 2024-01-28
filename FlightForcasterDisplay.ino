#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
  // Set up the LCD's number of columns and rows
  lcd.begin(16, 2);
  
  // Initialize Serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    String data = Serial.readStringUntil('\n');

    scrollText(data);
  }
}

void scrollText(String text){
  int len = text.length();
  int maxPos = len - 16;

  for(int pos = 0; pos <= maxPos ; pos++){
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(text.substring(pos, pos + 16));
    delay(500);
  }
}

