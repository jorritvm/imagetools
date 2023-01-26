from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from resources.uipy.resize import *

class Resize(QDialog, Ui_Resize):
    
    def __init__(self, files, supervisor, rootPath, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.files = files #QFileInfo objects
        self.supervisor = supervisor #threaded resizer
        self.rootPath = rootPath
       
        self.settings = dict()
        self.countItemsDone = 0
        self.totalItemsTodo = len(self.files)
        
        self.setupSlots()
        
    def setupSlots(self):
        self.buttonStartResize.pressed.connect(self.startResize)
        self.buttonCancelResize.pressed.connect(self.interuptResize)
        self.supervisor.newItemReady.connect(self.processNextResizedItem)
        
    def adjustSlider(self, x):
        self.labelQuality.setText(str(x)+" %")      
               
    def startResize(self):
       
        # GET THE USER SETTINGS
        settings = dict()
        """prefix - suffix"""
        settings["dprefix"] = self.editDirPrefix.text()
        settings["prefix"] = self.editNamePrefix.text()
        settings["suffix"] = self.editNameSuffix.text()
        
        """the quality is between 1 and 100 """
        settings["quality"] = self.spinQuality.value()
        
       
        """the size settings"""
        if self.rb1.isChecked():
            settings["rb"] = 1
            settings["rb1"] = self.comboBox.currentIndex()
        elif self.rb3.isChecked():
            settings["rb"] = 3
            
            slist = self.editSize.text().split("x")
            if len(slist) == 2:
                w = int(slist[0])
                h = int(slist[1])
                settings["rb3"] = (w,h)
            else:
                error = True
                QMessageBox.warning(self, "Invalid format", "Enter size formatted like 'WIDTHxHEIGHT'!")  
        
        self.settings = settings
        
        """size can be are file specific so we define it here"""
        if self.settings["rb"] == 1:
            if self.settings["rb1"] == 0:
                w = 1280 
                h = 1024
            elif self.settings["rb1"] == 1:
                w = 1024 
                h = 786
            elif self.settings["rb1"] == 2:
                w = 800 
                h = 600
            elif self.settings["rb1"] == 3:
                w = 640 
                h = 480
            elif self.settings["rb1"] == 4:
                w = 320 
                h = 240
            elif self.settings["rb1"] == 5:
                w = 160 
                h = 120
        elif self.settings["rb"] == 3:
            w = self.settings["rb3"][0]
            h = self.settings["rb3"][1]
        
        #CREATE THE RESIZE QUEUE
        q = []
        for fi in self.files:
            q.append([fi, w, True]) #smooth
        self.currentlyProcessing = self.supervisor.addItems(q)
        self.supervisor.processQueue()  
            
    def interuptResize(self):
        self.supervisor.clearQueue()

    def processNextResizedItem(self, ticket, img):
        for item in self.currentlyProcessing:
            if item[3] == ticket:
                fileInfo = item[0]
                """create the filename of the resized file"""
                newName = ""
                newName += self.settings["prefix"]
                newName += fileInfo.baseName()
                newName += self.settings["suffix"]
                newName += "."
                newName += fileInfo.completeSuffix()

                dir = QDir(self.rootPath + "/" + self.settings["dprefix"])
                dir.mkpath(dir.absolutePath()) #creating all necessary directories

                newNameAbs = dir.absolutePath() + '/' + newName 
                print(newNameAbs)
                
                if img.save(newNameAbs,  format = None, quality = self.settings["quality"]):
                    pass
                else:
                    QMessageBox.critical(self, "Save Error", "Could not save file \n"+newNameAbs)
            
                #progressbar aanpassen
                self.countItemsDone += 1
                progress = self.countItemsDone * 100 / self.totalItemsTodo            
                self.progressBar.setValue(progress)
                
                if self.countItemsDone == self.totalItemsTodo:
                    QMessageBox.information(self,"Done", "All files have been resized...", QMessageBox.Ok, QMessageBox.Ok)
                    self.accept()
                    
            


            
  

            
            

            
            
         
       
        
