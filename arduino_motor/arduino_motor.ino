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
String motorData = "";                    // string to store serial motor data
bool program = false;                     // boolean for if arduino should be programmed
bool motorMove = false;                   
long motorSteps[128];                     // array for motor instructions
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

    // motor 2 - drv8834
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
        char character = Serial.read();                     
        
        if (character == 'P') {                             // program msg
            program = true;
            motorData = "";
        } else if (program) {                               
            if (character == 'V') {                         // end of the program msg
                program = false;
                parseData(motorData);                      
                motorMove = true;                           
                // Serial.println("Y");                     // Confirm programmed state
                moveMotors();   
                motorIndex = 1;  
                startTime = millis();                       
            } else {
                motorData += character;                     
            }
        }
    }

    if (motorMove){                              
      if (stepper1.distanceToGo() == 0 && stepper2.distanceToGo() == 0) {                   
            if (motorIndex < motorStepCount) {
                moveMotors();
                motorIndex++;
            } else {
                motorIndex = 0;
                motorMove = false;
                endTime = millis();                       
                Serial.println(endTime - startTime, DEC);
                Serial.println("Y"); 
            }
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