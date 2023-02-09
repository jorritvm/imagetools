import os
import sys
import time
import pickle #todo remove

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pyprojroot import here

from resources.resource import *

from core.mainwindow import *
from core.about import *
from core.settings import *

from threadedResizer.threadedResizer import *

from operations.importjpg import *
from operations.number import *
from operations.rename import *
from operations.resize import *
from operations.web import *
from operations.upload import *
from operations.judge import *


class MainWindow(QMainWindow, Ui_mainwindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.settings = SettingsManager(self)
        self.supervisor = Supervisor(self.settings['n_threads'], self)
        self.setup_ui()  # this is where most of the widgets are created
        self.setup_slots()
        self.setFolder(self.settings['path'])

    def setup_slots(self):
        self.widget_left.selectionChanged.connect(self.thumbnailBrowser.changeFolder)
        self.btn_import.pressed.connect(self.importButtonAction)
        self.btn_number.pressed.connect(self.numberButtonAction)
        self.btn_rename.pressed.connect(self.renameButtonAction)
        self.btn_resize.pressed.connect(self.resizeButtonAction)
        self.btn_webalbum.pressed.connect(self.webAlbumButtonAction)
        self.btn_upload.pressed.connect(self.uploadButtonAction)
        self.btn_judge.pressed.connect(self.judgeButtonAction)
        self.action_settings.triggered.connect(self.settings.show_settings)
        self.action_exit.triggered.connect(self.close)
        self.action_about.triggered.connect(self.show_about)


    def setFolder(self, path):
        self.widget_left.ui_path.setText(path)
        self.widget_left.ui_path.returnPressed.emit()

    def show_about(self):
        about = AboutDialog()
        about.exec_()
        about.close()
        
    def closeEvent(self, event):
        self.settings['path'] = self.widget_left.ui_path.text()
        self.settings.save_settings()

    def importButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            im = Import(files, self.settings, self.widget_left.ui_path.text())
            if im.exec_():
                path = im.getNewPath()
                self.setFolder(path)
            im.close()

    def numberButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog and extract the user's settings"""
            num = Number()
            settings = None
            if num.exec_():
                settings = num.getSettings()
                
                """start the rename procedure"""
                trackChanges = num.renameFiles(files, settings)
                self.thumbnailBrowser.updateElements(trackChanges)
                num.close()
       
    def renameButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            ren = Rename(files, self.supervisor)
            ren.exec_()
            ren.close()
           
            """the dialog is ready now, we should update the application with the new filenames"""
            trackChanges = ren.getChanges()
            self.thumbnailBrowser.updateElements(trackChanges)
       
  
    def resizeButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            res = Resize(files, self.supervisor, self.widget_left.ui_path.text())
            res.exec_()
            x = self.widget_left.ui_path.text()
            res.close()
         
    def webAlbumButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            wa = WebAlbum(files, self.supervisor)
            wa.exec_()
            wa.close()
           
    def uploadButtonAction(self):
        """create the dialog"""
        up = Upload(self.settings, self.widget_left.ui_path.text())
        up.exec_()
        up.close()
        
    def judgeButtonAction(self):
        files = self.thumbnailBrowser.getSelection()
        if len(files) == 0:
            QMessageBox.warning(self, "No selection", "Create a selection first.")
        else: 
            """create the dialog"""
            ju = Judge(files, self.supervisor) 
            ju.exec_()
            ju.close()

    def debug(self):
        print(self.widget_left.ui_path.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())