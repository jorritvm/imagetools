# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\python\imagetools\src\resources\uixml\import_images.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Import(object):
    def setupUi(self, Import):
        Import.setObjectName("Import")
        Import.resize(388, 526)
        self.verticalLayout = QtWidgets.QVBoxLayout(Import)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Import)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radio_move = QtWidgets.QRadioButton(self.groupBox)
        self.radio_move.setChecked(False)
        self.radio_move.setObjectName("radio_move")
        self.gridLayout_3.addWidget(self.radio_move, 0, 0, 1, 1)
        self.radio_copy = QtWidgets.QRadioButton(self.groupBox)
        self.radio_copy.setChecked(True)
        self.radio_copy.setObjectName("radio_copy")
        self.gridLayout_3.addWidget(self.radio_copy, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Import)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_destination = QtWidgets.QLineEdit(self.groupBox_2)
        self.edit_destination.setObjectName("edit_destination")
        self.horizontalLayout.addWidget(self.edit_destination)
        self.btn_folder_select = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_folder_select.sizePolicy().hasHeightForWidth())
        self.btn_folder_select.setSizePolicy(sizePolicy)
        self.btn_folder_select.setMaximumSize(QtCore.QSize(32, 32))
        self.btn_folder_select.setObjectName("btn_folder_select")
        self.horizontalLayout.addWidget(self.btn_folder_select)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.btn_import = QtWidgets.QPushButton(Import)
        self.btn_import.setObjectName("btn_import")
        self.verticalLayout.addWidget(self.btn_import)
        self.progress_bar = QtWidgets.QProgressBar(Import)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout.addWidget(self.progress_bar)
        self.text = QtWidgets.QTextBrowser(Import)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.btn_goto = QtWidgets.QPushButton(Import)
        self.btn_goto.setObjectName("btn_goto")
        self.verticalLayout.addWidget(self.btn_goto)

        self.retranslateUi(Import)
        QtCore.QMetaObject.connectSlotsByName(Import)

    def retranslateUi(self, Import):
        _translate = QtCore.QCoreApplication.translate
        Import.setWindowTitle(_translate("Import", "Import"))
        self.groupBox.setTitle(_translate("Import", "Preferences"))
        self.radio_move.setText(_translate("Import", "Move"))
        self.radio_copy.setText(_translate("Import", "Copy"))
        self.groupBox_2.setTitle(_translate("Import", "Destination: "))
        self.btn_folder_select.setText(_translate("Import", "..."))
        self.btn_import.setText(_translate("Import", "Import"))
        self.btn_goto.setText(_translate("Import", "Take me to the new folder..."))
