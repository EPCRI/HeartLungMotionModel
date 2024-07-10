#include <Arduino.h>
#include "DRV8834.h"

#define MOTOR_STEPS 200
#define DIR 8
#define STEP 9
#define SLEEP 13
#define M0 10
#define M1 11

// Initialization
DRV8834 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, M0, M1);

void setup() {
    Serial.begin(9600);
    stepper.enable();
    stepper.setMicrostep(1); // Set microstep mode to 1:1
}

void moveMotor(float duration, float rpm) {
    // Calculate steps for the given duration
    int steps = (rpm/ 60.0) * MOTOR_STEPS* duration;

    stepper.move(steps);
}

void loop() {
    // Check for incoming serial data
    if (Serial.available() > 0) {
        String commandStr = Serial.readStringUntil('\n');
        if (commandStr.length() > 0) {
            char direction = commandStr.charAt(0);
            float rpm = commandStr.substring(1).toFloat();
            bool clockwise = (direction == '+');
      
            moveMotor(di);
        }
    }
}
