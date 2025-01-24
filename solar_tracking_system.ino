#include <Servo.h>

#define SERVOPINH  5 // horizontal servo
#define SERVOPINV  6 // vertical servo

int tol = 100;      // Response range of illuminance
int dtime = 100;    // Delay parameter

// Horizontal servo settings
Servo horizontal;            
int servoh = 90;             // Initial angle
int servohLimitHigh = 180;   // Max horizontal angle
int servohLimitLow = 0;      // Min horizontal angle

// Vertical servo settings
Servo vertical;              
int servov = 120;            // Initial angle
int servovLimitHigh = 180;   // Max vertical angle
int servovLimitLow = 90;     // Min vertical angle

// 4 connection ports for photoresistor modules   
const int ldrlt = A0;   // Top left
const int ldrrt = A1;   // Top right
const int ldrld = A2;   // Bottom left
const int ldrrd = A3;   // Bottom right

// Voltage measurement pins
const int servoHorizPin = A4; // Horizontal servo voltage
const int servoVertPin = A5;  // Vertical servo voltage

float readVoltage(int pin) {
  int raw = analogRead(pin);
  return (raw * 5.0) / 1023.0; // Convert ADC value to voltage
}

void setup() {
  horizontal.attach(SERVOPINH); 
  vertical.attach(SERVOPINV);
  horizontal.write(servoh);
  vertical.write(servov);
  delay(100);
  Serial.begin(9600);
}

void loop() {
  // Read illuminance values
  int lt = analogRead(ldrlt);
  int rt = analogRead(ldrrt);
  int ld = analogRead(ldrld);
  int rd = analogRead(ldrrd);

  // Calculate averages
  int avt = (lt + rt) / 2; 
  int avd = (ld + rd) / 2; 
  int avl = (lt + ld) / 2; 
  int avr = (rt + rd) / 2;
  int veg = (avt + avd + avl + avr) / 4;

  // Adjust vertical angle
  int dvert = avt - avd;
  if (abs(dvert) > tol) {
    if (dvert > 0) {
      servov = min(servov + 1, servovLimitHigh);
    } else {
      servov = max(servov - 1, servovLimitLow);
    }
    vertical.write(servov);
  }

  // Adjust horizontal angle
  int dhoriz = avl - avr;
  if (abs(dhoriz) > tol) {
    if (dhoriz < 0) {
      servoh = max(servoh - 1, servohLimitLow);
    } else {
      servoh = min(servoh + 1, servohLimitHigh);
    }
    horizontal.write(servoh);
  }

  // Read voltages
  float voltageLt = readVoltage(ldrlt);
  float voltageRt = readVoltage(ldrrt);
  float voltageLd = readVoltage(ldrld);
  float voltageRd = readVoltage(ldrrd);
  float voltageServoH = readVoltage(servoHorizPin);
  float voltageServoV = readVoltage(servoVertPin);

  // Send data via Serial
  Serial.print("lt:"); Serial.print(lt); Serial.print(" ");
  Serial.print("rt:"); Serial.print(rt); Serial.print(" ");
  Serial.print("ld:"); Serial.print(ld); Serial.print(" ");
  Serial.print("rd:"); Serial.print(rd); Serial.print(" ");
  Serial.print("servoh:"); Serial.print(servoh); Serial.print(" ");
  Serial.print("servov:"); Serial.print(servov); Serial.print(" ");
  Serial.print("voltageLt:"); Serial.print(voltageLt); Serial.print(" ");
  Serial.print("voltageRt:"); Serial.print(voltageRt); Serial.print(" ");
  Serial.print("voltageLd:"); Serial.print(voltageLd); Serial.print(" ");
  Serial.print("voltageRd:"); Serial.print(voltageRd); Serial.print(" ");
  Serial.print("voltageServoH:"); Serial.print(voltageServoH); Serial.print(" ");
  Serial.print("voltageServoV:"); Serial.println(voltageServoV);

  delay(dtime);
}
