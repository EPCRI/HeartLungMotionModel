#include <Arduino.h>
#include "DRV8834.h"

#define MOTOR_STEPS 200
#define DIR 8
#define STEP 9
#define SLEEP 13 // optional
#define M0 10
#define M1 11
#define RPM 200

// Initialization
DRV8834 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, M0, M1);

// Variables
String motorData = "";            // String to store received motor instruction data
bool program = false;             // boolean for managing if the motor instructions should be programmed to memory
int instructionIndex = 0;
unsigned long interval;

int motorSteps[256];              // Memory array to store motor instructions
int motorStepCount = 0;

void setup() {
    Serial.begin(9600);
    stepper.begin(RPM);
    stepper.enable();
    stepper.setMicrostep(1);      // Set microstep mode to 1:1
}

void loop() {
    while (Serial.available() > 0) {
        char character = Serial.read();                     // read character
        
        if (character == 'P') {                             // if this is the start of the msg - reset var
            program = true;
            motorData = "";
        } else if (program) {                               // if we're in the middle of receiving
            if (character == 'V') {                         // reached the end of the msg
                program = false;
                parseData(motorData);                       // parse received data
                // printMotorSteps();                       // after we're all done, print the decoded data
            } else {
                motorData += character;                     // else, we're still receiving - append to motorData
            }
        }
    }
}

void parseData(String data) {
    motorStepCount = 0;
    int samplingRate = strtol(data.substring(0, 2).c_str(), NULL, 16);
    
    interval = 1000 / samplingRate;                               // update value of sampling interval in ms

    for (int i = 2; i < data.length(); i += 3) {
        char sign = data.charAt(i);
        int steps = strtol(data.substring(i + 1, i + 3).c_str(), NULL, 16);
        if (sign == '0') steps = -steps;
        motorSteps[motorStepCount++] = steps;
    }
}


---------------------Archive functions-------------------------------
void printMotorSteps() {
    for (int i = 0; i < motorStepCount; i++) {
        Serial.print("Step ");
        Serial.print(i + 1);
        Serial.print(": ");
        Serial.println(motorSteps[i]);
    }
}
