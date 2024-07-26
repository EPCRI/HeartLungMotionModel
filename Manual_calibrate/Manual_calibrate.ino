#include <Arduino.h>
#include <AccelStepper.h>
#include "DRV8834.h" 

#define MOTOR_STEPS 200
#define MOTOR1_DIR 8
#define MOTOR1_STEP 9
#define MOTOR1_SLEEP 10
#define MOTOR1_M0 11
#define MOTOR1_M1 12

#define MOTOR2_DIR 2
#define MOTOR2_STEP 3
#define MOTOR2_SLEEP 4
#define MOTOR2_M0 5
#define MOTOR2_M1 6


AccelStepper stepper1(AccelStepper::DRIVER, MOTOR1_STEP, MOTOR1_DIR);
DRV8834 drv8834_1(MOTOR_STEPS, MOTOR1_DIR, MOTOR1_STEP, MOTOR1_SLEEP, MOTOR1_M0, MOTOR1_M1);
DRV8834 drv8834_2(MOTOR_STEPS, MOTOR2_DIR, MOTOR2_STEP, MOTOR2_SLEEP, MOTOR2_M0, MOTOR2_M1);
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

unsigned long acce = 4000;
void setup() {
    Serial.begin(9600);
    // motor 1 - a4988
    drv8834_1.begin();
    drv8834_1.enable();
    drv8834_1.setMicrostep(stepMode);
    pinMode(MOTOR1_SLEEP, OUTPUT);
    pinMode(MOTOR1_M0, OUTPUT);
    pinMode(MOTOR1_M1, OUTPUT);
    digitalWrite(MOTOR1_SLEEP, HIGH);
    digitalWrite(MOTOR1_M0, LOW);
    digitalWrite(MOTOR1_M1, LOW);

    stepper1.setMaxSpeed(150000);      
    stepper1.setAcceleration(acce);

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
          
    stepper2.setMaxSpeed(150000);          
    stepper2.setAcceleration(acce);  
}


void loop() {
    if (Serial.available() > 0) {
        char received = Serial.read();
        if (received == 'U') {
            // Move one full rotation (200 steps for a 1.8-degree step angle motor in full-step mode)
            stepper1.moveTo(stepper1.currentPosition() - MOTOR_STEPS);
            stepper2.moveTo(stepper2.currentPosition() - MOTOR_STEPS);
        }
        if (received == 'D') {
            // Move one full rotation (200 steps for a 1.8-degree step angle motor in full-step mode)
            stepper1.moveTo(stepper1.currentPosition() + MOTOR_STEPS);
            stepper2.moveTo(stepper2.currentPosition() + MOTOR_STEPS);
        }
    }

    // Run the motor to the target position
    stepper1.run();
    stepper2.run();
}
