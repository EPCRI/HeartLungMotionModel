#include <Arduino.h>
#include "DRV8834.h"
#include <AccelStepper.h>

/* Lead screw motor connection
 *  Blue, red, black, green (top to bottom, bottom is gnd)
 *  With coupler: Green, black red blue
*/
 
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
// Motor 1
#define MOTOR_STEPS 200
#define MOTOR1_DIR 8
#define MOTOR1_STEP 9
#define MOTOR1_MS1 10
#define MOTOR1_MS2 11
#define MOTOR1_MS3 12

#define MOTOR2_DIR 2
#define MOTOR2_STEP 3
#define MOTOR2_SLEEP 4
#define MOTOR2_M0 5
#define MOTOR2_M1 6


AccelStepper stepper1(AccelStepper::DRIVER, MOTOR1_STEP, MOTOR1_DIR);
DRV8834 drv8834(MOTOR_STEPS, MOTOR2_DIR, MOTOR2_STEP, MOTOR2_SLEEP, MOTOR2_M0, MOTOR2_M1);
AccelStepper stepper2(AccelStepper::DRIVER, MOTOR2_STEP, MOTOR2_DIR);

// Variables
String motorData = "";                    // string to store received serial motor instruction data
bool program = false;                     // boolean to manage if arduino should be programmed with motor instructions (start button)
bool motorMove = false;                   // boolean to manage if motor should start moving (instructions received)
long motorSteps[128];                     // array to store motor instructions
int motorStepCount = 0;                   // int to track number of motor instructions given
int motorIndex = 0;                       // int to track 
int stepMode = 1;                         // Microstepping mode, 1 for full step, can go up to 32

unsigned long startTime = 0;              // Variable to store the start time
unsigned long endTime = 0;                // Variable to store the end time

long positions[2];

void setup() {
    Serial.begin(9600);
    // motor 1 - a4988
    pinMode(MOTOR1_MS1, OUTPUT);
    pinMode(MOTOR1_MS2, OUTPUT);
    pinMode(MOTOR1_MS3, OUTPUT);

    digitalWrite(MOTOR1_MS1, LOW);
    digitalWrite(MOTOR1_MS2, LOW);
    digitalWrite(MOTOR1_MS3, LOW);

    stepper1.setMaxSpeed(150000);      
    stepper1.setAcceleration(4000);

    // motor 2 - drv8834
    drv8834.begin();
    drv8834.enable();
    drv8834.setMicrostep(stepMode);
    pinMode(MOTOR2_SLEEP, OUTPUT);
    pinMode(MOTOR2_M0, OUTPUT);
    pinMode(MOTOR2_M1, OUTPUT);
    digitalWrite(MOTOR2_SLEEP, HIGH);
    digitalWrite(MOTOR2_M0, LOW);
    digitalWrite(MOTOR2_M1, LOW);
          
    stepper2.setMaxSpeed(150000);          
    stepper2.setAcceleration(4000);  
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
                // Serial.println("Y");                        // Confirmation back to UI that motor is programmed
                moveMotors();
                motorIndex = 1;  
            } else {
                motorData += character;                     // else, we're still receiving - append to motorData
            }
        }
    }

    if (motorMove){ 
                                     
      if (stepper1.distanceToGo() == 0 && stepper2.distanceToGo() == 0) {                   // finished one motor instruction, move on
            if (motorIndex < motorStepCount) {
                moveMotors();
                motorIndex++;
            } else {
                motorIndex = 0;
                motorMove = false;
                endTime = millis();                        // Record the end time
                Serial.println(endTime - startTime, DEC);
                Serial.println("Y"); 
            }
        }
        stepper1.run();
        stepper2.run();
    }
}

void moveMotors() {
    stepper1.moveTo(motorSteps[motorIndex] * stepMode);
    stepper2.moveTo(motorSteps[motorIndex] * stepMode);
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
