#include <Servo.h> 

#define SERVOPINH  5 // Horizontal servo
#define SERVOPINV  6 // Vertical servo
bool operation_flag=true;

// Horizontal servo settings
Servo horizontal;            // Horizontal servo
int servoh = 90;             // Initialize angle
int servohLimitHigh = 180;   // Maximum angle of rotation in the horizontal direction
int servohLimitLow = 0;      // Minimum angle of rotation in the horizontal direction

// Vertical Servo Settings
Servo vertical;              // Vertical servo
int servov = 90;             // Initialize angle
int servovLimitHigh = 180;   // Maximum angle of rotation in the vertical direction
int servovLimitLow = 90;     // Minimum angle of rotation in the vertical direction

void setup()
{ 
  horizontal.attach(SERVOPINH); 
  vertical.attach(SERVOPINV);
  horizontal.write(servoh);
  vertical.write(servov);
}

void loop() 
{
}
