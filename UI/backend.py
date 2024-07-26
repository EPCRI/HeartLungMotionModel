from frontend import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QComboBox, QLineEdit, QLabel, QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
import sys
import time
import serial
import numpy as np
import pyqtgraph as pg
import glob
from random import randint
from scipy.signal import find_peaks
# import matplotlib.pyplot as plt

"""
README:
This script works together with fronend.py and UI_integrate_Heart_Lung.ino

This UI is currently coded to support the lead screw system design.
For the lead screw design, stepper.moveTo have the motors move in the same direction.

To support the belt-rod design, change the following parameters:
Set displacement_per_revolution to 40 value
In the arduino code, whereever there is stepper.moveTo function, make sure one is positive and one is negative.

BUGS:
Currently, the user can input the number of cm that they want to move the system in a specified direction. 
With testing, it seems that it could only complete one set of such movement, and it will get stuck or motors lose steps.
Seems like there might be an issue with communication delay. For precaution, just restart the UI for multiple position tuning.
"""
def generate_motion(t, heart_amplitude, heart_frequency, lung_amplitude, lung_frequency):
    """
    Python code to generate combined waveform consisting heart and lung sine waves
    """
    heart_motion = heart_amplitude * np.sin(2 * np.pi * heart_frequency * t)
    lung_motion = lung_amplitude * np.sin(2 * np.pi * lung_frequency * t)
    combined_motion = heart_motion + lung_motion
    return heart_motion, lung_motion, combined_motion

def encode_motor_instructions(steps):
    """
    Encoding of motor instructions by measuring displacement in between peaks of the combined waveform
    Message = "P" (start byte) + data bytes (1 sign byte, 3 hex magnitude bytes) + "V" (end byte)
    """
    data = ['P']  # Start byte 'P'
    for step in steps:
        sign = '1' if step >= 0 else '0'
        magnitude = f'{abs(step):03X}'    # mag in 3 hex bytes, sign in 1 byte, total 4 bytes per datapoint
        data.append(sign)                    
        data.append(magnitude)
    data.append('V')                      # End byte 'V'
    return ''.join(data).encode('utf-8')

displacement_per_revolution = 8 # mm
steps_per_mm = 200 / displacement_per_revolution

