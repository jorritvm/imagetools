import os
import sys
import time
import pickle #todo remove

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pyprojroot import here

from resources.resource import *
from core.about_run import *
from core.settings import *
from core.folder_select import *
from core.thumbnailBrowser import *
from threadedResizer.threadedResizer import *

from operations.importjpg import *
from operations.number import *
from operations.rename import *
from operations.resize import *
from operations.web import *
from operations.upload import *
from operations.judge import *


class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
       
        self.settings = SettingsManager()
        self.supervisor = Supervisor(self.settings['n_threads'], self)
        
        self.widget_left = FolderSelectWidget()
        self.thumbnailBrowser = thumbnailBrowser(self.supervisor, self.settings['path'])
        self.setupUi()
        self.widget_left.selectionChanged.connect(self.thumbnailBrowser.changeFolder)
        self.setupToolButtons()
        self.setFolder(self.settings['path'])

    def debug(self):
        print(self.widget_left.ui_path.text())

    def setFolder(self, path):
        self.widget_left.ui_path.setText(path)
        self.widget_left.ui_path.returnPressed.emit()
    
    #===========================================================================
    # DIALOG HANDLING
    #===========================================================================


    
    def closeEvent(self, event):
        self.settings['path'] = self.widget_left.ui_path.text()
        self.save_settings()
    
    def showAbout(self):
        about = AboutRun()
        about.exec_()
        about.close()
        

    #===========================================================================
    # TOOL BUTTONS ACTIONS
    #===========================================================================
    
    def setupToolButtons(self):
        self.uiBtnImport.pressed.connect(self.importButtonAction)
        self.uiBtnNumber.pressed.connect(self.numberButtonAction)
        self.uiBtnRename.pressed.connect(self.renameButtonAction)
        self.uiBtnResize.pressed.connect(self.resizeButtonAction)
        self.uiBtnWebAlbum.pressed.connect(self.webAlbumButtonAction)
        self.uiBtnUpload.pressed.connect(self.uploadButtonAction)
        self.uiBtnJudge.pressed.connect(self.judgeButtonAction)
        
        self.uiBtnAutoSelect.setDisabled(True)
        self.uiBtnRotate.setDisabled(True)
        
    
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

            
    #===========================================================================
    # SET UP UI
    #===========================================================================
        
    def setupUi(self):

        self.centralWidget = QWidget(self)
        self.setWindowTitle("Imagetools")
        
        #=======================================================================
        # """create toolbuttons"""
        #=======================================================================
        self.uiBtnAutoSelect = QPushButton("1. Auto Select")
        self.uiBtnImport = QPushButton("2. Import")
        self.uiBtnRotate = QPushButton("3. Rotate")
        self.uiBtnNumber = QPushButton("4. Number")
        self.uiBtnJudge = QPushButton("5. Judge")
        self.uiBtnRename = QPushButton("6. Rename")
        self.uiBtnResize = QPushButton("7. Resize")
        self.uiBtnWebAlbum = QPushButton("8. Web Album")
        self.uiBtnUpload = QPushButton("9. Upload")
        BtnList = [self.uiBtnAutoSelect, self.uiBtnImport, self.uiBtnRotate, self.uiBtnNumber, self.uiBtnJudge, self.uiBtnRename, self.uiBtnResize, self.uiBtnWebAlbum, self.uiBtnUpload]
                
        """layout buttons 3x3"""
        self.groupActions = QGroupBox("Actions")
        self.uiLayoutBtns = QGridLayout(self.groupActions)
        i = 0
        for Btn in BtnList:
            x = i % 3
            y = int(i/3)
            self.uiLayoutBtns.addWidget(Btn,y,x)
            i += 1
        self.uiLayoutBtns.setContentsMargins(4,4,4,4)
        self.uiLayoutBtns.setSpacing(4)
        self.groupActions.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum))
     
        self.uiLayoutRight = QVBoxLayout()
        self.uiLayoutRight.addWidget(self.thumbnailBrowser)
        self.uiLayoutRight.addWidget(self.groupActions)
        self.uiLayoutRight.setContentsMargins(0,0,0,0)
        
        self.widgetRight = QWidget()
        self.widgetRight.setLayout(self.uiLayoutRight)
        
        
        #=======================================================================
        # """globale layout"""
        #=======================================================================
        """vertical splitter (left | right)"""
        self.hsplitter = QSplitter()
        self.hsplitter.addWidget(self.widget_left)
        self.hsplitter.addWidget(self.widgetRight)
                  
        """setting the central widget and its contents"""
        self.setCentralWidget(self.centralWidget)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.addWidget(self.hsplitter)
        
        """size"""
        self.resize(800, 600)
        self.hsplitter.setSizes([150,300]) #this gives us a nice startup size distribution
        #sizepol = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        #self.ui_tree.setSizePolicy(sizepol)
        
        self.setWindowIcon(QIcon(":/appicon.ico"))
        
        """create menubar"""
        settingsAction = QAction("&Settings", self)
        settingsAction.triggered.connect(self.show_settings)
        exitAction = QAction('&Exit', self)        
        exitAction.triggered.connect(qApp.quit)
        aboutAction = QAction('&About', self)        
        aboutAction.triggered.connect(self.showAbout)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(settingsAction)
        fileMenu.addAction(exitAction)
        helpMenu = menubar.addMenu("&Help")
        helpMenu .addAction(aboutAction)
        
        debugAction = QAction("&Debug", self)
        debugAction.triggered.connect(self.debug)
        helpMenu.addAction(debugAction)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())