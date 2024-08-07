# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_7_9.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)  # Initial size
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        # Setup group box
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        
        self.setupLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.setupLayout.addWidget(self.label)
        
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.setupLayout.addWidget(self.comboBox)
        
        self.pushButtonNext = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonNext.setFont(font)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.setupLayout.addWidget(self.pushButtonNext)
        
        self.labelStatus = QtWidgets.QLabel(self.groupBox)
        self.labelStatus.setFont(font)
        self.labelStatus.setObjectName("labelStatus")
        self.setupLayout.addWidget(self.labelStatus)
        
        self.pushButtonCalibrate = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonCalibrate.setFont(font)
        self.pushButtonCalibrate.setObjectName("pushButtonCalibrate")
        self.setupLayout.addWidget(self.pushButtonCalibrate)
        
        self.mainLayout.addWidget(self.groupBox)
        
        # Parameters group box
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")

        self.parametersLayout = QtWidgets.QGridLayout(self.groupBox_2)

        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.parametersLayout.addWidget(self.label_11, 0, 0)

        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_5.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.label_5, 0, 1)

        self.horizontalSlider_3 = QtWidgets.QSlider(self.groupBox_2)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.setMinimumSize(QtCore.QSize(300, 0))
        self.parametersLayout.addWidget(self.horizontalSlider_3, 0, 2, 1, 1)  # Combine columns 2 and 3

        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_7.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.label_7, 0, 3)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.parametersLayout.addWidget(self.lineEdit_2, 0, 4)

        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.parametersLayout.addWidget(self.label_13, 0, 5)

        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.parametersLayout.addWidget(self.label_8, 1, 0)

        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.label_4, 1, 1)

        self.horizontalSlider_2 = QtWidgets.QSlider(self.groupBox_2)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.setMinimumSize(QtCore.QSize(300, 0))
        self.parametersLayout.addWidget(self.horizontalSlider_2, 1, 2, 1, 1)  # Combine columns 2 and 3

        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_6.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.label_6, 1, 3)

        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.parametersLayout.addWidget(self.lineEdit_3, 1, 4)

        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.parametersLayout.addWidget(self.label_12, 1, 5)

        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.parametersLayout.addWidget(self.label_9, 2, 0)

        self.lineEdit_phase_diff = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_phase_diff.setFont(font)
        self.lineEdit_phase_diff.setObjectName("lineEdit_phase_diff")
        self.parametersLayout.addWidget(self.lineEdit_phase_diff, 2, 1, 1, 2)  # Span multiple columns

        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_10.setAlignment(QtCore.Qt.AlignRight)
        self.parametersLayout.addWidget(self.label_10, 2, 4)

        self.mainLayout.addWidget(self.groupBox_2)

        # Buttons
        self.buttonLayout = QtWidgets.QHBoxLayout()
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonLayout.addWidget(self.pushButton_2)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.buttonLayout.addWidget(self.pushButton_3)
        
        self.mainLayout.addLayout(self.buttonLayout)
        
        # Waveform group box
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        
        self.waveformLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        
        self.widget4 = QtWidgets.QWidget(self.groupBox_3)
        self.widget4.setMinimumHeight(300)  # Increased height for the waveform box
        self.widget4.setStyleSheet("background-color: rgb(46, 46, 46);")
        self.widget4.setObjectName("widget4")
        self.waveformLayout.addWidget(self.widget4)
        
        self.mainLayout.addWidget(self.groupBox_3, stretch=1)  # Stretch to adjust size with window
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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
        self.groupBox.setTitle(_translate("MainWindow", "Setup"))
        self.pushButtonCalibrate.setText(_translate("MainWindow", "Calibrate"))
        self.pushButtonNext.setText(_translate("MainWindow", "Refresh"))
        self.label.setText(_translate("MainWindow", "COM Port:"))
        self.labelStatus.setText(_translate("MainWindow", "Arduino connected, etc."))
        self.groupBox_2.setTitle(_translate("MainWindow", "Parameters"))
        self.label_11.setText(_translate("MainWindow", "Heart Motion"))
        self.label_5.setText(_translate("MainWindow", "Amp"))
        self.label_7.setText(_translate("MainWindow", "Freq"))
        self.label_13.setText(_translate("MainWindow", "Hz"))
        self.label_8.setText(_translate("MainWindow", "Lung Motion"))
        self.label_4.setText(_translate("MainWindow", "Amp"))
        self.label_6.setText(_translate("MainWindow", "Freq"))
        self.label_12.setText(_translate("MainWindow", "Hz"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.pushButton_3.setText(_translate("MainWindow", "Stop"))
        self.label_9.setText(_translate("MainWindow", "Phase diff (deg)"))
        self.label_10.setText(_translate("MainWindow", "Max Amplitude: x cm"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Waveform"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