class Gooey(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Gooey, self).__init__(parent)
        self.setupUi(self)

        # Connect widgets to methods
        self.buttonStart.clicked.connect(self.start)
        self.buttonStop.clicked.connect(self.stop)
        self.buttonRefresh.clicked.connect(self.refresh_serial_ports)
        self.buttonWaveFormTest.clicked.connect(self.waveform_gen)
        self.buttonUp.clicked.connect(self.up_movement)
        self.buttonDown.clicked.connect(self.down_movement)

        # Default display - com ports
        if get_serial_ports() == []:
            self.labelConnectionStatus.setText("No available ports. Refresh!")
        else:
            self.labelConnectionStatus.setText("Connect to serial port.")
            self.comboBoxComPort.addItems(get_serial_ports())
        self.comboBoxComPort.activated.connect(self.connect_arduino)

    def up_movement(self):
        """
        Elevate system by user input box (input received in cm)
        """
        displacement = float(self.lineEditDisplacement.text())
        steps = displacement * 10 * steps_per_mm
        command = f"U{steps}"
        self.ser.write(command.encode())

    def down_movement(self):
        """
        Lower system by user input box (input received in cm)
        """
        displacement = float(self.lineEditDisplacement.text())
        steps = displacement * 10 * steps_per_mm
        command = f"D{steps}"
        self.ser.write(command.encode())

    def start(self):
        """
        Program the arduino with motor instructions and let it run for one period
        """
        heart_amp = float(self.lineEditHeartAmp.text())
        heart_freq = float(self.lineEditHeartFreq.text()) / 60  # In hz
        lung_amp = float(self.lineEditLungAmp.text())
        lung_freq = float(self.lineEditLungFreq.text()) / 60  # In hz

        t_fine = np.arange(0, 1 / lung_freq, 0.01)
        heart_motion, lung_motion, combined_motion = generate_motion(t_fine, heart_amp, heart_freq, lung_amp, lung_freq)
        
        peaks, _ = find_peaks(combined_motion)
        troughs, _ = find_peaks(-combined_motion)
        
        extrema_indices = np.sort(np.concatenate((peaks, troughs)))
        extrema_values = combined_motion[extrema_indices] * 10  # in mm
        
        displacements_mm = np.diff(extrema_values)
        motor_steps = np.round(displacements_mm * steps_per_mm).astype(int)
        
        return_step = -np.round((extrema_values[-1] - extrema_values[0]) * steps_per_mm).astype(int)
        motor_steps = np.append(motor_steps, return_step)
        
        motor_instructions = encode_motor_instructions(motor_steps)

        self.ser.write(motor_instructions)
   
    def stop(self): # No stop button code on arduino
        """
        Stop motors through arduino
        """
        self.ser.write('X'.encode())

    def refresh_serial_ports(self):
        """
        Refresh serial port list and update label message
        """       
        if self.ser:
            self.ser.close()

        self.comboBoxComPort.clear()
        self.labelConnectionStatus.clear()
       
        if get_serial_ports() == []:
            self.labelConnectionStatus.setText("No available ports. Refresh!")
        else:
            self.labelConnectionStatus.setText("Connect to serial port.")
            self.comboBoxComPort.addItems(get_serial_ports())

    def connect_arduino(self):
        """
        Once user select COM Port, attempt serial onnection with firmware
        """
        self.ser = serial.Serial(port = self.comboBoxComPort.currentText(), baudrate=9600, timeout=1, write_timeout=1)
        time.sleep(2)

        # Write 'T', expect to hear back 'C'
        self.ser.write('T'.encode())
        # Receive msg
        msg = self.ser.readline()
        if msg and msg == (b'C'):
            self.labelConnectionStatus.setText("Connected.")
        else:
            self.labelConnectionStatus.setText("Recheck COM Port")
            self.ser.close()

    def waveform_gen(self):
        """
        Plot waveform based on user inputs of amplitudes, freq
        """
        self.widgetWaveForm.clear()
        self.heart_amplitude = float(self.lineEditHeartAmp.text())
        print("Heart amplitude reading", self.heart_amplitude)
        self.heart_frequency = float(self.lineEditHeartFreq.text())
        self.lung_amplitude = float(self.lineEditLungAmp.text())
        self.lung_frequency = float(self.lineEditLungFreq.text())
        dt = 0.01
        wave_period = 1 / self.lung_frequency
        print("Period: ", wave_period)
        t = np.arange(0, wave_period, dt)
        heart_pen = pg.mkPen(color=(255,0,0), width=3)
        heart_motion = self.heart_amplitude * np.sin(2 * np.pi * self.heart_frequency * t)
        self.widgetWaveForm.addLegend(offset=-0.25)
        self.widgetWaveForm.plot(t, heart_motion,  pen=heart_pen, label='Heart Motion', name="Heart Motion")
        lung_pen = pg.mkPen(color=(0,255,0), width=3)
        lung_motion = self.lung_amplitude * np.sin(2 * np.pi * self.lung_frequency * t)
        self.widgetWaveForm.plot(t, lung_motion,  pen=lung_pen, label='Lung Motion', name="Lung Motion")
        combined_pen = pg.mkPen(color=(0,0,255), width=3)
        combined_motion = heart_motion + lung_motion
        self.widgetWaveForm.plot(t, combined_motion,  pen=combined_pen, label='Combined Motion', linestyle='--', name="Combined motion")
        self.widgetWaveForm.setXRange(0, wave_period)
        return heart_motion, lung_motion, combined_motion
  
def get_serial_ports():
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
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
            except (OSError):
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





