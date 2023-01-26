'''
Created on 19-okt.-2013

@author: jorrit
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from resources.uipy.importjpg import *
import os.path
import shutil


class Import(QDialog, Ui_Import):
    
    def __init__(self, files, settings, root,  parent=None):
        QDialog.__init__(self, parent)
    
        self.files = files
        self.root = root
        self.settings = settings
        self.total = len(self.files)
        self.progress = 0

        self.setupUi(self)
        self.setupSlots()
    
        self.presetValues()
        
        self.fh = FileHandler()
        self.fh.nextDone.connect(self.nextDone)     
        
            
    def debug(self):
        print(self.settings)
    
    def log(self, txt):
        self.text.append(txt)
        
    def setupSlots(self):
        self.btnImport.clicked.connect(self.startImport)
        self.btnGoto.clicked.connect(self.accept)
    
    def presetValues(self):
        tmp = self.files[0].lastModified()
        yyyymmdd = tmp.toString("yyyy-MM-dd")
        x = os.path.normcase(os.path.join(self.settings['defaultLocation'], yyyymmdd))
        self.editDestination.setText(x)
        
    def updateprogressBar(self):
        self.progress += 1
        x = self.progress / self.total * 100
        self.progressBar.setValue(x)
        
    def startImport(self):
        self.abort = False
        
        # is it copy or move?
        mode = ""
        if self.radioMove.isChecked():
            mode = "move"
        if self.radioCopy.isChecked():
            mode = "copy"
        self.log("Mode set to "+mode)
            
        # create the directory
        self.log("Creating main directory..")
        newPath = self.editDestination.text()
        fi = self.files[0]
        dirp = fi.dir()
        
        if dirp.mkpath(newPath):
            self.log("Directory created...")
        else:
            self.abort = True
            self.log("Creating directory failed...")
                    
        if not self.abort:
            self.mode = mode
            self.manageFiles()
    
    def manageFiles(self):
        if len(self.files) > 0:
            fi = self.files.pop()
            destDir = self.editDestination.text()
            
            self.log('Handling '+fi.fileName())
            self.fh.initialize(fi, destDir, self.mode)
            self.fh.start()
        else:
            self.btnImport.setDisabled(True)
            self.log("FINISHED")
          
        
    def nextDone(self, s):
        self.log(s + " handled..")
        self.updateprogressBar()
        self.manageFiles()
        
    def getNewPath(self):
        return self.editDestination.text()
    
    
class FileHandler(QThread):
    
    nextDone = pyqtSignal(str)
    
    def __init__(self,  parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
    
    def initialize(self, fi, destDir, mode):
        self.fi = fi
        self.destDir = destDir
        self.mode = mode

    def run(self):
        fi = self.fi
        fi_old = fi.absoluteFilePath()
        fi_new = QFileInfo(QDir(self.destDir), fi.fileName()).absoluteFilePath()
        fi_cr2_old = fi.absolutePath() + "/" +  fi.baseName() + ".CR2"
        fi_cr2_new = QFileInfo(QDir(self.destDir), fi.baseName() + ".CR2").absoluteFilePath()
         
        if self.mode == "copy":
            shutil.copy2(fi_old, fi_new)
            if os.path.exists(fi_cr2_old):
                shutil.copy2(fi_cr2_old, fi_cr2_new)
        if self.mode == "move":
            shutil.move(fi_old, fi_new)
            if os.path.exists(fi_cr2_old):
                shutil.move(fi_cr2_old, fi_cr2_new)
        
        self.nextDone.emit(fi.fileName())