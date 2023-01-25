# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Dropbox\dev\python\applications\imagetools\dev\imageoperations\Numberui.ui'
#
# Created: Tue Jun  3 20:44:46 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Number(object):
    def setupUi(self, Number):
        Number.setObjectName("Number")
        Number.resize(262, 211)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Number.sizePolicy().hasHeightForWidth())
        Number.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Number)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(Number)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName("gridlayout")
        self.radioPre = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioPre.setObjectName("radioPre")
        self.gridlayout.addWidget(self.radioPre, 0, 0, 1, 1)
        self.radioSuff = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioSuff.setObjectName("radioSuff")
        self.gridlayout.addWidget(self.radioSuff, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 1, 0, 1, 1)
        self._2 = QtWidgets.QHBoxLayout()
        self._2.setObjectName("_2")
        self.spinDigits = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinDigits.setMaximum(3)
        self.spinDigits.setObjectName("spinDigits")
        self._2.addWidget(self.spinDigits)
        spacerItem = QtWidgets.QSpacerItem(34, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._2.addItem(spacerItem)
        self.gridlayout.addLayout(self._2, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.editLineSeparator = QtWidgets.QLineEdit(self.groupBox_2)
        self.editLineSeparator.setObjectName("editLineSeparator")
        self.gridlayout.addWidget(self.editLineSeparator, 2, 1, 1, 1)
        self.checkKeepOldName = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkKeepOldName.setObjectName("checkKeepOldName")
        self.gridlayout.addWidget(self.checkKeepOldName, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(Number)
        self.groupBox_3.setObjectName("groupBox_3")
        self._3 = QtWidgets.QGridLayout(self.groupBox_3)
        self._3.setObjectName("_3")
        self.buttonStartNumbering = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonStartNumbering.sizePolicy().hasHeightForWidth())
        self.buttonStartNumbering.setSizePolicy(sizePolicy)
        self.buttonStartNumbering.setMinimumSize(QtCore.QSize(125, 0))
        self.buttonStartNumbering.setObjectName("buttonStartNumbering")
        self._3.addWidget(self.buttonStartNumbering, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.retranslateUi(Number)
        QtCore.QMetaObject.connectSlotsByName(Number)

    def retranslateUi(self, Number):
        _translate = QtCore.QCoreApplication.translate
        Number.setWindowTitle(_translate("Number", "Number Images"))
        self.groupBox_2.setTitle(_translate("Number", "Options"))
        self.radioPre.setText(_translate("Number", "Prefix"))
        self.radioSuff.setText(_translate("Number", "Suffix"))
        self.label.setText(_translate("Number", "Digits:"))
        self.label_2.setText(_translate("Number", "Separator:"))
        self.editLineSeparator.setText(_translate("Number", "-"))
        self.checkKeepOldName.setText(_translate("Number", "Keep old filename"))
        self.groupBox_3.setTitle(_translate("Number", "Numbering"))
        self.buttonStartNumbering.setText(_translate("Number", "Start!"))

