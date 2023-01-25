'''
Created on 10-sep.-2013

@author: jorrit
'''

from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from core.about import *
import os

class AboutRun(QDialog, Ui_Dialog):
    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        if os.path.exists("README.txt"):
            try: 
                x = open("README.txt","r")
                txt = x.read()
                self.textEdit.setStyleSheet("font: 10pt \"Courier\";");
                self.textEdit.append("<hr><span style='font-family: monospace'> ")
                self.textEdit.append(str(txt))
                    
            finally:
                x.close()
                
        
        