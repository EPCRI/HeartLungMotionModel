# HeartLungMotionModel

Folder descriptions:

Arduino code works on library "DRV8834.h" and "AccelStepper.h"

Manual calibrate: allows user to use just the arduino control the motors via serial with simple commands like "U" (up one rotation) and "D" one rotation

UI: contains the frontend, backend PyQt5 code of user interface, works together with arduino code UI_integrate_Heart_Lung.ino

Test_Motion - accel_stepper_impl: python code that only contains the functionality to program motors for the combined waveform displacement, works with accel_stepper_impl.ino


Archive: some old code that led to above folders' development
