/*
 * Microstepping demo
 *
 * This requires that microstep control pins be connected in addition to STEP,DIR
 *
 * Copyright (C)2015 Laurentiu Badea
 *
 * This file may be redistributed under the terms of the MIT license.
 * A copy of this license has been included with this distribution in the file LICENSE.
 */
#include <Arduino.h>
#include "DRV8834.h"

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200
#define RPM 250

#define DIR 8
#define STEP 9
#define SLEEP 13 // optional (just delete SLEEP from everywhere if not used)
#define M0 10
#define M1 11

// Initizliation
DRV8834 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, M0, M1);
void setup() {
    /*
     * Set target motor RPM.
     */
    stepper.begin(RPM);
    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
    // stepper.setEnableActiveState(LOW);
    stepper.enable();
    
    // set current level (for DRV8880 only). 
    // Valid percent values are 25, 50, 75 or 100.
    // stepper.setCurrent(100);
}

void loop() {
    delay(1000);

    /*
     * Moving motor in full step mode is simple:
     */
    stepper.setMicrostep(1);  // Set microstep mode to 1:1

    // Calculate steps for 1 second at 250 RPM
    int steps_per_second = (RPM / 60.0) * MOTOR_STEPS;

    // Move the motor for 1 second
    stepper.move(-steps_per_second);
    delay(2000);
}
