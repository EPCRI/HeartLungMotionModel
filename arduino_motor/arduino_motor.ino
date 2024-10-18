// Arduino Code
#include <Arduino.h>
#include <AccelStepper.h>
#include "DRV8834.h"

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

AccelStepper stepper1(AccelStepper::DRIVER, MOTOR1_STEP, MOTOR1_DIR);
AccelStepper stepper2(AccelStepper::DRIVER, MOTOR2_STEP, MOTOR2_DIR);
DRV8834 drv8834_1(MOTOR_STEPS, MOTOR1_DIR, MOTOR1_STEP, MOTOR1_SLEEP, MOTOR1_M0, MOTOR1_M1);
DRV8834 drv8834_2(MOTOR_STEPS, MOTOR2_DIR, MOTOR2_STEP, MOTOR2_SLEEP, MOTOR2_M0, MOTOR2_M1);

// Variables
String motorData = "";                    // String to store serial motor data
bool program = false;                     // Boolean for if Arduino should be programmed
bool motorMove = false;                   
bool calibrateMotor = false;
bool continuousMode = false;              // New variable for continuous mode
long motorSteps[128];                     // Array for motor instructions
int motorStepCount = 0;                   
int motorIndex = 0;                       
int stepMode = 1;                        

unsigned long startTime = 0;              
unsigned long endTime = 0;                
unsigned long acce = 20000;
unsigned long speedd = 200000;

void setup() {
    Serial.begin(9600);
    drv8834_1.begin();
    drv8834_1.enable();
    drv8834_1.setMicrostep(stepMode);
    pinMode(MOTOR1_SLEEP, OUTPUT);
    pinMode(MOTOR1_M0, OUTPUT);
    pinMode(MOTOR1_M1, OUTPUT);
    digitalWrite(MOTOR1_SLEEP, HIGH);
    digitalWrite(MOTOR1_M0, LOW);
    digitalWrite(MOTOR1_M1, LOW);   

    // Motor 2 - drv8834
    drv8834_2.begin();
    drv8834_2.enable();
    drv8834_2.setMicrostep(stepMode);
    pinMode(MOTOR2_SLEEP, OUTPUT);
    pinMode(MOTOR2_M0, OUTPUT);
    pinMode(MOTOR2_M1, OUTPUT);
    digitalWrite(MOTOR2_SLEEP, HIGH);
    digitalWrite(MOTOR2_M0, LOW);
    digitalWrite(MOTOR2_M1, LOW);

    stepper1.setMaxSpeed(speedd);   
    stepper2.setMaxSpeed(speedd);           
}

void loop() {
    while (Serial.available() > 0) {
        char command = Serial.read();                     

        if (command == 'T'){
            Serial.write("C");
        }
        else if (command == 'P') {                             // Program message
            program = true;
            motorData = "";
        } else if (program) {                               
            if (command == 'V') {                         // End of the program message
                program = false;
                parseData(motorData);                      
                // Do not start moving yet, wait for 'G' or 'O' command
            } else {
                motorData += command;                     
            }
        } else if (command == 'G') {   // Start continuous movement
            continuousMode = true;
            motorMove = true;
            motorIndex = 0;
            moveMotors();
            motorIndex++;
            startTime = millis(); 
        } else if (command == 'O') {  // Start one-time movement
            continuousMode = false;
            motorMove = true;
            motorIndex = 0;
            moveMotors();
            motorIndex++;
            startTime = millis(); 
        } else if (command == 'U' || command == 'D') {  // Handle up/down commands
            String steps_str = Serial.readStringUntil('\n');
            long steps = steps_str.toInt();
            if (command == 'D') steps = -steps;
            calibrateMotor = true;
            stepper1.move(steps);
            stepper2.move(steps);
        } else if (command == 'X') {  // Stop motors
            stepper1.stop();
            stepper2.stop();
            motorMove = false;
            program = false;
            motorIndex = 0;
        }
    }

    if (motorMove){                              
        if (stepper1.distanceToGo() == 0 && stepper2.distanceToGo() == 0) {                   
            if (motorIndex < motorStepCount) {
                moveMotors();
                motorIndex++;
            } else {
                endTime = millis();
                Serial.println(endTime - startTime, DEC);
                Serial.println("Y");

                if (continuousMode) {
                    motorIndex = 0;  // Reset index and continue moving
                    startTime = millis();  // Reset start time
                    moveMotors();
                    motorIndex++;
                } else {
                    motorIndex = 0;
                    motorMove = false;
                }
            }
        }
        stepper1.run();
        stepper2.run();
    }

    if (calibrateMotor){
        if (stepper1.distanceToGo() == 0 && stepper2.distanceToGo() == 0) { 
            calibrateMotor = false;
        }
        stepper1.run();
        stepper2.run();
    }
}

void moveMotors() {
    stepper1.move(motorSteps[motorIndex] * stepMode);
    stepper2.move(motorSteps[motorIndex] * stepMode);
}

void parseData(String data) {
    motorStepCount = 0;
    long acceleration = strtol(data.substring(0, 3).c_str(), NULL, 16) * 100;
    
    stepper1.setAcceleration(acceleration);
    stepper2.setAcceleration(acceleration);
    
    for (int i = 3; i < data.length(); i += 4) { 
        char sign = data.charAt(i);
        long steps = strtol(data.substring(i + 1, i + 4).c_str(), NULL, 16);
        if (sign == '0') steps = -steps;
        motorSteps[motorStepCount++] = steps;
    }
}
