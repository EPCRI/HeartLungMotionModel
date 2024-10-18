# backend.py
from frontend import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import time
import serial
import numpy as np
import pyqtgraph as pg
import glob
from scipy.signal import find_peaks
import json

"""
README:
This script works together with frontend.py and the Arduino firmware.

This UI is currently coded to support the lead screw system design.
For the lead screw design, stepper.moveTo have the motors move in the same direction.

To support the belt-rod design, change the following parameters:
Set displacement_per_revolution to 40 value
In the Arduino code, wherever there is stepper.moveTo function, make sure one is positive and one is negative.
"""

def generate_motion(t, heart_amplitude, heart_frequency, lung_amplitude, lung_frequency):
    """
    Python code to generate combined waveform consisting of heart and lung sine waves.
    """
    heart_motion = heart_amplitude * np.sin(2 * np.pi * heart_frequency * t)
    lung_motion = lung_amplitude * np.sin(2 * np.pi * lung_frequency * t)
    combined_motion = heart_motion + lung_motion
    return heart_motion, lung_motion, combined_motion

def encode_motor_instructions(steps, acceleration):
    """
    Encoding of motor instructions by measuring displacement between peaks of the combined waveform.
    Message = "P" (start byte) + acceleration (3 hex bytes) + data bytes (1 sign byte, 3 hex magnitude bytes per step) + "V" (end byte)
    """
    data = ['P']  # Start byte 'P'
    acceleration_hex = f'{int(acceleration / 100):03X}'  # Divide by 100 as Arduino multiplies by 100
    data.append(acceleration_hex)
    for step in steps:
        sign = '1' if step >= 0 else '0'
        magnitude = f'{abs(step):03X}'    # Mag in 3 hex bytes, sign in 1 byte, total 4 bytes per data point
        data.append(sign)
        data.append(magnitude)
    data.append('V')                      # End byte 'V'
    return ''.join(data).encode('utf-8')

displacement_per_revolution = 8  # mm
steps_per_mm = 200 / displacement_per_revolution

