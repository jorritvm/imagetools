from PyQt5.QtWidgets import *
from pyprojroot import here

from src.resources.uipy.about import Ui_Dialog

class AboutDialog(QDialog, Ui_Dialog):
    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        if here("README.md").exists():
            try:
                fcon = open(here("README.md"), "r")
                txt = fcon.read()
                self.textEdit.setMarkdown(txt)
            finally:
                fcon.close()
                
        
        