# backend.py
from frontend import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
import sys
import time
import serial
import numpy as np
import pyqtgraph as pg
import glob
from scipy.signal import find_peaks
import json

import os
os.environ["QT_LOGGING_RULES"] = "qt.qpa.fonts.warning=false"


"""
This script works together with frontend.py and the Arduino firmware.
"""

def generate_motion(t, heart_amplitude, heart_frequency, lung_amplitude, lung_frequency):
    """
    Generate combined waveform consisting of heart and lung sine waves.
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

# Variables
displacement_per_revolution = 8  # mm
steps_per_mm = 200 / displacement_per_revolution

class RampTestWorker(QObject):
    progress = pyqtSignal(int, str)
    profile_started = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, profiles, ser):
        super().__init__()
        self.profiles = profiles
        self.ser = ser
        self._is_running = True

    def run(self):
        for index, profile in enumerate(self.profiles):
            if not self._is_running:
                break

            self.profile_started.emit(index)
            QApplication.processEvents()

            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

            # Program Arduino with current profile
            t_fine = np.arange(0, 1 / (profile['lung_frequency'] / 60), 0.01)
            heart_amp = profile['heart_amplitude']
            heart_freq = profile['heart_frequency'] / 60
            lung_amp = profile['lung_amplitude']
            lung_freq = profile['lung_frequency'] / 60
            acceleration = profile['acceleration']

            _, _, combined_motion = generate_motion(t_fine, heart_amp, heart_freq, lung_amp, lung_freq)

            peaks, _ = find_peaks(combined_motion)
            troughs, _ = find_peaks(-combined_motion)

            extrema_indices = np.sort(np.concatenate((peaks, troughs)))
            extrema_values = combined_motion[extrema_indices] * 10  # in mm

            displacements_mm = np.diff(extrema_values)
            motor_steps = np.round(displacements_mm * steps_per_mm).astype(int)

            return_step = -np.round((extrema_values[-1] - extrema_values[0]) * steps_per_mm).astype(int)
            motor_steps = np.append(motor_steps, return_step)

            motor_instructions = encode_motor_instructions(motor_steps, acceleration)

            # Send motor instructions to Arduino
            self.ser.write(motor_instructions)
            time.sleep(0.1)

            # Send 'O' command to run once
            self.ser.write(b'O')

            # Read feedback from Arduino
            time_feedback = None
            while self._is_running:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode().strip()
                    if line == '':
                        continue  # Ignore empty lines
                    elif line == 'Y':
                        break  # Done
                    else:
                        try:
                            time_feedback = int(line)
                        except ValueError:
                            pass  # Ignore non-integer lines
                else:
                    time.sleep(0.01)  # Small delay to prevent tight loop

            if time_feedback is not None:
                self.progress.emit(index, f"Time feedback: {time_feedback} ms")
            else:
                self.progress.emit(index, "Time feedback: N/A")

            # Small delay before moving to next profile
            time.sleep(1)

        self.finished.emit()

    def stop(self):
        self._is_running = False

class Gooey(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Gooey, self).__init__(parent)
        self.setupUi(self)

        # Load profiles from JSON file
        with open('UI/profiles.json', 'r') as f:
            self.profiles = json.load(f)
        profile_names = [profile['name'] for profile in self.profiles]
        self.comboBoxProfile.addItems(profile_names)
        self.comboBoxProfile.currentIndexChanged.connect(self.profile_selected)
        self.acceleration = 1000

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
        self.profile_selected(0)

        # Initialize a timer for continuous feedback
        self.feedback_timer = QTimer()
        self.feedback_timer.timeout.connect(self.read_continuous_feedback)

    def profile_selected(self, index):
        selected_profile = self.profiles[index]
        # Update the parameters
        self.heart_amplitude = selected_profile['heart_amplitude']
        self.heart_frequency = selected_profile['heart_frequency'] / 60  
        self.lung_amplitude = selected_profile['lung_amplitude']
        self.lung_frequency = selected_profile['lung_frequency'] / 60 
        self.acceleration = selected_profile['acceleration']
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
        command = f"U{int(steps)}\n" 
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
        command = f"D{int(steps)}\n"
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

        # Start the timer to read feedback
        self.feedback_timer.start(100)

        # Disable buttons to prevent multiple starts
        self.buttonStart.setEnabled(False)
        self.buttonTest.setEnabled(False)
        self.buttonRampTest.setEnabled(False)
        self.buttonStop.setEnabled(True)

    def read_continuous_feedback(self):
        """
        Read time feedback from Arduino during continuous movement.
        """
        while self.ser.in_waiting:
            line = self.ser.readline().decode().strip()
            if line == '':
                continue  # Ignore empty lines
            elif line == 'Y':
                pass
            else:
                try:
                    time_feedback = int(line)
                    self.labelTimeFeedback.setText(f"Time feedback: {time_feedback} ms")
                except ValueError:
                    pass  # Ignore non-integer lines

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
        _, _, combined_motion = generate_motion(t_fine, self.heart_amplitude, self.heart_frequency, self.lung_amplitude, self.lung_frequency)

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
        Stop motors and cleanup
        """
        if self.ser:
            self.ser.write(b'X')
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        else:
            self.labelConnectionStatus.setText("No serial connection.")

        # Stop the feedback timer if running
        if self.feedback_timer.isActive():
            self.feedback_timer.stop()

        # If ramp test is running, stop the worker
        if hasattr(self, 'ramp_test_worker'):
            self.ramp_test_worker.stop()
            self.ramp_test_thread.quit()
            self.ramp_test_thread.wait()
            del self.ramp_test_worker
            del self.ramp_test_thread

        # Re-enable buttons
        self.buttonStart.setEnabled(True)
        self.buttonTest.setEnabled(True)
        self.buttonRampTest.setEnabled(True)
        self.buttonStop.setEnabled(False)

        # Reset time feedback label
        self.labelTimeFeedback.setText("Time feedback: N/A")


    def update_profile_started(self, index):
        self.comboBoxProfile.setCurrentIndex(index)
        self.profile_selected(index)
        QApplication.processEvents()

    def ramp_test(self):
        """
        Loop through the profiles, running each one time full period, and stop.
        """
        if not self.ser:
            self.labelConnectionStatus.setText("No serial connection.")
            return

        # Disable the buttons to prevent multiple clicks
        self.buttonStart.setEnabled(False)
        self.buttonTest.setEnabled(False)
        self.buttonRampTest.setEnabled(False)
        self.buttonStop.setEnabled(True)

        # Create the worker and thread
        self.ramp_test_worker = RampTestWorker(self.profiles, self.ser)
        self.ramp_test_thread = QThread()
        self.ramp_test_worker.moveToThread(self.ramp_test_thread)

        # Connect signals
        self.ramp_test_worker.profile_started.connect(self.update_profile_started)
        self.ramp_test_thread.started.connect(self.ramp_test_worker.run)
        self.ramp_test_worker.progress.connect(self.update_ramp_test_progress)
        self.ramp_test_worker.finished.connect(self.ramp_test_finished)
        self.ramp_test_worker.finished.connect(self.ramp_test_thread.quit)
        self.ramp_test_worker.finished.connect(self.ramp_test_worker.deleteLater)
        self.ramp_test_thread.finished.connect(self.ramp_test_thread.deleteLater)

        self.ramp_test_thread.start()

    def update_ramp_test_progress(self, index, time_feedback):
        # Update the profile selection and time feedback
        self.comboBoxProfile.setCurrentIndex(index)
        self.labelTimeFeedback.setText(time_feedback)
        QApplication.processEvents()

    def ramp_test_finished(self):
        # Re-enable buttons
        self.buttonStart.setEnabled(True)
        self.buttonTest.setEnabled(True)
        self.buttonRampTest.setEnabled(True)
        self.buttonStop.setEnabled(False)
        self.labelConnectionStatus.setText("Ramp test completed.")

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
