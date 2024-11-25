# frontend.py
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

"""
PyQt5 frontend design that works with backend.py for full functionality.

Author: Wendy Tan
Date: 11/24/2024
"""

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)  # Window size
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Font settings
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)

        # Groupbox setup
        self.groupBoxSetup = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxSetup.setFont(font)
        self.groupBoxSetup.setObjectName("groupBoxSetup")

        self.setupLayout = QtWidgets.QHBoxLayout(self.groupBoxSetup)
        self.labelComPort = QtWidgets.QLabel(self.groupBoxSetup)
        self.labelComPort.setFont(font)
        self.labelComPort.setObjectName("labelComPort")
        self.setupLayout.addWidget(self.labelComPort)

        self.comboBoxComPort = QtWidgets.QComboBox(self.groupBoxSetup)
        self.comboBoxComPort.setFont(font)
        self.comboBoxComPort.setObjectName("comboBoxComPort")
        self.setupLayout.addWidget(self.comboBoxComPort)

        self.buttonRefresh = QtWidgets.QPushButton(self.groupBoxSetup)
        self.buttonRefresh.setFont(font)
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.setupLayout.addWidget(self.buttonRefresh)

        self.labelConnectionStatus = QtWidgets.QLabel(self.groupBoxSetup)
        self.labelConnectionStatus.setFont(font)
        self.labelConnectionStatus.setObjectName("labelConnectionStatus")
        self.setupLayout.addWidget(self.labelConnectionStatus)

        self.mainLayout.addWidget(self.groupBoxSetup)

        # Calibrate group box
        self.groupBoxCalibrate = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxCalibrate.setFont(font)
        self.groupBoxCalibrate.setObjectName("groupBoxCalibrate")

        self.calibrateLayout = QtWidgets.QHBoxLayout(self.groupBoxCalibrate)
        self.labelDisplacement = QtWidgets.QLabel(self.groupBoxCalibrate)
        self.labelDisplacement.setFont(font)
        self.labelDisplacement.setObjectName("labelDisplacement")
        self.calibrateLayout.addWidget(self.labelDisplacement)

        self.lineEditDisplacement = QtWidgets.QLineEdit(self.groupBoxCalibrate)
        self.lineEditDisplacement.setFont(font)
        self.lineEditDisplacement.setObjectName("lineEditDisplacement")
        self.calibrateLayout.addWidget(self.lineEditDisplacement)

        self.buttonUp = QtWidgets.QPushButton(self.groupBoxCalibrate)
        self.buttonUp.setFont(font)
        self.buttonUp.setFixedSize(220, 40)
        self.buttonUp.setObjectName("buttonUp")
        self.calibrateLayout.addWidget(self.buttonUp)

        self.buttonDown = QtWidgets.QPushButton(self.groupBoxCalibrate)
        self.buttonDown.setFont(font)
        self.buttonDown.setFixedSize(220, 40)
        self.buttonDown.setObjectName("buttonDown")
        self.calibrateLayout.addWidget(self.buttonDown)

        self.mainLayout.addWidget(self.groupBoxCalibrate)

        # Parameters group box
        self.groupBoxParameters = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxParameters.setFont(font)
        self.groupBoxParameters.setObjectName("groupBoxParameters")

        self.parametersLayout = QtWidgets.QGridLayout(self.groupBoxParameters)

        # Add Profile Selection Label and ComboBox
        self.labelProfile = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelProfile.setFont(font)
        self.labelProfile.setObjectName("labelProfile")
        self.parametersLayout.addWidget(self.labelProfile, 0, 0)

        self.comboBoxProfile = QtWidgets.QComboBox(self.groupBoxParameters)
        self.comboBoxProfile.setFont(font)
        self.comboBoxProfile.setObjectName("comboBoxProfile")
        self.parametersLayout.addWidget(self.comboBoxProfile, 0, 1, 1, 4)

        # Label for Max Amplitude
        self.labelMaxAmp = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelMaxAmp.setFont(font)
        self.labelMaxAmp.setObjectName("labelMaxAmp")
        self.labelMaxAmp.setAlignment(QtCore.Qt.AlignLeft)
        self.parametersLayout.addWidget(self.labelMaxAmp, 1, 0, 1, 2)

        # Label for Time Feedback
        self.labelTimeFeedback = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelTimeFeedback.setFont(font)
        self.labelTimeFeedback.setObjectName("labelTimeFeedback")
        self.labelTimeFeedback.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.labelTimeFeedback, 1, 2, 1, 3)

        self.mainLayout.addWidget(self.groupBoxParameters)

        # Button Layout
        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.buttonStart = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStart.setFont(font)
        self.buttonStart.setObjectName("buttonStart")
        self.buttonLayout.addWidget(self.buttonStart)

        self.buttonStop = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStop.setFont(font)
        self.buttonStop.setObjectName("buttonStop")
        self.buttonLayout.addWidget(self.buttonStop)

        self.buttonTest = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTest.setFont(font)
        self.buttonTest.setObjectName("buttonTest")
        self.buttonLayout.addWidget(self.buttonTest)

        self.buttonRampTest = QtWidgets.QPushButton(self.centralwidget)
        self.buttonRampTest.setFont(font)
        self.buttonRampTest.setObjectName("buttonRampTest")
        self.buttonLayout.addWidget(self.buttonRampTest)

        self.mainLayout.addLayout(self.buttonLayout)

        # Waveform group box
        self.groupBoxWaveForm = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxWaveForm.setFont(font)
        self.groupBoxWaveForm.setObjectName("groupBoxWaveForm")
        self.groupBoxWaveForm.setMinimumHeight(350) 
        self.waveformLayout = QtWidgets.QVBoxLayout(self.groupBoxWaveForm)

        self.widgetWaveForm = pg.PlotWidget(self.groupBoxWaveForm)
        styles = {"color": "black", "font-size": "15px"}
        self.widgetWaveForm.setLabel("left", "Amplitude (cm)", **styles)
        self.widgetWaveForm.setLabel("bottom", "Time (s)", **styles)
        self.widgetWaveForm.setTitle("Combined Heart Lung Motion", color="k", size="12pt")
        self.widgetWaveForm.setBackground("w")
        self.waveformLayout.addWidget(self.widgetWaveForm)

        self.mainLayout.addWidget(self.groupBoxWaveForm, stretch=1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Heart Lung Motion Simulator"))
        self.groupBoxSetup.setTitle(_translate("MainWindow", "Setup"))
        self.buttonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.labelComPort.setText(_translate("MainWindow", "COM Port:"))
        self.labelConnectionStatus.setText(_translate("MainWindow", "Arduino connected, etc."))
        self.groupBoxCalibrate.setTitle(_translate("MainWindow", "Calibrate"))
        self.labelDisplacement.setText(_translate("MainWindow", "Displacement (cm):"))
        self.buttonUp.setText(_translate("MainWindow", "Up"))
        self.buttonDown.setText(_translate("MainWindow", "Down"))
        self.groupBoxParameters.setTitle(_translate("MainWindow", "Parameters"))
        self.labelProfile.setText(_translate("MainWindow", "Select Profile:"))
        self.labelMaxAmp.setText(_translate("MainWindow", "Pk-pk amplitude: x cm"))
        self.labelTimeFeedback.setText(_translate("MainWindow", "Time feedback: x ms"))
        self.buttonStart.setText(_translate("MainWindow", "Start"))
        self.buttonStop.setText(_translate("MainWindow", "Stop"))
        self.buttonTest.setText(_translate("MainWindow", "Test"))
        self.buttonRampTest.setText(_translate("MainWindow", "Ramp Test"))
        self.groupBoxWaveForm.setTitle(_translate("MainWindow", "Waveform"))
