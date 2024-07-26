#include <Arduino.h>
#include "DRV8834.h"
#include <AccelStepper.h>

/*
 ------------------------------------------------------------------------------------------
 Library used: DRV8834 (white motor driver)
               AccelStepper (helps with motor accel.)
 To be done:
  - quantify relationship between accel. value and the output wave freq.
     a. Whole period vs. acceleration curve
  - Serial communication UI functionality
  - Determine calibration functionality - where to start?
  - Potentially simplify the setup by using a pro mini once everything is finalized
 ------------------------------------------------------------------------------------------  
*/

// Pin definitions 
// Motor 1
#define MOTOR_STEPS 200
#define MOTOR1_DIR 8
#define MOTOR1_STEP 9
#define MOTOR1_SLEEP 10
#define MOTOR1_M0 11
#define MOTOR1_M1 12

// Motor 2
#define MOTOR2_DIR 2
#define MOTOR2_STEP 3
#define MOTOR2_SLEEP 4
#define MOTOR2_M0 5
#define MOTOR2_M1 6

// Create motor control objects
AccelStepper stepper1(AccelStepper::DRIVER, MOTOR1_STEP, MOTOR1_DIR);
DRV8834 drv8834_1(MOTOR_STEPS, MOTOR1_DIR, MOTOR1_STEP, MOTOR1_SLEEP, MOTOR1_M0, MOTOR1_M1);
DRV8834 drv8834_2(MOTOR_STEPS, MOTOR2_DIR, MOTOR2_STEP, MOTOR2_SLEEP, MOTOR2_M0, MOTOR2_M1);
AccelStepper stepper2(AccelStepper::DRIVER, MOTOR2_STEP, MOTOR2_DIR);

// Variables
String motorData = "";                    // String to store received serial motor instruction data
bool program = false;                     // Boolean to manage if Arduino should be programmed with motor instructions (start button)
bool motorMove = false;                   // Boolean to manage if motor should start moving (instructions received)
bool calibrateMotorMove = false;          // Boolean to manage if motor should start moving due to calibration
long motorSteps[128];                     // Array to store motor instructions
int motorStepCount = 0;                   // Int to track number of motor instructions given
int motorIndex = 0;                       // Int to track current motor step index
int stepMode = 1;                         // Microstepping mode, 1 for full step, can go up to 32
unsigned long startTime = 0;              // Variable to store the start time
unsigned long endTime = 0;                // Variable to store the end time
unsigned long acce = 20000;               // Acceleration
unsigned long speedd = 100000;            // Maximum speed

void setup() {
    Serial.begin(9600);

    // Motor 1 setup
    drv8834_1.begin();
    drv8834_1.enable();
    drv8834_1.setMicrostep(stepMode);
    pinMode(MOTOR1_SLEEP, OUTPUT);
    pinMode(MOTOR1_M0, OUTPUT);
    pinMode(MOTOR1_M1, OUTPUT);
    digitalWrite(MOTOR1_SLEEP, HIGH);
    digitalWrite(MOTOR1_M0, LOW);
    digitalWrite(MOTOR1_M1, LOW);

    stepper1.setMaxSpeed(speedd);      
    stepper1.setAcceleration(acce);

    // Motor 2 setup
    drv8834_2.begin();
    drv8834_2.enable();
    drv8834_2.setMicrostep(stepMode);
    pinMode(MOTOR2_SLEEP, OUTPUT);
    pinMode(MOTOR2_M0, OUTPUT);
    pinMode(MOTOR2_M1, OUTPUT);
    digitalWrite(MOTOR2_SLEEP, HIGH);
    digitalWrite(MOTOR2_M0, LOW);
    digitalWrite(MOTOR2_M1, LOW);

    stepper2.setMaxSpeed(speedd);          
    stepper2.setAcceleration(acce);  
}

void loop() {
    while (Serial.available() > 0) {
        char command = Serial.read();  // Read serial char

        if (command == 'T'){
          Serial.write("C");
        }
        else if (command == 'P') {  // If this is the start of the msg, initiate programming msg
            program = true;
            motorData = "";
        } else if (program) {  // If during programming
            if (command == 'V') {  // If we reach the end of the msg
                program = false;
                parseData(motorData);
                motorMove = true;  // Motor ready to move
                moveMotors();
                motorIndex = 1;  
                startTime = millis();
            } else {
                motorData += command;  // Else, we're still receiving - append to motorData
            }
        } else if (command == 'U' || command == 'D') {  // Handle up/down commands
            String steps_str = Serial.readStringUntil('\n');
            long steps = steps_str.toInt();
            if (command == 'D') steps = -steps;
            calibrateMotorMove = true;
            stepper1.moveTo(steps);
            stepper2.moveTo(steps);
        } else if (command == 'X') {  // Stop motors
            stepper1.stop();
            stepper2.stop();
        }
    }

    if (motorMove) {
        if (stepper1.distanceToGo() == 0 && stepper2.distanceToGo() == 0) {  // Finished one motor instruction, move on
            if (motorIndex < motorStepCount) {
                moveMotors();
                motorIndex++;
            } else {
                motorMove = false;
                motorIndex = 0;
                endTime = millis();  // Record the end time
                Serial.println(endTime - startTime, DEC);
                Serial.println("Y");  // Notify UI that the sequence is complete
            }
        }
        stepper1.run();
        stepper2.run();
    }

    if (calibrateMotorMove){
        if (stepper1.distanceToGo() == 0 && stepper2.distanceToGo() == 0) { 
            calibrateMotorMove = false;
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
    for (int i = 0; i < data.length(); i += 4) {  // 4 bytes per data point (1 sign, 3 mag)
        char sign = data.charAt(i);
        long steps = strtol(data.substring(i + 1, i + 4).c_str(), NULL, 16);
        if (sign == '0') steps = -steps;
        motorSteps[motorStepCount++] = steps;
    }
}
