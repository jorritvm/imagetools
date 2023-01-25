# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Dropbox\dev\python\applications\imagetools\dev\imageoperations\Importui.ui'
#
# Created: Tue Jun  3 20:44:44 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Import(object):
    def setupUi(self, Import):
        Import.setObjectName("Import")
        Import.resize(264, 456)
        self.gridLayout_4 = QtWidgets.QGridLayout(Import)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(Import)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Import)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioMove = QtWidgets.QRadioButton(self.groupBox)
        self.radioMove.setChecked(True)
        self.radioMove.setObjectName("radioMove")
        self.gridLayout_3.addWidget(self.radioMove, 0, 0, 1, 1)
        self.radioCopy = QtWidgets.QRadioButton(self.groupBox)
        self.radioCopy.setObjectName("radioCopy")
        self.gridLayout_3.addWidget(self.radioCopy, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Import)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.editDestination = QtWidgets.QLineEdit(self.groupBox_2)
        self.editDestination.setObjectName("editDestination")
        self.gridLayout_2.addWidget(self.editDestination, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 2, 0, 1, 1)
        self.btnImport = QtWidgets.QPushButton(Import)
        self.btnImport.setObjectName("btnImport")
        self.gridLayout_4.addWidget(self.btnImport, 3, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Import)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_4.addWidget(self.progressBar, 4, 0, 1, 1)
        self.text = QtWidgets.QTextBrowser(Import)
        self.text.setObjectName("text")
        self.gridLayout_4.addWidget(self.text, 5, 0, 1, 1)
        self.btnGoto = QtWidgets.QPushButton(Import)
        self.btnGoto.setObjectName("btnGoto")
        self.gridLayout_4.addWidget(self.btnGoto, 6, 0, 1, 1)

        self.retranslateUi(Import)
        QtCore.QMetaObject.connectSlotsByName(Import)

    def retranslateUi(self, Import):
        _translate = QtCore.QCoreApplication.translate
        Import.setWindowTitle(_translate("Import", "Import"))
        self.groupBox_3.setTitle(_translate("Import", "Note"))
        self.label.setText(_translate("Import", "This will include all .CR2 files..."))
        self.groupBox.setTitle(_translate("Import", "Preferences"))
        self.radioMove.setText(_translate("Import", "Move"))
        self.radioCopy.setText(_translate("Import", "Copy"))
        self.groupBox_2.setTitle(_translate("Import", "Destination: "))
        self.btnImport.setText(_translate("Import", "Import"))
        self.btnGoto.setText(_translate("Import", "Take me to the new folder..."))

