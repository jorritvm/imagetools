from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from imageoperations.Numberui import *
import __main__

class Number(QDialog, Ui_Number):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        """qdialog features"""
        self.buttonStartNumbering.clicked.connect(self.accept)
        self.buttonStartNumbering.setDefault(True)
    
    
    def getSettings(self):
        """returns the user input / settings of the dialog"""
        settings = dict()
        if self.radioPre.isChecked():
            settings["position"] = "pre"
        elif self.radioSuff.isChecked():
            settings["position"] = "suff"
        else:
            settings["position"] = None
        settings["digits"] = self.spinDigits.value()
        settings["seperator"] = self.editLineSeparator.text()
        if self.checkKeepOldName.isChecked():
            settings["keepOldFileName"] = True
        else:
            settings["keepOldFileName"] = False
        return settings
    
    
    def renameFiles(self, files, settings):
        """renames the files with the given settings"""
        
        trackChanges = dict()

        """transform the settings"""
        if settings["position"] == "pre": 
            addto = 0
        elif settings["position"] == "suff":
            addto = 1
        else: 
            #print("Error, select prefix or suffix first!")
            return
        digits = settings["digits"]
        sep = settings["seperator"]
        if settings["keepOldFileName"]:
            keepold = 1
        else:
            keepold = 0
        
        """start the rename procedure"""
        for i in range(1, len(files) + 1):
            """create the objects to manipulate the files"""
            fileInfo = files[i - 1]
            ext = fileInfo.completeSuffix()
            file = QFile(fileInfo.absoluteFilePath())
            
            """create the new name"""
            newName = str(i).zfill(digits) # leading zeroes            
                        
            if not addto: #prefix
                if digits:
                    newName += sep
            
                if keepold:
                    newName += fileInfo.fileName()
                else:
                    newName += "."
                    newName += ext
                    
            else: #suffix
                if digits:
                    newName = sep + newName
                if keepold:
                    newName = fileInfo.baseName() + newName + "." + ext
                else:
                    newName += '.'
                    newName += ext

            """rename the file to the new name"""          
            absoluteNewName = fileInfo.absolutePath() + "/" + newName
            
            x = file.rename(absoluteNewName)
            if x:
                trackChanges[fileInfo.absoluteFilePath()] = absoluteNewName #list met key = oude abspath en value = new abspath
            else:
                pass
        
        return trackChanges
                
                
                
                
