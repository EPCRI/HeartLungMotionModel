bool calibrating = false;

void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT); // LED pin set to output mode - LED blinks to simulate calibration purposes
    Serial.println("Arduino is ready.");
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();

        switch (command) {
            case 'T':                   // UI sends T, arduino responds C
                Serial.write("C\n"); 
                break;
            case 'C':
                calibrating = true;
                Serial.write("Y\n");     // Respond with Y to calibration request
                while (calibrating) {    // continuously blink LED to simulate calibration process
                    digitalWrite(LED_BUILTIN, HIGH);
                    delay(500); 
                    digitalWrite(LED_BUILTIN, LOW);
                    delay(500);

                    if (Serial.available() > 0 && Serial.read() == 'X') {       // if we get an "X" message in the middle, pause, return Y
                        calibrating = false;
                        Serial.write("Y\n");
                    }
                }
                break;
            case 'X':
                calibrating = false;          // Stop everything, return Y
                Serial.write("Y\n"); 
                break;
            case 'P':                         // P simulate start button for now
                {
                    int numbers[10] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
                    for (int i = 0; i < 10; i++) {
                        Serial.print(numbers[i]);
                        if (i < 9) {
                            Serial.print(", ");
                        }
                    }
                    Serial.println();
                }
                break;
            default:
                // All other cases
                Serial.println("A");
                break;
        }
    }
}
