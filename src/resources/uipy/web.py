# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\python\imagetools\src\resources\uixml\web.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WebAlbum(object):
    def setupUi(self, WebAlbum):
        WebAlbum.setObjectName("WebAlbum")
        WebAlbum.resize(312, 280)
        self.gridLayout = QtWidgets.QGridLayout(WebAlbum)
        self.gridLayout.setObjectName("gridLayout")
        self.editTitle = QtWidgets.QLineEdit(WebAlbum)
        self.editTitle.setObjectName("editTitle")
        self.gridLayout.addWidget(self.editTitle, 0, 1, 1, 1)
        self.editLocation = QtWidgets.QLineEdit(WebAlbum)
        self.editLocation.setObjectName("editLocation")
        self.gridLayout.addWidget(self.editLocation, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(WebAlbum)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.editDescription = QtWidgets.QLineEdit(WebAlbum)
        self.editDescription.setObjectName("editDescription")
        self.gridLayout.addWidget(self.editDescription, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(WebAlbum)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(WebAlbum)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.btnCreate = QtWidgets.QPushButton(WebAlbum)
        self.btnCreate.setObjectName("btnCreate")
        self.gridLayout.addWidget(self.btnCreate, 3, 0, 1, 2)
        self.btnCancel = QtWidgets.QPushButton(WebAlbum)
        self.btnCancel.setObjectName("btnCancel")
        self.gridLayout.addWidget(self.btnCancel, 4, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(WebAlbum)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 2)
        self.textBox = QtWidgets.QTextBrowser(WebAlbum)
        self.textBox.setObjectName("textBox")
        self.gridLayout.addWidget(self.textBox, 6, 0, 1, 2)

        self.retranslateUi(WebAlbum)
        QtCore.QMetaObject.connectSlotsByName(WebAlbum)
        WebAlbum.setTabOrder(self.editTitle, self.editDescription)
        WebAlbum.setTabOrder(self.editDescription, self.editLocation)
        WebAlbum.setTabOrder(self.editLocation, self.btnCreate)
        WebAlbum.setTabOrder(self.btnCreate, self.btnCancel)
        WebAlbum.setTabOrder(self.btnCancel, self.textBox)

    def retranslateUi(self, WebAlbum):
        _translate = QtCore.QCoreApplication.translate
        WebAlbum.setWindowTitle(_translate("WebAlbum", "Web Album Generator"))
        self.label_3.setText(_translate("WebAlbum", "Location"))
        self.label_2.setText(_translate("WebAlbum", "Album Description"))
        self.label.setText(_translate("WebAlbum", "Album Title"))
        self.btnCreate.setText(_translate("WebAlbum", "Create webalbum"))
        self.btnCancel.setText(_translate("WebAlbum", "Cancel"))
