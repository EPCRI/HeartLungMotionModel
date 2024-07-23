
from frontend import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QComboBox, QLineEdit, QLabel, QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
import sys
import time
import serial
from serial.tools import list_ports
import numpy as np
import pyqtgraph as pg
from random import randint
# import matplotlib.pyplot as plt


class Gooey(QMainWindow, Ui_MainWindow): 
    def __init__(self, parent=None):
        super(Gooey, self).__init__(parent)
        self.setupUi(self)
        self.buttonStart.clicked.connect(self.Start)
        self.buttonStop.clicked.connect(self.Stop)
        # self.Calibrate_pushButton.clicked.connect(self.Calibrate)
        # self.Hard_Stop_pushButton.clicked.connect(self.Hard_Stop)
        self.buttonRefresh.clicked.connect(self.Refresh)
        # self.Connect_pushButton.clicked.connect(self.Connect)
        self.buttonWaveFormTest.clicked.connect(self.Wave)

        self.labelConnectionStatus.setText("Connect to serial port.")
        if serial_ports() == []:
            self.labelConnectionStatus.setText("No available ports. Refresh!")
        self.comboBoxComPort.addItems(serial_ports())

    def Start(self): # Start button to run motors 
        self.ser.write('P'.encode()) 
        Start = self.ser.read()
        print(Start)
    
    def Stop(self): # No stop button code on arduino 
        self.ser.write(''.encode())
        Stop = self.ser.read()
        print(Stop)

    def Refresh(self): # Refresh button to intake new COMs 
        self.comboBoxComPort.clear()
        list_of_ports = serial_ports()
        for port in list_of_ports:
            self.comboBoxComPort.addItem(port.name)

    def Connect(self): #Connect button for connecting to COMs 
        portname = self.comboBoxComPort.currentText()
        self.ser = serial.Serial(portname, baudrate=9600, timeout=1, write_timeout=1)
        time.sleep(2)
        self.ser.write('T'.encode())
        Itemscheck = self.ser.read()
        print(portname)
        print(Itemscheck)
        if Itemscheck == (b'C'):
            print ("COM connected")
        else:   
            print ("COM not connected")

    def Calibrate(self): #Calibrate button for restarting the motor start point 
        self.ser.write('C'.encode())
        Calibrate = self.ser.read()
        print(Calibrate)
        if Calibrate == (b'Y'):
            print("Calibrating")
    
    def Hard_Stop(self): #Hard stop button for if calibration goes wrong 
        self.ser.write('X'.encode())
        Hard_Stop = self.ser.read()
        print(Hard_Stop)
        if Hard_Stop == (b'Y'):
            print("Stop Calibrating")
        

    def Wave(self):
        self.widgetWaveForm.clear()
        self.heart_amplitude = float(self.lineEditHeartAmp.text())
        print("Heart amplitude reading", self.heart_amplitude)
        self.heart_frequency = float(self.lineEditHeartFreq.text())
        self.lung_amplitude = float(self.lineEditLungAmp.text())
        self.lung_frequency = float(self.lineEditLungFreq.text())
        self.Phase_Diff = float(self.lineEditPhaseDiff.text())
        dt = 0.05
        wave_period = 1 / self.lung_frequency
        print("Period: ", wave_period)
        t = np.arange(0, wave_period, dt)
        heart_pen = pg.mkPen(color=(255,0,0), width=3)
        heart_motion = self.heart_amplitude * np.sin(2 * np.pi * self.heart_frequency * t) # (self.Phase_Diff/360 * 2 * np.pi)
        self.widgetWaveForm.addLegend()
        self.widgetWaveForm.plot(t, heart_motion,  pen=heart_pen, label='Heart Motion', name="Heart Motion")
        lung_pen = pg.mkPen(color=(0,255,0), width=3)
        lung_motion = self.lung_amplitude * np.sin(2 * np.pi * self.lung_frequency * t)
        self.widgetWaveForm.plot(t, lung_motion,  pen=lung_pen, label='Lung Motion', name="Lung Motion")
        combined_pen = pg.mkPen(color=(0,0,255), width=3)
        combined_motion = heart_motion + lung_motion
        self.widgetWaveForm.plot(t, combined_motion,  pen=combined_pen, label='Combined Motion', linestyle='--', name="Combined motion")
        self.widgetWaveForm.setXRange(0, wave_period)
        return heart_motion, lung_motion, combined_motion
 
    
     
def serial_ports():
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

