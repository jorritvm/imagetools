'''
Created on 17-okt.-2013

@author: jorrit
'''

import os
from ftplib import *

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ui.designer.upload import *


class Upload(QDialog, Ui_Upload):

    def __init__(self, settings, root, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setupSlots()

        self.root = root
        self.settings = settings
        self.currentItem = "<new>"
        self.loadPresets()
        self.suggestFolderName()

        self.fu = FileUploader()
        self.fu.uploadDone.connect(self.uploadDone)

    def debug(self):
        print(self.settings)

    def setupSlots(self):
        self.btnSave.clicked.connect(self.savePreset)
        self.btnLoad.clicked.connect(self.loadPreset)
        self.btnDel.clicked.connect(self.delPreset)
        self.btnUpload.clicked.connect(self.upload)

    def loadPresets(self):
        self.comboPreset.clear()
        self.comboPreset.addItem("<new>")
        if "FTP" in self.settings.keys():
            x = self.settings['FTP']
            for d in sorted(x):  # sort keys
                self.comboPreset.addItem(d)
        i = self.comboPreset.findText(self.currentItem)
        if i > 0:
            self.comboPreset.setCurrentIndex(i)

    def loadPreset(self):
        t = self.comboPreset.currentText()
        if t == "<new>":
            self.editIP.clear()
            self.editPort.clear()
            self.editUser.clear()
            self.editPassword.clear()
            self.editDirectory.clear()
        else:
            d = self.settings["FTP"][t]
            self.editIP.setText(d["ip"])
            self.editPort.setText(d["port"])
            self.editUser.setText(d["user"])
            self.editPassword.setText(d["pass"])
            self.editDirectory.setText(d["folder"])

    def savePreset(self):
        x = dict()
        x['ip'] = self.editIP.text()
        x['port'] = self.editPort.text()
        x['user'] = self.editUser.text()
        x['pass'] = self.editPassword.text()
        x['folder'] = self.editDirectory.text()

        preset = ""
        if self.comboPreset.currentText() == "<new>":
            y = QInputDialog.getText(self, 'Preset name', 'Give a name for this preset')
            if y[1]:
                preset = y[0]
        else:
            preset = self.comboPreset.currentText()
        if preset != "":
            # save it to the settings dict
            if "FTP" in self.settings.keys():
                self.settings['FTP'][preset] = x
            else:
                z = dict()
                z[preset] = x
                self.settings['FTP'] = z
            self.currentItem = preset

        self.loadPresets()

    def delPreset(self):
        if self.comboPreset.currentText() != "<new>":
            preset = self.comboPreset.currentText()
            self.settings["FTP"].pop(preset)
            self.currentItem = "<new>"
            i = self.comboPreset.findText(preset)
            self.comboPreset.removeItem(i)
            self.comboPreset.setCurrentIndex(0)

    def suggestFolderName(self):
        d = QDir(self.root)
        while d.cdUp():
            n = d.dirName()
            if n[0:4].isdigit():
                self.editNewFolderName.setText(n)
                break

    def log(self, s):
        self.textLog.append(s)

    def upload(self):
        ip = self.editIP.text()
        port = int(self.editPort.text())
        user = self.editUser.text()
        pwd = self.editPassword.text()
        fol = self.editDirectory.text()
        newfol = self.editNewFolderName.text()

        healthy = True
        ftp = FTP()
        ftp.connect(ip, port)
        self.log("USER " + user)
        self.log("PASS")
        reply = ftp.login(user, pwd)
        self.log(reply)

        if fol != "":
            try:
                self.log("CWD " + fol)
                reply = ftp.cwd(fol)
                self.log(reply)
            except:
                healthy = False
                self.log("Requested directory not available... Go create it first...")
                ftp.close()

        if healthy:
            try:
                self.log("MKD " + newfol)
                reply = ftp.mkd(newfol)
                self.log(reply)
            except:
                self.log("Requested new directory exists already. Uploading in there...")

            self.log("CWD " + newfol)
            reply = ftp.cwd(newfol)
            self.log(reply)

            # upload dir contents
        self.ftp = ftp
        os.chdir(self.root)
        self.files = os.listdir(self.root)
        self.manageUploads()

    def manageUploads(self):
        if len(self.files) > 0:
            fi = self.files.pop()
            self.log('STOR ' + fi)
            self.fu.initialize(fi, self.ftp)
            self.fu.start()
        else:
            self.btnUpload.setDisabled(True)
            self.log("FINISHED")
            self.ftp.close()

    def uploadDone(self, s):
        self.log(s + " uploaded..")
        self.manageUploads()


class FileUploader(QThread):
    uploadDone = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent

    def initialize(self, fi, ftp):
        self.fi = fi
        self.ftp = ftp

    def run(self):
        fi = self.fi
        ftp = self.ftp
        ftp.storbinary('STOR ' + fi, open(fi, 'rb'))
        self.uploadDone.emit(fi)
