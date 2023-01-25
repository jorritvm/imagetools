'''
Created on 07-okt.-2013

@author: jorrit
'''

from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from core.settings import *
import os

class SettingsRun(QDialog, Ui_SettingsDialog):
    
    def __init__(self, values, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.openActions(values) #values is a dict
                
    def openActions(self, values):
        self.nthreadsBox.setValue(values['nThreads'])
        self.saveThumbsCheck.setChecked(values['saveThumbs'])
        self.rootfolderEdit.setText(values['defaultLocation'])  
    
    def dictValues(self):
        values = dict()
        values['nThreads'] = self.nthreadsBox.value()
        values['saveThumbs'] = self.saveThumbsCheck.isChecked()
        values['defaultLocation'] = self.rootfolderEdit.text() 
        return values
            
    def closeEvent(self, ev):
            ev.accept() #redundant
            
                
        
        