class Gooey(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Gooey, self).__init__(parent)
        self.setupUi(self)

        # Load profiles from JSON file
        with open('profiles.json', 'r') as f:
            self.profiles = json.load(f)
        # Populate comboBoxProfile
        profile_names = [profile['name'] for profile in self.profiles]
        self.comboBoxProfile.addItems(profile_names)
        # Connect profile selection
        self.comboBoxProfile.currentIndexChanged.connect(self.profile_selected)
        # Initialize acceleration
        self.acceleration = 1000  # Default value

        # Connect widgets to methods
        self.buttonStart.clicked.connect(self.start_continuous)
        self.buttonStop.clicked.connect(self.stop)
        self.buttonTest.clicked.connect(self.start_test)
        self.buttonRampTest.clicked.connect(self.ramp_test)
        self.buttonRefresh.clicked.connect(self.refresh_serial_ports)
        self.buttonUp.clicked.connect(self.up_movement)
        self.buttonDown.clicked.connect(self.down_movement)

        # Default display - COM ports
        self.ser = None
        ports = get_serial_ports()
        if not ports:
            self.labelConnectionStatus.setText("No available ports. Refresh!")
        else:
            self.labelConnectionStatus.setText("Connect to serial port.")
            self.comboBoxComPort.addItems(ports)
        self.comboBoxComPort.activated.connect(self.connect_arduino)

        # Initialize selected profile
        self.profile_selected(0)  # Load the first profile by default

    def profile_selected(self, index):
        selected_profile = self.profiles[index]
        # Update the parameters
        self.heart_amplitude = selected_profile['heart_amplitude']
        self.heart_frequency = selected_profile['heart_frequency'] / 60  # Convert bpm to Hz
        self.lung_amplitude = selected_profile['lung_amplitude']
        self.lung_frequency = selected_profile['lung_frequency'] / 60  # Convert bpm to Hz
        # Store the acceleration value
        self.acceleration = selected_profile['acceleration']
        # Update the waveform
        self.waveform_gen()
        # Calculate max amplitude
        t = np.arange(0, 1 / self.lung_frequency, 0.01)
        _, _, combined_motion = generate_motion(t, self.heart_amplitude, self.heart_frequency, self.lung_amplitude, self.lung_frequency)
        max_amp = np.nanmax(combined_motion) - np.nanmin(combined_motion)
        self.labelMaxAmp.setText(f"Pk-pk amplitude: {max_amp:.2f} cm")
        # Clear time feedback
        self.labelTimeFeedback.setText("Time feedback: N/A")

    def up_movement(self):
        """
        Elevate system by user input box (input received in cm)
        """
        displacement = float(self.lineEditDisplacement.text())
        steps = displacement * 10 * steps_per_mm
        command = f"U{int(steps)}\n"  # Added newline
        if self.ser:
            self.ser.write(command.encode())
        else:
            self.labelConnectionStatus.setText("No serial connection.")

    def down_movement(self):
        """
        Lower system by user input box (input received in cm)
        """
        displacement = float(self.lineEditDisplacement.text())
        steps = displacement * 10 * steps_per_mm
        command = f"D{int(steps)}\n"  # Added newline
        if self.ser:
            self.ser.write(command.encode())
        else:
            self.labelConnectionStatus.setText("No serial connection.")

    def start_continuous(self):
        """
        Send the motion pattern to the Arduino and start continuous movement.
        """
        if not self.ser:
            self.labelConnectionStatus.setText("No serial connection.")
            return

        # Program the Arduino with the motion pattern
        self.program_arduino()

        # Send 'G' command to start continuous movement
        self.ser.write(b'G')

    def start_test(self):
        """
        Send the motion pattern to the Arduino and run it once.
        """
        if not self.ser:
            self.labelConnectionStatus.setText("No serial connection.")
            return

        # Program the Arduino with the motion pattern
        self.program_arduino()

        # Send 'O' command to run once
        self.ser.write(b'O')

        # Read feedback from Arduino
        time_feedback = None
        while True:
            line = self.ser.readline().decode().strip()
            if line == '':
                continue  # Timeout, try again
            elif line == 'Y':
                break  # Done
            else:
                try:
                    time_feedback = int(line)
                except ValueError:
                    pass  # Ignore non-integer lines

        if time_feedback is not None:
            self.labelTimeFeedback.setText(f"Time feedback: {time_feedback} ms")
        else:
            self.labelTimeFeedback.setText("Time feedback: N/A")

    def program_arduino(self):
        """
        Generate motor instructions and send to Arduino.
        """
        t_fine = np.arange(0, 1 / self.lung_frequency, 0.01)
        heart_motion, lung_motion, combined_motion = generate_motion(t_fine, self.heart_amplitude, self.heart_frequency, self.lung_amplitude, self.lung_frequency)

        peaks, _ = find_peaks(combined_motion)
        troughs, _ = find_peaks(-combined_motion)

        extrema_indices = np.sort(np.concatenate((peaks, troughs)))
        extrema_values = combined_motion[extrema_indices] * 10  # in mm

        displacements_mm = np.diff(extrema_values)
        motor_steps = np.round(displacements_mm * steps_per_mm).astype(int)

        return_step = -np.round((extrema_values[-1] - extrema_values[0]) * steps_per_mm).astype(int)
        motor_steps = np.append(motor_steps, return_step)

        motor_instructions = encode_motor_instructions(motor_steps, self.acceleration)

        # Send motor instructions to Arduino
        self.ser.write(motor_instructions)

    def stop(self):
        """
        Stop motors through Arduino
        """
        if self.ser:
            self.ser.write(b'X')
        else:
            self.labelConnectionStatus.setText("No serial connection.")

    def ramp_test(self):
        """
        Loop through the profiles, running each one time full period, and stop.
        """
        if not self.ser:
            self.labelConnectionStatus.setText("No serial connection.")
            return

        for index, profile in enumerate(self.profiles):
            self.comboBoxProfile.setCurrentIndex(index)
            # Allow UI to update
            QApplication.processEvents()
            time.sleep(0.5)  # Small delay to ensure the waveform updates

            # Program and run test
            self.program_arduino()
            self.ser.write(b'O')

            # Read feedback from Arduino
            time_feedback = None
            while True:
                line = self.ser.readline().decode().strip()
                if line == '':
                    continue  # Timeout, try again
                elif line == 'Y':
                    break  # Done
                else:
                    try:
                        time_feedback = int(line)
                    except ValueError:
                        pass  # Ignore non-integer lines

            if time_feedback is not None:
                self.labelTimeFeedback.setText(f"Time feedback: {time_feedback} ms")
            else:
                self.labelTimeFeedback.setText("Time feedback: N/A")

            # Wait a bit before moving to next profile
            time.sleep(1)

    def refresh_serial_ports(self):
        """
        Refresh serial port list and update label message
        """
        if self.ser:
            self.ser.close()
            self.ser = None

        self.comboBoxComPort.clear()
        self.labelConnectionStatus.clear()

        ports = get_serial_ports()
        if not ports:
            self.labelConnectionStatus.setText("No available ports. Refresh!")
        else:
            self.labelConnectionStatus.setText("Connect to serial port.")
            self.comboBoxComPort.addItems(ports)

    def connect_arduino(self):
        """
        Once user selects COM Port, attempt serial connection with firmware
        """
        if self.ser:
            self.ser.close()
            self.ser = None

        port = self.comboBoxComPort.currentText()
        try:
            self.ser = serial.Serial(port=port, baudrate=9600, timeout=1, write_timeout=1)
            time.sleep(2)
            # Write 'T', expect to hear back 'C'
            self.ser.write(b'T')
            # Receive msg
            msg = self.ser.readline()
            if msg and msg.strip() == b'C':
                self.labelConnectionStatus.setText("Connected.")
            else:
                self.labelConnectionStatus.setText("Recheck COM Port")
                self.ser.close()
                self.ser = None
        except serial.SerialException as e:
            self.labelConnectionStatus.setText(f"Serial error: {e}")
            self.ser = None

    def waveform_gen(self):
        """
        Plot waveform based on selected profile
        """
        self.widgetWaveForm.clear()
        dt = 0.01
        wave_period = 1 / self.lung_frequency
        t = np.arange(0, wave_period, dt)
        # Only plot combined_motion
        _, _, combined_motion = generate_motion(t, self.heart_amplitude, self.heart_frequency, self.lung_amplitude, self.lung_frequency)

        combined_pen = pg.mkPen(color=(0, 0, 255), width=2)

        # Removed legend since only one plot
        self.widgetWaveForm.plot(t, combined_motion, pen=combined_pen)
        self.widgetWaveForm.setXRange(0, wave_period)
        self.widgetWaveForm.showGrid(x=True, y=True)

def get_serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = [f'COM{i+1}' for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(str(port))
        except (OSError, serial.SerialException):
            pass
    return result

def main():
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    form = Gooey()
    form.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
