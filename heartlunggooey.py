
from maincontrol import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QComboBox
from PyQt5.QtGui import QIcon
import sys
import time
import serial
from serial.tools import list_ports

class Gooey(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Gooey, self).__init__(parent)
        self.setupUi(self)
        self.Start_pushButton.clicked.connect(self.Start)
        self.Stop_pushButton.clicked.connect(self.Stop)
        self.Calibrate_pushButton.clicked.connect(self.Calibrate)
        self.Serial_Connection_pushButton.clicked.connect(self.Refresh)
        self.Connect_pushButton.clicked.connect(self.Connect)
        self.Heart_Amp_Input_lineEdit.textChanged.connect(self.Heart_Amp_Text)
        self.Heart_Freq_Input_lineEdit.textChanged.connect(self.Heart_Freq_Text)
        self.Lung_Amp_Input_lineEdit.textChanged.connect(self.Lung_Amp_Text)
        self.Lung_Freq_Input_lineEdit.textChanged.connect(self.Lung_Freq_Text)
        self.Phase_diff_lineEdit.textChanged.connect(self.Phase_Diff)
    def Start(self):
        pass 
    
    def Stop(self):
        pass

    def Refresh(self):
        self.COM_Port_comboBox.clear()
        list_of_ports = serial.tools.list_ports.comports()
        print (list_of_ports)
        for port in list_of_ports:
            self.COM_Port_comboBox.addItem(port.name)

    def Connect(self):
        # comment
        portname = self.COM_Port_comboBox.currentText()
        ser = serial.Serial(portname, baudrate=9600, timeout=1, write_timeout=1)
        time.sleep(2)
        ser.write('T'.encode())
        Itemscheck = ser.read()
        print(portname)
        print(Itemscheck)
        if Itemscheck == (b'C'):
            print ("COM connected")
        else:   
            print ("COM not connected")

    def Calibrate(self):
        pass
    
    def Heart_Amp_Text(self):
        pass 

    def Heart_Freq_Text(self):
        pass

    def Lung_Amp_Text(self):
        pass

    def Lung_Freq_Text(self):
        pass

    def Phase_Diff(self):
        pass

def main():
    app = QApplication(sys.argv)
    form = Gooey()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
