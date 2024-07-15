#include <Arduino.h>
#include "DRV8834.h"
#include <AccelStepper.h>

/*
 ------------------------------------------------------------------------------------------
 Library used: DRV8834 (white motor driver)
               AccelStepper (helps with motor accel.)
 To be done:
  - quantify relationship between accel. value and the output wave freq.
     a. Plan was to to a whole period, use digitalWrite to flip a pin, measure with AD2
  - Serial communication UI functionality
  - Determine calibration functionality - where to start?
  - Mirror command with two motor drivers, drive two motors simultaneously
     a. TBD, another DRV8834? new motor drivers
     b. Also how to power both motors?
  - Potentially simplify the setup by using a pro mini once everything is finalized
 ------------------------------------------------------------------------------------------  
*/

// Pin definitions
#define MOTOR_STEPS 200
#define DIR 8
#define STEP 9
#define SLEEP 13
#define M0 10
#define M1 11

DRV8834 drv8834(MOTOR_STEPS, DIR, STEP, SLEEP, M0, M1);
AccelStepper stepper(AccelStepper::DRIVER, STEP, DIR);

// Variables
String motorData = "";                    // string to store received serial motor instruction data
bool program = false;                     // boolean to manage if arduino should be programmed with motor instructions (start button)
bool motorMove = false;                   // boolean to manage if motor should start moving (instructions received)
long motorSteps[256];                     // array to store motor instructions
int motorStepCount = 0;                   // int to track number of motor instructions given
int motorIndex = 0;                       // int to track 
int stepMode = 1;                         // Microstepping mode, 1 for full step, can go up to 32

void setup() {
    Serial.begin(9600);
    drv8834.begin();
    drv8834.enable();
    drv8834.setMicrostep(stepMode);     
    pinMode(SLEEP, OUTPUT);
    digitalWrite(SLEEP, HIGH);

    stepper.setMaxSpeed(150000);          // AccelStepper parameter to determine max speed
    stepper.setAcceleration(40000);       // AccelStepper parameter for acceleration
}

void loop() {
    while (Serial.available() > 0) {
        char character = Serial.read();                     // read serial char
        
        if (character == 'P') {                             // if this is the start of the msg, initiate programming msg
            program = true;
            motorData = "";
        } else if (program) {                               // if during programming
            if (character == 'V') {                         // if we reach the end of the msg
                program = false;
                parseData(motorData);                      
                motorMove = true;                           // motor ready to move
                // printMotorSteps();
                Serial.println("Y");                        // Confirmation back to UI that motor is programmed
                stepper.moveTo(motorSteps[0]*stepMode);    
                motorIndex = 1;  
            } else {
                motorData += character;                     // else, we're still receiving - append to motorData
            }
        }
    }

    if (motorMove){                                 
      if (stepper.distanceToGo() == 0) {                    // finished one motor instruction, move on
            // Serial.println(motorSteps[motorIndex],DEC);
            stepper.moveTo(motorSteps[motorIndex++]*stepMode);
      }
  
      if (motorIndex == motorStepCount){                    // reset motor instruction index
         motorIndex =0;
      }
      
      stepper.run();
    }
}

void parseData(String data) {
    motorStepCount = 0;
    for (int i = 0; i < data.length(); i += 4) {                              // 4 bytes per data point (1 sign, 3 mag)
        char sign = data.charAt(i);
        long steps = strtol(data.substring(i + 1, i + 4).c_str(), NULL, 16);
        if (sign == '0') steps = -steps;
        motorSteps[motorStepCount++] = steps;
    }
}

// ---------------------Debugging functions-------------------------------
void printMotorSteps() {
    for (int i = 0; i < motorStepCount; i++) {
        Serial.print("Step ");
        Serial.print(i + 1);
        Serial.print(": ");
        Serial.println(motorSteps[i]);
    }
}
