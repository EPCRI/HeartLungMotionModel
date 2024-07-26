from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

"""
README:
UI design that works with backend.py
"""
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)  # Window size
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Groupbox setup
        self.groupBoxSetup = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
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

        self.labelHeartText = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelHeartText.setFont(font)
        self.labelHeartText.setObjectName("labelHeartText")
        self.parametersLayout.addWidget(self.labelHeartText, 0, 0)

        self.labelAmpHeart = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelAmpHeart.setFont(font)
        self.labelAmpHeart.setObjectName("labelAmpHeart")
        self.labelAmpHeart.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.labelAmpHeart, 0, 1)

        self.lineEditHeartAmp = QtWidgets.QLineEdit(self.groupBoxParameters)
        self.lineEditHeartAmp.setFont(font)
        self.lineEditHeartAmp.setObjectName("lineEditHeartAmp")
        self.parametersLayout.addWidget(self.lineEditHeartAmp, 0, 2)

        self.labelFreqHeart = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelFreqHeart.setFont(font)
        self.labelFreqHeart.setObjectName("labelFreqHeart")
        self.labelFreqHeart.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.labelFreqHeart, 0, 3)

        self.lineEditHeartFreq = QtWidgets.QLineEdit(self.groupBoxParameters)
        self.lineEditHeartFreq.setFont(font)
        self.lineEditHeartFreq.setObjectName("lineEditHeartFreq")
        self.parametersLayout.addWidget(self.lineEditHeartFreq, 0, 4)

        self.labelbpmHeart = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelbpmHeart.setFont(font)
        self.labelbpmHeart.setObjectName("labelbpmHeart")
        self.parametersLayout.addWidget(self.labelbpmHeart, 0, 5)

        self.labelLungText = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelLungText.setFont(font)
        self.labelLungText.setObjectName("labelLungText")
        self.parametersLayout.addWidget(self.labelLungText, 1, 0)

        self.labelAmpLung = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelAmpLung.setFont(font)
        self.labelAmpLung.setObjectName("labelAmpLung")
        self.labelAmpLung.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.labelAmpLung, 1, 1)

        self.lineEditLungAmp = QtWidgets.QLineEdit(self.groupBoxParameters)
        self.lineEditLungAmp.setFont(font)
        self.lineEditLungAmp.setObjectName("lineEditLungAmp")
        self.parametersLayout.addWidget(self.lineEditLungAmp, 1, 2)

        self.labelFreqLung = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelFreqLung.setFont(font)
        self.labelFreqLung.setObjectName("labelFreqLung")
        self.labelFreqLung.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.labelFreqLung, 1, 3)

        self.lineEditLungFreq = QtWidgets.QLineEdit(self.groupBoxParameters)
        self.lineEditLungFreq.setFont(font)
        self.lineEditLungFreq.setObjectName("lineEditLungFreq")
        self.parametersLayout.addWidget(self.lineEditLungFreq, 1, 4)

        self.labelbpmLung = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelbpmLung.setFont(font)
        self.labelbpmLung.setObjectName("labelbpmLung")
        self.parametersLayout.addWidget(self.labelbpmLung, 1, 5)

        self.labelDistRevol = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelDistRevol.setFont(font)
        self.labelDistRevol.setObjectName("labelDistRevol")
        self.parametersLayout.addWidget(self.labelDistRevol, 2, 0)

        self.lineEditDistRevol = QtWidgets.QLineEdit(self.groupBoxParameters)
        self.lineEditDistRevol.setFont(font)
        self.lineEditDistRevol.setObjectName("lineEditDistRevol")
        self.parametersLayout.addWidget(self.lineEditDistRevol, 2, 1, 1, 2)  # Span multiple columns

        self.labelMaxAmp = QtWidgets.QLabel(self.groupBoxParameters)
        self.labelMaxAmp.setFont(font)
        self.labelMaxAmp.setObjectName("labelMaxAmp")
        self.labelMaxAmp.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.labelMaxAmp, 2, 4)

        self.mainLayout.addWidget(self.groupBoxParameters)


        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.buttonStart = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStart.setFont(font)
        self.buttonStart.setObjectName("buttonStart")
        self.buttonLayout.addWidget(self.buttonStart)

        self.buttonStop = QtWidgets.QPushButton(self.centralwidget)
        self.buttonStop.setFont(font)
        self.buttonStop.setObjectName("buttonStop")
        self.buttonLayout.addWidget(self.buttonStop)
    
        self.buttonWaveFormTest = QtWidgets.QPushButton(self.centralwidget)
        self.buttonWaveFormTest.setFont(font)
        self.buttonWaveFormTest.setObjectName("buttonWaveFormTest")
        self.buttonLayout.addWidget(self.buttonWaveFormTest)

        self.mainLayout.addLayout(self.buttonLayout)

        # Waveform group box
        self.groupBoxWaveForm = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxWaveForm.setFont(font)
        self.groupBoxWaveForm.setObjectName("groupBoxWaveForm")
        self.groupBoxWaveForm.setMinimumHeight(350)  # Adjust the height as needed
        self.waveformLayout = QtWidgets.QVBoxLayout(self.groupBoxWaveForm)

        self.widgetWaveForm = pg.PlotWidget(self.groupBoxWaveForm)
        styles = {"color": "black", "font-size": "15px"}
        self.widgetWaveForm.setLabel("left", "Amp HZ", **styles)
        self.widgetWaveForm.setLabel("bottom", "Freq HZ", **styles)
        self.widgetWaveForm.setTitle("Combined Heart Lung Motion", color="k", size="12pt")
        self.widgetWaveForm.setBackground("w")
        self.waveformLayout.addWidget(self.widgetWaveForm)

        self.mainLayout.addWidget(self.groupBoxWaveForm, stretch=1)  # Stretch to adjust size with window

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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBoxSetup.setTitle(_translate("MainWindow", "Setup"))
        self.buttonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.labelComPort.setText(_translate("MainWindow", "COM Port:"))
        self.labelConnectionStatus.setText(_translate("MainWindow", "Arduino connected, etc."))
        self.groupBoxCalibrate.setTitle(_translate("MainWindow", "Calibrate"))
        self.labelDisplacement.setText(_translate("MainWindow", "Displacement (cm):"))
        self.buttonUp.setText(_translate("MainWindow", "Up"))
        self.buttonDown.setText(_translate("MainWindow", "Down"))
        self.groupBoxParameters.setTitle(_translate("MainWindow", "Parameters"))
        self.labelHeartText.setText(_translate("MainWindow", "Heart Motion"))
        self.labelAmpHeart.setText(_translate("MainWindow", "Amp"))
        self.labelFreqHeart.setText(_translate("MainWindow", "Freq"))
        self.labelbpmHeart.setText(_translate("MainWindow", "bpm"))
        self.labelLungText.setText(_translate("MainWindow", "Lung Motion"))
        self.labelAmpLung.setText(_translate("MainWindow", "Amp"))
        self.labelFreqLung.setText(_translate("MainWindow", "Freq"))
        self.labelbpmLung.setText(_translate("MainWindow", "bpm"))
        self.buttonStart.setText(_translate("MainWindow", "Start"))
        self.buttonStop.setText(_translate("MainWindow", "Stop"))
        self.buttonWaveFormTest.setText(_translate("MainWindow", "Waveform Test"))
        self.labelDistRevol.setText(_translate("MainWindow", "Distance per rev. (mm)"))
        self.labelMaxAmp.setText(_translate("MainWindow", "Max Amplitude: x cm"))
        self.groupBoxWaveForm.setTitle(_translate("MainWindow", "Waveform"))


