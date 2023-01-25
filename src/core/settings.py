# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Dropbox\dev\python\applications\imagetools\dev\core\settings.ui'
#
# Created: Tue Jun  3 20:44:18 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(390, 137)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsDialog.sizePolicy().hasHeightForWidth())
        SettingsDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SettingsDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(SettingsDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nthreadsBox = QtWidgets.QSpinBox(SettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nthreadsBox.sizePolicy().hasHeightForWidth())
        self.nthreadsBox.setSizePolicy(sizePolicy)
        self.nthreadsBox.setObjectName("nthreadsBox")
        self.gridLayout.addWidget(self.nthreadsBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(SettingsDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.saveThumbsCheck = QtWidgets.QCheckBox(SettingsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveThumbsCheck.sizePolicy().hasHeightForWidth())
        self.saveThumbsCheck.setSizePolicy(sizePolicy)
        self.saveThumbsCheck.setText("")
        self.saveThumbsCheck.setObjectName("saveThumbsCheck")
        self.gridLayout.addWidget(self.saveThumbsCheck, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(SettingsDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.rootfolderEdit = QtWidgets.QLineEdit(SettingsDialog)
        self.rootfolderEdit.setObjectName("rootfolderEdit")
        self.verticalLayout.addWidget(self.rootfolderEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Imagetools settings"))
        self.label.setText(_translate("SettingsDialog", "Number of threads to use for resizing:"))
        self.label_2.setText(_translate("SettingsDialog", "Save thumbnails in binary file in image folder:"))
        self.label_3.setText(_translate("SettingsDialog", "Set destination images root folder"))

