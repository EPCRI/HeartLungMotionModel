# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_7_9.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(869, 536)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 691, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 670, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Serial_Connection_pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.Serial_Connection_pushButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Serial_Connection_pushButton.sizePolicy().hasHeightForWidth())
        self.Serial_Connection_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Serial_Connection_pushButton.setFont(font)
        self.Serial_Connection_pushButton.setIconSize(QtCore.QSize(30, 14))
        self.Serial_Connection_pushButton.setObjectName("Serial_Connection_pushButton")
        self.gridLayout.addWidget(self.Serial_Connection_pushButton, 0, 2, 1, 1)
        self.COM_Port_comboBox = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.COM_Port_comboBox.sizePolicy().hasHeightForWidth())
        self.COM_Port_comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.COM_Port_comboBox.setFont(font)
        self.COM_Port_comboBox.setObjectName("COM_Port_comboBox")
        self.gridLayout.addWidget(self.COM_Port_comboBox, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
        self.Calibrate_pushButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calibrate_pushButton.sizePolicy().hasHeightForWidth())
        self.Calibrate_pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Calibrate_pushButton.setFont(font)
        self.Calibrate_pushButton.setIconSize(QtCore.QSize(30, 30))
        self.Calibrate_pushButton.setObjectName("Calibrate_pushButton")
        self.gridLayout.addWidget(self.Calibrate_pushButton, 0, 6, 1, 1)
        self.Connect_pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.Connect_pushButton.setObjectName("Connect_pushButton")
        self.gridLayout.addWidget(self.Connect_pushButton, 0, 3, 1, 1)
        self.Hard_Stop_pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.Hard_Stop_pushButton.setObjectName("Hard_Stop_pushButton")
        self.gridLayout.addWidget(self.Hard_Stop_pushButton, 0, 7, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 70, 691, 191))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 20, 601, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_9.addWidget(self.label_7, 0, 6, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_13.setObjectName("label_13")
        self.gridLayout_9.addWidget(self.label_13, 0, 8, 1, 1)
        self.Heart_Freq_Input_lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Heart_Freq_Input_lineEdit.setFont(font)
        self.Heart_Freq_Input_lineEdit.setObjectName("Heart_Freq_Input_lineEdit")
        self.gridLayout_9.addWidget(self.Heart_Freq_Input_lineEdit, 0, 7, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_9.addWidget(self.label_11, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(97, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem1, 0, 5, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_9.addWidget(self.label_5, 0, 2, 1, 1)
        self.Heart_Amp_Input_lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.Heart_Amp_Input_lineEdit.setObjectName("Heart_Amp_Input_lineEdit")
        self.gridLayout_9.addWidget(self.Heart_Amp_Input_lineEdit, 0, 3, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget2.setGeometry(QtCore.QRect(50, 60, 601, 25))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 7, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 5, 1, 1)
        self.Lung_Freq_Input_lineEdit = QtWidgets.QLineEdit(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Lung_Freq_Input_lineEdit.setFont(font)
        self.Lung_Freq_Input_lineEdit.setObjectName("Lung_Freq_Input_lineEdit")
        self.gridLayout_3.addWidget(self.Lung_Freq_Input_lineEdit, 0, 6, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 1, 1, 1)
        self.Lung_Amp_Input_lineEdit = QtWidgets.QLineEdit(self.layoutWidget2)
        self.Lung_Amp_Input_lineEdit.setObjectName("Lung_Amp_Input_lineEdit")
        self.gridLayout_3.addWidget(self.Lung_Amp_Input_lineEdit, 0, 3, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget3.setGeometry(QtCore.QRect(150, 140, 391, 51))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.Stop_pushButton = QtWidgets.QPushButton(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Stop_pushButton.setFont(font)
        self.Stop_pushButton.setObjectName("Stop_pushButton")
        self.gridLayout_5.addWidget(self.Stop_pushButton, 0, 1, 1, 1)
        self.Start_pushButton = QtWidgets.QPushButton(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Start_pushButton.setFont(font)
        self.Start_pushButton.setObjectName("Start_pushButton")
        self.gridLayout_5.addWidget(self.Start_pushButton, 0, 0, 1, 1)
        self.Wave_Form_Test_pushButton = QtWidgets.QPushButton(self.layoutWidget3)
        self.Wave_Form_Test_pushButton.setObjectName("Wave_Form_Test_pushButton")
        self.gridLayout_5.addWidget(self.Wave_Form_Test_pushButton, 0, 2, 1, 1)
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget4.setGeometry(QtCore.QRect(50, 100, 601, 27))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(79, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 0, 1, 1, 1)
        self.Phase_diff_lineEdit = QtWidgets.QLineEdit(self.layoutWidget4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Phase_diff_lineEdit.sizePolicy().hasHeightForWidth())
        self.Phase_diff_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Phase_diff_lineEdit.setFont(font)
        self.Phase_diff_lineEdit.setObjectName("Phase_diff_lineEdit")
        self.gridLayout_4.addWidget(self.Phase_diff_lineEdit, 0, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem5 = QtWidgets.QSpacerItem(102, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem5, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_6.addWidget(self.label_10, 0, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_6, 0, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 270, 851, 231))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.Wave_widget = pg.PlotWidget(self.groupBox_3)
        styles = {"color": "black", "font-size": "15px"}
        self.Wave_widget.setLabel("left", "Amp HZ", **styles)
        self.Wave_widget.setLabel("bottom", "Freq HZ", **styles)
        self.Wave_widget.setTitle("Combined Heart Lung Motion", color="k", size="12pt")
        self.Wave_widget.setBackground("w")
        self.Wave_widget.setGeometry(QtCore.QRect(0, 20, 731, 161))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 869, 21))
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
        self.Serial_Connection_pushButton.setText(_translate("MainWindow", "Refresh"))
        self.label.setText(_translate("MainWindow", "COM Port:"))
        self.label_2.setText(_translate("MainWindow", "Arduino connected, etc."))
        self.Calibrate_pushButton.setText(_translate("MainWindow", "Calibrate"))
        self.Connect_pushButton.setText(_translate("MainWindow", "Connect"))
        self.Hard_Stop_pushButton.setText(_translate("MainWindow", "Hard Stop"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Parameters"))
        self.label_7.setText(_translate("MainWindow", "Freq"))
        self.label_13.setText(_translate("MainWindow", "Hz"))
        self.label_11.setText(_translate("MainWindow", "Heart Motion"))
        self.label_5.setText(_translate("MainWindow", "Amp"))
        self.label_12.setText(_translate("MainWindow", "Hz"))
        self.label_6.setText(_translate("MainWindow", "Freq"))
        self.label_8.setText(_translate("MainWindow", "Lung Motion"))
        self.label_4.setText(_translate("MainWindow", "Amp"))
        self.Stop_pushButton.setText(_translate("MainWindow", "Stop"))
        self.Start_pushButton.setText(_translate("MainWindow", "Start"))
        self.Wave_Form_Test_pushButton.setText(_translate("MainWindow", "Wave Form Test"))
        self.label_9.setText(_translate("MainWindow", "Phase diff (deg)"))
        self.label_10.setText(_translate("MainWindow", "Max Amplitude: x cm"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Waveform"))
